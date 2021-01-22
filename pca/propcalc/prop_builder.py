# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from itertools import product
import importlib
module_name = 'subpackage.i.import'
special_module = importlib.import_module(module_name, package='my_current_pkg')

from ..tools.proposition import BinaryOp, ConjunctionOp, DisjunctionOp, EquivalenceOp, FalseProp
from ..tools.proposition import ImplicationOp, NegationOp, TrueProp, UnaryOp, Variable
from ..tools.parser import PARSER


class InitProp:
    __slots__ = ('_prop', '_parsed')

    def __init__(self, prop: str) -> None:
        self._prop = prop
        self._parsed = PARSER.parse(prop)

    def __eq__(self, other) -> bool:
        """
        Structural equivalence
        'A or B' != 'B or A'
        'A or B' == '(A or B)'
        :param other:
        :return: bool
        """
        return isinstance(other, self.__class__) and self._parsed == other._parsed

    def build_interp(self, max_vars: int = 5):
        prop_vars = sorted(set(_get_vars(self._parsed)))
        len_prop_vars = len(prop_vars)
        all_interp = []
        if len_prop_vars < 1:
            raise ValueError('Number of variables must be at least 1')
        if len_prop_vars > max_vars:
            raise ValueError(f'Variable length {len_prop_vars}, exceeded the allowed {max_vars}')
        for comb in product([FalseProp(), TrueProp()], repeat=len_prop_vars):
            interp = dict(zip(prop_vars, comb))
            interp_prop = _get_interp(self._parsed, interp)
            all_interp.append((interp, _eval_prop(interp_prop)))
        return all_interp

    # TODO: Implement better SAT solver.
    def satisfiable(self) -> bool:
        for i in self.build_interp():
            for j in i:
                if isinstance(j, (bool, TrueProp, FalseProp)) and j:
                    return True
        return False

    def tautology(self) -> bool:
        for i in self.build_interp():
            for j in i:
                if isinstance(j, (bool, TrueProp, FalseProp)) and not j:
                    return False
        return True

    def contradiction(self) -> bool:
        return not self.satisfiable()

    def cnf(self):
        raise NotImplementedError

    def minimize(self):
        raise NotImplementedError


def _get_vars(op):
    if isinstance(op, Variable):
        return [op]
    elif isinstance(op, UnaryOp):
        return _get_vars(op.prop)
    elif isinstance(op, BinaryOp):
        return _get_vars(op.prop_l) + _get_vars(op.prop_r)
    else:
        return []


def _get_interp(op, interp):
    if isinstance(op, (bool, TrueProp, FalseProp)):
        return op
    elif isinstance(op, Variable):
        return interp[op]
    elif isinstance(op, UnaryOp):
        return op.__class__(_get_interp(op.prop, interp))
    elif isinstance(op, BinaryOp):
        return op.__class__(_get_interp(op.prop_l, interp), _get_interp(op.prop_r, interp))
    else:
        raise TypeError({type(op)})


def _eval_prop(op):
    if isinstance(op, (bool, TrueProp, FalseProp)):
        return op
    elif isinstance(op, NegationOp):
        if isinstance(op.prop, (bool, TrueProp, FalseProp)):
            return op.eval()
        return op.__class__(_eval_prop(op.prop)).eval()
    elif isinstance(op, (DisjunctionOp, ConjunctionOp, ImplicationOp, EquivalenceOp)):
        if all(isinstance(prop, (bool, TrueProp, FalseProp)) for prop in [op.prop_l, op.prop_r]):
            return op.eval()
        elif isinstance(op.prop_l, (bool, TrueProp, FalseProp)):
            return op.__class__(op.prop_l, _eval_prop(op.prop_r)).eval()
        elif isinstance(op.prop_r, (bool, TrueProp, FalseProp)):
            return op.__class__(_eval_prop(op.prop_l), op.prop_r).eval()
        else:
            return op.__class__(_eval_prop(op.prop_l), _eval_prop(op.prop_r)).eval()
    else:
        raise TypeError({type(op)})

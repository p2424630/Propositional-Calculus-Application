# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from itertools import product
from pca_main import pcaprop, pcaparser


class InitProp:
    __slots__ = ('prop', 'parsed')

    def __init__(self, prop: str) -> None:
        self.prop = prop
        self.parsed = pcaparser.PARSER.parse(prop)

    def __eq__(self, other) -> bool:
        """
        Structural equivalence
        'A or B' != 'B or A'
        'A or B' == '(A or B)'
        :param other:
        :return: bool
        """
        return isinstance(other, self.__class__) and self.parsed == other.parsed

    def unique_vars(self):
        return sorted(x.name for x in set(_get_vars(self.parsed)))

    def build_interp(self, max_vars: int = 50):
        prop_vars = sorted(set(_get_vars(self.parsed)))
        len_prop_vars = len(prop_vars)
        all_interp = []
        if len_prop_vars < 1:
            raise ValueError('Number of variables must be at least 1')
        if len_prop_vars > max_vars:
            raise ValueError(f'Variable length {len_prop_vars}, exceeded the allowed {max_vars}')
        for comb in product([pcaprop.FalseProp(), pcaprop.TrueProp()], repeat=len_prop_vars):
            interp = dict(zip(prop_vars, comb))
            interp_prop = _get_interp(self.parsed, interp)
            list_vals = [bool(x) for x in interp.values()]
            list_vals.append(bool(_eval_prop(interp_prop)))
            all_interp.append(list_vals)
        return all_interp

    # TODO: Implement better SAT solver. Do not rely on truth table, prop with only bool values must still be checked
    def satisfiable(self) -> bool:
        for i in self.build_interp():
            if i[-1]:
                return True
        return False

    def tautology(self) -> bool:
        for i in self.build_interp():
            if not i[-1]:
                return False
        return True

    def contradiction(self) -> bool:
        return not self.satisfiable()

    def cnf(self):
        raise NotImplementedError

    def minimize(self):
        raise NotImplementedError


def _get_vars(op):
    if isinstance(op, pcaprop.Variable):
        return [op]
    elif isinstance(op, pcaprop.UnaryOp):
        return _get_vars(op.prop)
    elif isinstance(op, pcaprop.BinaryOp):
        return _get_vars(op.prop_l) + _get_vars(op.prop_r)
    else:
        return []


def _get_interp(op, interp):
    if isinstance(op, (bool, pcaprop.TrueProp, pcaprop.FalseProp)):
        return op
    elif isinstance(op, pcaprop.Variable):
        return interp[op]
    elif isinstance(op, pcaprop.UnaryOp):
        return op.__class__(_get_interp(op.prop, interp))
    elif isinstance(op, pcaprop.BinaryOp):
        return op.__class__(_get_interp(op.prop_l, interp), _get_interp(op.prop_r, interp))
    else:
        raise TypeError({type(op)})


def _eval_prop(op):
    if isinstance(op, (bool, pcaprop.TrueProp, pcaprop.FalseProp)):
        return op
    elif isinstance(op, pcaprop.NegationOp):
        if isinstance(op.prop, (bool, pcaprop.TrueProp, pcaprop.FalseProp)):
            return op.eval()
        return op.__class__(_eval_prop(op.prop)).eval()
    elif isinstance(op, (pcaprop.DisjunctionOp, pcaprop.ConjunctionOp, pcaprop.ImplicationOp, pcaprop.EquivalenceOp)):
        if all(isinstance(prop, (bool, pcaprop.TrueProp, pcaprop.FalseProp)) for prop in [op.prop_l, op.prop_r]):
            return op.eval()
        elif isinstance(op.prop_l, (bool, pcaprop.TrueProp, pcaprop.FalseProp)):
            return op.__class__(op.prop_l, _eval_prop(op.prop_r)).eval()
        elif isinstance(op.prop_r, (bool, pcaprop.TrueProp, pcaprop.FalseProp)):
            return op.__class__(_eval_prop(op.prop_l), op.prop_r).eval()
        else:
            return op.__class__(_eval_prop(op.prop_l), _eval_prop(op.prop_r)).eval()
    else:
        raise TypeError({type(op)})

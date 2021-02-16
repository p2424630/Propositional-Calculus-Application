# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from itertools import product
from pca_main import pcaprop, pcaparser


class PropLaws:
    __slots__ = ('proposition', 'parsed')

    def __init__(self, proposition: str) -> None:
        self.proposition = proposition
        self.parsed = pcaparser.PARSER.parse(proposition)

    def idempotence(self):
        return

    def commutativity(self):
        return

    def associativity(self):
        return

    def absorption(self):
        return

    def distributivity(self):
        return

    def maximum(self):
        return

    def minimum(self):
        return

    def excluded_middle(self):
        return

    def de_morgan(self):
        return

    def implication(self):
        return

    def contrapositive(self):
        return

    def equivalence(self):
        return


class InitProp(PropLaws):

    def __init__(self, prop: str):
        super().__init__(prop)

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
        return sorted(set(_get_vars(self.parsed)))

    def interpretations(self, max_vars: int = 10):
        prop_vars = self.unique_vars()
        len_prop_vars = len(prop_vars)
        if len_prop_vars < 1:
            raise ValueError('Number of variables must be at least 1')
        elif len_prop_vars > max_vars:
            raise ValueError(f'Variable length {len_prop_vars}, exceeded the allowed {max_vars}')
        for comb in product([pcaprop.FalseProp(), pcaprop.TrueProp()], repeat=len_prop_vars):
            interp = dict(zip(prop_vars, comb))
            interp_prop = _get_interp(self.parsed, interp)
            interp_values = list(interp.values())
            interp_values.append(_eval_prop(interp_prop))
            yield interp_values

    # TODO: Implement better SAT solver.
    def satisfiable(self) -> bool:
        for i in self.interpretations():
            if i[-1]:
                return True
        return False

    def tautology(self) -> bool:
        for i in self.interpretations():
            if not i[-1]:
                return False
        return True

    def contradiction(self) -> bool:
        return not self.satisfiable()

    def cnf(self):
        return

    def minimize(self):
        return


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

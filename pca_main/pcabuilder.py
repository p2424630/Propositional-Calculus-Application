# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from itertools import product
from pca_main import pcaprop, pcaparser


class InitProp:
    __slots__ = ('proposition', 'parsed')

    def __init__(self, proposition: str) -> None:
        self.proposition = proposition
        self.parsed = pcaparser.PARSER.parse(proposition)

    def __eq__(self, other) -> bool:
        """
        Structural equivalence
        'A or B' != 'B or A'
        'A or B' == '(A or B)'
        :param other:
        :return: bool
        """
        return isinstance(other, self.__class__) and self.parsed == other.parsed

    def __str__(self):
        return str(self.parsed)

    def __repr__(self):
        return repr(self.parsed)

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

    def idempotence(self):
        return _idempotence(self.parsed)

    def commutativity(self):
        return _commutativity(self.parsed)

    def associativity(self):
        return _associativity(self.parsed)

    def absorption(self):
        return _absorption(self.parsed)

    def distributivity(self):
        return _distributivity(self.parsed)

    def maximum(self):
        return _maximum(self.parsed)

    def minimum(self):
        return _minimum(self.parsed)

    def excluded_middle(self):
        return _excluded_middle(self.parsed)

    def de_morgan(self):
        return _de_morgan(self.parsed)

    def implication(self):
        return _implication(self.parsed)

    def contrapositive(self):
        return _contrapositive(self.parsed)

    def equivalence(self):
        return _equivalence(self.parsed)

    def involution(self):
        return _involution(self.parsed)


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


def _idempotence(op):
    if isinstance(op, (pcaprop.Variable, pcaprop.TrueProp, pcaprop.FalseProp)):
        return op
    if isinstance(op, pcaprop.NegationOp):
        return op.__class__(_idempotence(op.prop))
    elif isinstance(op, (pcaprop.DisjunctionOp, pcaprop.ConjunctionOp)):
        if op.prop_l == op.prop_r:
            return op.prop_l
    return op.__class__(_idempotence(op.prop_l), _idempotence(op.prop_r))


def _commutativity(op):
    if isinstance(op, (pcaprop.Variable, pcaprop.TrueProp, pcaprop.FalseProp)):
        return op
    if isinstance(op, pcaprop.NegationOp):
        return op.__class__(_commutativity(op.prop))
    elif isinstance(op, (pcaprop.ImplicationOp, pcaprop.EquivalenceOp)):
        return op.__class__(_commutativity(op.prop_l), _commutativity(op.prop_r))
    elif isinstance(op, (pcaprop.DisjunctionOp, pcaprop.ConjunctionOp)):
        if all(isinstance(prop, (pcaprop.Variable, pcaprop.FalseProp, pcaprop.TrueProp)
                          ) for prop in [op.prop_l, op.prop_r]):
            return op.__class__(op.prop_r, op.prop_l)
    return op.__class__(_commutativity(op.prop_r), _commutativity(op.prop_l))


def _maximum(op):
    if isinstance(op, (pcaprop.Variable, pcaprop.TrueProp, pcaprop.FalseProp)):
        return op
    elif isinstance(op, pcaprop.NegationOp):
        return op.__class__(_maximum(op.prop))
    elif isinstance(op, (pcaprop.ImplicationOp, pcaprop.EquivalenceOp)):
        return op.__class__(_maximum(op.prop_l), _maximum(op.prop_r))
    elif isinstance(op, pcaprop.DisjunctionOp):
        if any(isinstance(prop, pcaprop.TrueProp) for prop in [op.prop_l, op.prop_r]):
            return pcaprop.TrueProp()
    elif isinstance(op, pcaprop.ConjunctionOp):
        if isinstance(op.prop_l, pcaprop.TrueProp):
            return _maximum(op.prop_r)
        elif isinstance(op.prop_r, pcaprop.TrueProp):
            return _maximum(op.prop_l)
    return op.__class__(_maximum(op.prop_l), _maximum(op.prop_r))


def _minimum(op):
    if isinstance(op, (pcaprop.Variable, pcaprop.TrueProp, pcaprop.FalseProp)):
        return op
    elif isinstance(op, pcaprop.NegationOp):
        return op.__class__(_minimum(op.prop))
    elif isinstance(op, (pcaprop.ImplicationOp, pcaprop.EquivalenceOp)):
        return op.__class__(_minimum(op.prop_l), _minimum(op.prop_r))
    elif isinstance(op, pcaprop.ConjunctionOp):
        if any(isinstance(prop, pcaprop.FalseProp) for prop in [op.prop_l, op.prop_r]):
            return pcaprop.FalseProp()
    elif isinstance(op, pcaprop.DisjunctionOp):
        if isinstance(op.prop_l, pcaprop.FalseProp):
            return _minimum(op.prop_r)
        elif isinstance(op.prop_r, pcaprop.FalseProp):
            return _minimum(op.prop_l)
    return op.__class__(_minimum(op.prop_l), _minimum(op.prop_r))


def _involution(op):
    if isinstance(op, (pcaprop.DisjunctionOp, pcaprop.ConjunctionOp, pcaprop.ImplicationOp, pcaprop.EquivalenceOp)):
        return op.__class__(_involution(op.prop_l), _involution(op.prop_r))
    elif isinstance(op, pcaprop.NegationOp):
        if isinstance(op.prop, pcaprop.NegationOp):
            return _involution(op.prop.prop)
        else:
            return op.__class__(_involution(op.prop))
    return op


def _de_morgan(op):
    if isinstance(op, (pcaprop.DisjunctionOp, pcaprop.ConjunctionOp, pcaprop.ImplicationOp, pcaprop.EquivalenceOp)):
        return op.__class__(_de_morgan(op.prop_l), _de_morgan(op.prop_r))
    elif isinstance(op, pcaprop.NegationOp):
        if isinstance(op.prop, pcaprop.DisjunctionOp):
            return pcaprop.ConjunctionOp(pcaprop.NegationOp(op.prop.prop_l), pcaprop.NegationOp(op.prop.prop_r))
        elif isinstance(op.prop, pcaprop.ConjunctionOp):
            return pcaprop.DisjunctionOp(pcaprop.NegationOp(op.prop.prop_l), pcaprop.NegationOp(op.prop.prop_r))
        else:
            return op.__class__(_de_morgan(op.prop))
    return op


def _implication(op):
    if isinstance(op, (pcaprop.DisjunctionOp, pcaprop.ConjunctionOp, pcaprop.EquivalenceOp)):
        return op.__class__(_implication(op.prop_l), _implication(op.prop_r))
    elif isinstance(op, pcaprop.NegationOp):
        return op.__class__(_implication(op.prop))
    elif isinstance(op, pcaprop.ImplicationOp):
        return pcaprop.DisjunctionOp(pcaprop.NegationOp(op.prop_l), op.prop_r)
    return op


def _associativity(op):
    return


def _absorption(op):
    return


def _distributivity(op):
    return


def _excluded_middle(op):
    return


def _contrapositive(op):
    return


def _equivalence(op):
    return

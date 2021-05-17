# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from itertools import product
from pca_main import pcaprop, pcaparser


class Laws:
    __slots__ = '_parsed'

    def __init__(self, proposition: str) -> None:
        self._parsed = pcaparser.PARSER.parse(proposition)

    def commutativity(self):
        return _commutativity(self._parsed)

    def de_morgan(self):
        return _de_morgan(self._parsed)

    def idempotence(self):
        return _idempotence(self._parsed)

    def implication(self):
        return _implication(self._parsed)

    def involution(self):
        return _involution(self._parsed)

    def maximum(self):
        return _maximum(self._parsed)

    def minimum(self):
        return _minimum(self._parsed)


class InitProp(Laws):

    def __eq__(self, other) -> bool:
        """
        Structural equivalence
        'A or B' != 'B or A'
        'A or B' == '(A or B)'
        :param other:
        :return: bool
        """
        return isinstance(other, self.__class__) and self._parsed == other._parsed

    def __str__(self):
        return str(self._parsed)

    def __repr__(self):
        return repr(self._parsed)

    def unique_vars(self):
        """
        :return: Sorted list of all unique variables.
        """
        return sorted(set(_get_vars(self._parsed)))

    def interpretations(self, max_vars: int = 10):
        """
        Create all possible interpretations for all unique variables. For each interpretation replace the variables in
        the proposition and evaluate, the result is then appended to the current interpretation's list and yielded.
        :param: max_vars -The number of maximum variables the proposition can have.
        :return: iterable
        """
        prop_vars = self.unique_vars()
        len_prop_vars = len(prop_vars)
        if len_prop_vars < 1:
            # Return empty interpretation as this means the proposition is composed without any variables,
            # which means it can only take one, the current, interpretation.
            return
        if len_prop_vars > max_vars:
            raise ValueError(f'Variable length {len_prop_vars}, exceeded the allowed {max_vars}')
        # List of tuples for all possible interpretations for given number of variables
        combinations = product([pcaprop.FalseProp(), pcaprop.TrueProp()], repeat=len_prop_vars)
        for combination in combinations:
            # Create a dictionary mapping the variables to the current interpretation values.
            interp = dict(zip(prop_vars, combination))
            # Replace the variables in the proposition with the current interpretation mapping.
            interp_prop = _get_interp(self._parsed, interp)
            interp_values = list(interp.values())
            # For the current interpretation evaluate the proposition and append the result in the original
            # interpretation list.
            interp_values.append(_eval_prop(interp_prop))
            yield interp_values

    def satisfiable(self):
        """
        Check if self is satisfiable, this is calculated based on all interpretations.
        :return: bool (Class)
        """
        if len(self.unique_vars()) < 1:
            return _eval_prop(self._parsed)
        for i in self.interpretations():
            if i[-1]:
                return pcaprop.TrueProp()
        return pcaprop.FalseProp()

    def tautology(self):
        """
        Check if self is a tautology, this is calculated based on all interpretations.
        :return: bool (Class)
        """
        if len(self.unique_vars()) < 1:
            return _eval_prop(self._parsed)
        for i in self.interpretations():
            if not i[-1]:
                return pcaprop.FalseProp()
        return pcaprop.TrueProp()

    def contradiction(self):
        """
        Check if self is a contradiction by returning the opposite of satisfiable.
        :return: bool (Class)
        """
        return pcaprop.FalseProp() if self.satisfiable() else pcaprop.TrueProp()


def _get_vars(op):
    """
    Recursively traverse proposition and return a list of all variables.
    :param op: Proposition
    :return: list of variables
    """
    if isinstance(op, pcaprop.Variable):
        return [op]
    if isinstance(op, pcaprop.UnaryOp):
        return _get_vars(op.prop)
    if isinstance(op, pcaprop.BinaryOp):
        return _get_vars(op.prop_l) + _get_vars(op.prop_r)
    return []


def _get_interp(op, interp):
    """
    Recursively traverse proposition and replace all instances of variables with the interpretation mapping.
    :param op: Proposition
    :param interp: Dictionary mapping variables to TrueProp or FalseProp.
    :return: Proposition with FalseProp/TrueProp instead of Variables.
    """
    if isinstance(op, (bool, pcaprop.TrueProp, pcaprop.FalseProp)):
        return op
    if isinstance(op, pcaprop.Variable):
        return interp[op]
    if isinstance(op, pcaprop.UnaryOp):
        return op.__class__(_get_interp(op.prop, interp))
    if isinstance(op, pcaprop.BinaryOp):
        return op.__class__(_get_interp(op.prop_l, interp), _get_interp(op.prop_r, interp))


def _eval_prop(op):
    """
    Recursively traverse proposition evaluate.
    :param op: Proposition
    :return: bool (Class)
    """
    if isinstance(op, (bool, pcaprop.TrueProp, pcaprop.FalseProp)):
        return op
    if isinstance(op, pcaprop.NegationOp):
        return op.__class__(_eval_prop(op.prop)).eval()
    if isinstance(op, (pcaprop.DisjunctionOp, pcaprop.ConjunctionOp, pcaprop.ImplicationOp, pcaprop.EquivalenceOp)):
        return op.__class__(_eval_prop(op.prop_l), _eval_prop(op.prop_r)).eval()


def _idempotence(op):
    """
    Recursively traverse proposition postorder (left->right->root) and check on Disjunction and Conjunction operations
    if left child equals right.
    :param op: Proposition
    :return: Proposition
    """
    if isinstance(op, (pcaprop.Variable, pcaprop.TrueProp, pcaprop.FalseProp)):
        return op
    if isinstance(op, pcaprop.UnaryOp):
        return op.__class__(_idempotence(op.prop))
    if isinstance(op, pcaprop.BinaryOp):
        prop_l = _idempotence(op.prop_l)
        prop_r = _idempotence(op.prop_r)
        if isinstance(op, (pcaprop.DisjunctionOp, pcaprop.ConjunctionOp)) and (prop_l == prop_r):
            return prop_l
        return op.__class__(prop_l, prop_r)


def _commutativity(op):
    """
    Recursively traverse proposition and for all Binary operations besides implication and equivalence, switch the
    positions of left and right child.
    :param op: Proposition
    :return: Proposition
    """
    if isinstance(op, (pcaprop.Variable, pcaprop.TrueProp, pcaprop.FalseProp)):
        return op
    if isinstance(op, pcaprop.UnaryOp):
        return op.__class__(_commutativity(op.prop))
    if isinstance(op, pcaprop.BinaryOp):
        # Same order for implication or equivalence
        if isinstance(op, (pcaprop.ImplicationOp, pcaprop.EquivalenceOp)):
            return op.__class__(_commutativity(op.prop_l), _commutativity(op.prop_r))
        return op.__class__(_commutativity(op.prop_r), _commutativity(op.prop_l))


def _maximum(op):
    """
    Recursively traverse proposition postorder (left->right->root) and check if disjunction and either left or right
    child is TrueProp then return TrueProp or if it's conjunction then return left if right is TrueProp or right if
    left is TrueProp.
    :param op: Proposition
    :return: Proposition
    """
    if isinstance(op, (pcaprop.Variable, pcaprop.TrueProp, pcaprop.FalseProp)):
        return op
    if isinstance(op, pcaprop.UnaryOp):
        return op.__class__(_maximum(op.prop))
    if isinstance(op, pcaprop.BinaryOp):
        prop_l = _maximum(op.prop_l)
        prop_r = _maximum(op.prop_r)
        if isinstance(op, pcaprop.DisjunctionOp):
            if any(isinstance(prop, pcaprop.TrueProp) for prop in [prop_l, prop_r]):
                return pcaprop.TrueProp()
        if isinstance(op, pcaprop.ConjunctionOp):
            if isinstance(prop_l, pcaprop.TrueProp):
                return prop_r
            if isinstance(prop_r, pcaprop.TrueProp):
                return prop_l
        return op.__class__(prop_l, prop_r)


def _minimum(op):
    """
    Recursively traverse proposition postorder (left->right->root) and check if conjunction and either left or right
    child is FalseProp then return FalseProp if it's disjunction then return left if right is FalseProp or right if
    left is FalseProp.
    :param op: Proposition
    :return: Proposition
    """
    if isinstance(op, (pcaprop.Variable, pcaprop.TrueProp, pcaprop.FalseProp)):
        return op
    if isinstance(op, pcaprop.UnaryOp):
        return op.__class__(_minimum(op.prop))
    if isinstance(op, pcaprop.BinaryOp):
        prop_l = _minimum(op.prop_l)
        prop_r = _minimum(op.prop_r)
        if isinstance(op, pcaprop.ConjunctionOp):
            if any(isinstance(prop, pcaprop.FalseProp) for prop in [prop_l, prop_r]):
                return pcaprop.FalseProp()
        if isinstance(op, pcaprop.DisjunctionOp):
            if isinstance(prop_l, pcaprop.FalseProp):
                return prop_r
            if isinstance(prop_r, pcaprop.FalseProp):
                return prop_l
        return op.__class__(prop_l, prop_r)


def _involution(op):
    """
    Recursively traverse proposition and if the current proposition is Negation and the child is Negation then return
    the child of child.
    :param op: Proposition
    :return: Proposition
    """
    if isinstance(op, (pcaprop.Variable, pcaprop.TrueProp, pcaprop.FalseProp)):
        return op
    if isinstance(op, pcaprop.BinaryOp):
        return op.__class__(_involution(op.prop_l), _involution(op.prop_r))
    if isinstance(op, pcaprop.NegationOp):
        if isinstance(op.prop, pcaprop.NegationOp):
            return _involution(op.prop.prop)
        return op.__class__(_involution(op.prop))


def _de_morgan(op):
    """
    Recursively traverse proposition and apply de_morgan transformation on all Disjunction and Conjunction operations.
    :param op: Proposition
    :return: Proposition
    """
    if isinstance(op, (pcaprop.Variable, pcaprop.TrueProp, pcaprop.FalseProp)):
        return op
    if isinstance(op, pcaprop.UnaryOp):
        return op.__class__(_de_morgan(op.prop))
    if isinstance(op, pcaprop.BinaryOp):
        if isinstance(op, pcaprop.DisjunctionOp):
            return pcaprop.NegationOp(pcaprop.ConjunctionOp(pcaprop.NegationOp(_de_morgan(op.prop_l)),
                                                            pcaprop.NegationOp(_de_morgan(op.prop_r))))
        if isinstance(op, pcaprop.ConjunctionOp):
            return pcaprop.NegationOp(pcaprop.DisjunctionOp(pcaprop.NegationOp(_de_morgan(op.prop_l)),
                                                            pcaprop.NegationOp(_de_morgan(op.prop_r))))
        return op.__class__(_de_morgan(op.prop_l), _de_morgan(op.prop_r))


def _implication(op):
    """
    Recursively traverse proposition and apply implication tranformation on all implication operations.
    :param op: Proposition
    :return: Proposition
    """
    if isinstance(op, (pcaprop.Variable, pcaprop.TrueProp, pcaprop.FalseProp)):
        return op
    if isinstance(op, pcaprop.UnaryOp):
        return op.__class__(_implication(op.prop))
    if isinstance(op, pcaprop.BinaryOp):
        if isinstance(op, pcaprop.ImplicationOp):
            return pcaprop.DisjunctionOp(pcaprop.NegationOp(_implication(op.prop_l)), _implication(op.prop_r))
        return op.__class__(_implication(op.prop_l), _implication(op.prop_r))

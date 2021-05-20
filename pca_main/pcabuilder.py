# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from itertools import product

from pca_main import pcaprop, pcaparser, pcalaws


class InitProp(pcalaws.Laws):
    __slots__ = '_parsed'

    def __init__(self, proposition: str) -> None:
        self._parsed = pcaparser.PARSER.parse(proposition)

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

    @property
    def proposition(self):
        return self._parsed

    def unique_vars(self):
        """
        :return: Sorted list of all unique variables.
        """

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

        return sorted(set(_get_vars(self._parsed)))

    def interpretations(self):
        """
        Create all possible interpretations for all unique variables. For each interpretation replace the variables in
        the proposition and evaluate, the result is then appended to the current interpretation's list and yielded.
        :return: iterable
        """

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

        prop_vars = self.unique_vars()
        len_prop_vars = len(prop_vars)
        if len_prop_vars < 1:
            # Return empty interpretation as this means the proposition is composed without any variables,
            # which means it can only take one, the current, interpretation.
            return
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
            interp_values.append(self.eval_prop(interp_prop))
            yield interp_values

    def satisfiable(self):
        """
        Check if self is satisfiable, this is calculated based on all interpretations.
        :return: bool (Class)
        """

        if len(self.unique_vars()) < 1:
            return self.eval_prop(self._parsed)
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
            return self.eval_prop(self._parsed)
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

    @staticmethod
    def eval_prop(op):
        """
        Recursively traverse proposition and perform evaluation.
        :param op: Proposition
        :return: bool (Class)
        """

        def _eval_prop(op):
            if isinstance(op, (bool, pcaprop.TrueProp, pcaprop.FalseProp)):
                return op
            if isinstance(op, pcaprop.NegationOp):
                return op.__class__(_eval_prop(op.prop)).eval()
            if isinstance(op,
                          (pcaprop.DisjunctionOp, pcaprop.ConjunctionOp, pcaprop.ImplicationOp, pcaprop.EquivalenceOp)):
                return op.__class__(_eval_prop(op.prop_l), _eval_prop(op.prop_r)).eval()

        return _eval_prop(op)

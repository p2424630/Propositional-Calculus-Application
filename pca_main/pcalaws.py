# @Author: GKarseras
# @Date:   10 May 2021 12:28

from abc import ABC, abstractmethod

from pca_main import pcaprop


class Laws(ABC):

    @abstractmethod
    def proposition(self):
        raise NotImplementedError

    def commutativity(self):
        """
        Recursively traverse proposition and for all Binary operations besides implication and equivalence,
        switch the positions of left and right child.
        :param op: Proposition
        :return: Proposition
        """

        def _commutativity(op):
            if isinstance(op, (pcaprop.Variable, pcaprop.TrueProp, pcaprop.FalseProp)):
                return op
            if isinstance(op, pcaprop.UnaryOp):
                return op.__class__(_commutativity(op.prop))
            if isinstance(op, pcaprop.BinaryOp):
                # Same order for implication or equivalence
                if isinstance(op, (pcaprop.ImplicationOp, pcaprop.EquivalenceOp)):
                    return op.__class__(_commutativity(op.prop_l), _commutativity(op.prop_r))
                return op.__class__(_commutativity(op.prop_r), _commutativity(op.prop_l))

        return _commutativity(self.proposition)

    def de_morgan(self):
        """
        Recursively traverse proposition and apply de_morgan transformation on all Disjunction and Conjunction operations.
        :param op: Proposition
        :return: Proposition
        """

        def _de_morgan(op):
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

        return _de_morgan(self.proposition)

    def idempotence(self):
        """
        Recursively traverse proposition postorder (left->right->root) and check on Disjunction and Conjunction operations
        if left child equals right.
        :param op: Proposition
        :return: Proposition
        """

        def _idempotence(op):
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

        return _idempotence(self.proposition)

    def implication(self):
        """
        Recursively traverse proposition and apply implication tranformation on all implication operations.
        :param op: Proposition
        :return: Proposition
        """

        def _implication(op):
            if isinstance(op, (pcaprop.Variable, pcaprop.TrueProp, pcaprop.FalseProp)):
                return op
            if isinstance(op, pcaprop.UnaryOp):
                return op.__class__(_implication(op.prop))
            if isinstance(op, pcaprop.BinaryOp):
                if isinstance(op, pcaprop.ImplicationOp):
                    return pcaprop.DisjunctionOp(pcaprop.NegationOp(_implication(op.prop_l)), _implication(op.prop_r))
                return op.__class__(_implication(op.prop_l), _implication(op.prop_r))

        return _implication(self.proposition)

    def involution(self):
        """
        Recursively traverse proposition and if the current proposition is Negation and the child is Negation then return
        the child of child.
        :param op: Proposition
        :return: Proposition
        """

        def _involution(op):
            if isinstance(op, (pcaprop.Variable, pcaprop.TrueProp, pcaprop.FalseProp)):
                return op
            if isinstance(op, pcaprop.BinaryOp):
                return op.__class__(_involution(op.prop_l), _involution(op.prop_r))
            if isinstance(op, pcaprop.NegationOp):
                if isinstance(op.prop, pcaprop.NegationOp):
                    return _involution(op.prop.prop)
                return op.__class__(_involution(op.prop))

        return _involution(self.proposition)

    def maximum(self):
        """
        Recursively traverse proposition postorder (left->right->root) and check if disjunction and either left or right
        child is TrueProp then return TrueProp or if it's conjunction then return left if right is TrueProp or right if
        left is TrueProp.
        :param op: Proposition
        :return: Proposition
        """

        def _maximum(op):
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

        return _maximum(self.proposition)

    def minimum(self):
        """
        Recursively traverse proposition postorder (left->right->root) and check if conjunction and either left or right
        child is FalseProp then return FalseProp if it's disjunction then return left if right is FalseProp or right if
        left is FalseProp.
        :param op: Proposition
        :return: Proposition
        """

        def _minimum(op):
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

        return _minimum(self.proposition)

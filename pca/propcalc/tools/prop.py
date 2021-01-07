# @Author: GKarseras
# @Date:   17 Nov 2020 08:28

from abc import ABC, abstractmethod
from lark import Transformer

from operator import not_, and_, or_


class Proposition:

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    # def __or__(self, other):
    #     if all(isinstance(prop, (bool, TrueProp, FalseProp)) for prop in [self, other]):
    #         return self or other
    #     else:
    #         return DisjunctionOp(self, other)
    #
    # def __ror__(self, other):
    #     return self.__or__(other)
    #
    # def __ior__(self, other):
    #     return self.__or__(other)
    #
    # def __and__(self, other):
    #     if all(isinstance(prop, (bool, TrueProp, FalseProp)) for prop in [self, other]):
    #         return self and other
    #     else:
    #         return ConjunctionOp(self, other)
    #
    # def __rand__(self, other):
    #     return self.__and__(other)
    #
    # def __iand__(self, other):
    #     return self.__and__(other)
    #
    # def __invert__(self):
    #     if isinstance(self, (bool, TrueProp, FalseProp)):
    #         return not self
    #     return NegationOp(self)

    # def __inv__(self):
    #     return self.__invert__()
    #
    # def __not__(self):
    #     return self.__invert__()

    # def __xor__(self):


# class Variable(Proposition):
#
#     def __init__(self, name: str):
#         self.name = str(name)
#
#     def __repr__(self):
#         return f'{self.__class__.__name__}({repr(self.name)})'
#
#     def __eq__(self, other):
#         return isinstance(other, self.__class__) and self.name == other.name


class Operation(Proposition):

    @abstractmethod
    def eval(self):
        raise NotImplementedError


# class PropBool(Proposition):
#
#     def __init__(self, n):
#         self._n = n
#
#     def __repr__(self):
#         return str(self._n)
#
#     def __bool__(self) -> bool:
#         return bool(self._n)


class UnaryOp(Operation, ABC):

    def __init__(self, prop) -> None:
        self.prop = prop

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({repr(self.prop)})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.prop == other.prop


class BinaryOp(Operation):

    def __init__(self, op, prop_l, prop_r) -> None:
        self.op = op
        self.prop_l = prop_l
        self.prop_r = prop_r

    def __repr__(self) -> str:
        return self.__class__.__name__ + f'({repr(self.prop_l)}, {repr(self.prop_r)})'

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.prop_l == other.prop_l and self.prop_r == other.prop_r

    def eval(self):
        return get_binary_eval(self.op, self.prop_l, self.prop_r)


class NegationOp(UnaryOp):

    def eval(self):
        return not self.prop


class DisjunctionOp(BinaryOp):

    def __init__(self, prop_l, prop_r):
        super().__init__(DisjunctionOp, prop_l, prop_r)


class ConjunctionOp(BinaryOp):

    def __init__(self, prop_l, prop_r):
        super().__init__(ConjunctionOp, prop_l, prop_r)


class ImplicationOp(BinaryOp):

    def __init__(self, prop_l, prop_r):
        super().__init__(ImplicationOp, prop_l, prop_r)


class EquivalenceOp(BinaryOp):

    def __init__(self, prop_l, prop_r):
        super().__init__(EquivalenceOp, prop_l, prop_r)


class AtomTransformer(Transformer):

    def __init__(self, interp):
        super().__init__()
        self.interp = interp

    def exp_iff(self, value):
        return EquivalenceOp(value[0], value[2])

    def exp_imp(self, value):
        return ImplicationOp(value[0], value[2])

    def exp_or(self, value):
        return DisjunctionOp(value[0], value[2])

    def exp_and(self, value):
        return ConjunctionOp(value[0], value[2])

    def exp_not(self, value):
        return NegationOp(value[1])

    def atom_true(self, value):
        return True

    def atom_false(self, value):
        return False

    def atom_paren(self, value):
        return value[0]

    def atom_var(self, value):
        return self.interp[value[0]]


def get_binary_eval(op, left, right):
    return {
        ConjunctionOp: left and right,
        DisjunctionOp: left or right,
        ImplicationOp: (not left) or right,
        EquivalenceOp: (left or (not right)) and ((not left) or right)
    }[op]

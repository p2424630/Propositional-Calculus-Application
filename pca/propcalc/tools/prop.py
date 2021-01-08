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
    #         return TrueProp() if (self or other) else FalseProp()
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
    #         return TrueProp() if (self and other) else FalseProp()
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
    #         return TrueProp() if not self else FalseProp()
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


class Operation(Proposition, ABC):

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
#
#
# class TrueProp(PropBool):
#
#     def __init__(self):
#         super().__init__(True)
#
#
# class FalseProp(PropBool):
#
#     def __init__(self):
#         super().__init__(False)


class UnaryOp(Operation, ABC):

    def __init__(self, prop) -> None:
        self._prop = prop

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({repr(self._prop)})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._prop == other._prop

    @property
    def prop(self):
        return self._prop


class BinaryOp(Operation, ABC):

    def __init__(self, prop_l, prop_r) -> None:
        self._prop_l = prop_l
        self._prop_r = prop_r

    def __repr__(self) -> str:
        return self.__class__.__name__ + f'({repr(self._prop_l)}, {repr(self._prop_r)})'

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self._prop_l == other._prop_l and self._prop_r == other._prop_r

    @property
    def prop_l(self):
        return self._prop_l

    @property
    def prop_r(self):
        return self._prop_r


class NegationOp(UnaryOp):

    def eval(self) -> bool:
        return not self.prop


class DisjunctionOp(BinaryOp):

    def eval(self) -> bool:
        return self.prop_l or self.prop_r


class ConjunctionOp(BinaryOp):

    def eval(self) -> bool:
        return self.prop_l and self.prop_r


class ImplicationOp(BinaryOp):

    def eval(self) -> bool:
        return (not self.prop_l) or self.prop_r


class EquivalenceOp(BinaryOp):

    def eval(self) -> bool:
        return (self.prop_l or (not self.prop_r)) and ((not self.prop_l) or self.prop_r)


# TODO: Fix value unpacking.
class AtomTransformer(Transformer):

    def __init__(self, interp):
        super().__init__()
        self._interp = interp

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
        return self._interp[value[0]]

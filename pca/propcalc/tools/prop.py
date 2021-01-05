# @Author: GKarseras
# @Date:   17 Nov 2020 08:28

from abc import ABC, abstractmethod
from lark import Transformer


class Proposition:

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __or__(self, other):
        if isinstance(self, (bool, TrueProp, FalseProp)) and isinstance(other, (bool, TrueProp, FalseProp)):
            return self or other
        else:
            return DisjunctionOp(self, other)

    def __and__(self, other):
        if isinstance(self, (bool, TrueProp, FalseProp)) and isinstance(other, (bool, TrueProp, FalseProp)):
            print('inside')
            return self and other
        else:
            return ConjunctionOp(self, other)

    def __invert__(self):
        if isinstance(self, (bool, TrueProp, FalseProp)):
            return not self
        return NegationOp(self)


class Variable(Proposition):
    __slots__ = 'name'

    def __init__(self, name: str):
        self.name = str(name)

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.name)})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name


class Operation(Proposition):

    @abstractmethod
    def eval(self, *args):
        raise NotImplementedError


class TrueProp(Proposition):

    def __repr__(self) -> str:
        return 'true'

    def __bool__(self) -> bool:
        return True

    def eval(self) -> bool:
        return True


class FalseProp(Proposition):

    def __repr__(self) -> str:
        return 'false'

    def __bool__(self) -> bool:
        return False

    def eval(self) -> bool:
        return False


class UnaryOp(Operation, ABC):
    __slots__ = 'prop'

    def __init__(self, prop: Proposition) -> None:
        self.prop = prop

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({repr(self.prop)})'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.prop == other.prop


class BinaryOp(Operation, ABC):
    __slots__ = ('prop_l', 'prop_r')

    def __init__(self, prop_l: Proposition, prop_r: Proposition) -> None:
        self.prop_l = prop_l
        self.prop_r = prop_r

    def __repr__(self) -> str:
        return self.__class__.__name__ + f'({repr(self.prop_l)}, {repr(self.prop_r)})'

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.prop_l == other.prop_l and self.prop_r == other.prop_r


class NegationOp(UnaryOp):

    def eval(self):
        return ~ self.prop


class DisjunctionOp(BinaryOp):

    def eval(self):
        return self.prop_l | self.prop_r


class ConjunctionOp(BinaryOp):

    def eval(self):
        return self.prop_l & self.prop_r


class ImplicationOp(BinaryOp):

    def eval(self):
        return (~self.prop_l) | self.prop_r


class EquivalenceOp(BinaryOp):

    def eval(self):
        return (self.prop_l | (~self.prop_r)) & ((~self.prop_l) | self.prop_r)


class AtomTransformer(Transformer):

    def __init__(self, interp):
        super().__init__()
        self.interp = interp

    def start(self, value): return value

    def exp_iff(self, value): return EquivalenceOp(value[0], value[2])

    def exp_imp(self, value): return ImplicationOp(value[0], value[2])

    def exp_or(self, value): return DisjunctionOp(value[0], value[2])

    def exp_and(self, value): return ConjunctionOp(value[0], value[2])

    def exp_not(self, value): return NegationOp(value[1])

    def true(self, value): return TrueProp()

    def false(self, value): return FalseProp()

    def paren(self, value): return value[1]

    def var(self, value):
        return self.interp[value[0]]

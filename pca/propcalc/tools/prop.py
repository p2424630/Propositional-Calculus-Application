# @Author: GKarseras
# @Date:   17 Nov 2020 08:28

from abc import ABC, abstractmethod
from lark import Transformer
from operator import and_, inv, or_
from typing import Type, Union


class Proposition:

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __or__(self, other):
        if all(isinstance(prop, (bool, TrueProp, FalseProp)) for prop in [self, other]):
            return TrueProp() if (self or other) else FalseProp()
        else:
            return DisjunctionOp(self, other)

    def __ror__(self, other):
        return self.__or__(other)

    def __and__(self, other):
        if all(isinstance(prop, (bool, TrueProp, FalseProp)) for prop in [self, other]):
            return TrueProp() if (self and other) else FalseProp()
        else:
            return ConjunctionOp(self, other)

    def __rand__(self, other):
        return self.__and__(other)

    def __invert__(self):
        if isinstance(self, (bool, TrueProp, FalseProp)):
            return TrueProp() if (not self) else FalseProp()
        return NegationOp(self)


class Variable(Proposition):

    def __init__(self, name: str) -> None:
        self._name = str(name)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({repr(self._name)})'

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self._name == other._name

    @property
    def name(self):
        return self._name


class TrueProp(Proposition):

    def __repr__(self) -> str:
        return 'True'

    def __bool__(self) -> bool:
        return True


class FalseProp(Proposition):

    def __repr__(self) -> str:
        return 'False'

    def __bool__(self) -> bool:
        return False


class UnaryOp(Proposition):

    def __init__(self, prop) -> None:
        self._prop = prop

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({repr(self._prop)})'

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self._prop == other._prop

    @property
    def prop(self):
        return self._prop


class BinaryOp(Proposition):

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


class Operation(ABC):

    @abstractmethod
    def eval(self):
        raise NotImplementedError


class NegationOp(UnaryOp, Operation):

    def eval(self):
        return inv(self.prop)


class DisjunctionOp(BinaryOp, Operation):

    def eval(self):
        return or_(self.prop_l, self.prop_r)


class ConjunctionOp(BinaryOp, Operation):

    def eval(self):
        return and_(self.prop_l, self.prop_r)


class ImplicationOp(BinaryOp, Operation):

    def eval(self):
        return or_(inv(self.prop_l), self.prop_r)


class EquivalenceOp(BinaryOp, Operation):

    def eval(self):
        return and_(or_(self.prop_l, inv(self.prop_r)), or_(inv(self.prop_l), self.prop_r))


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
        return TrueProp()

    def atom_false(self, value):
        return FalseProp()

    def atom_paren(self, value):
        return value[0]

    def atom_var(self, value):
        return self._interp[value[0]]

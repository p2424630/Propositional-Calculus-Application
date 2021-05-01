# @Author: GKarseras
# @Date:   17 Nov 2020 08:28

from __future__ import annotations
from abc import ABC, abstractmethod

SYMBOLS = {
    'UNARY': 'UN_OP ',
    'BINARY': ' BI_OP ',
    'EQUIVALENCE': ' \u21D4 ',
    'IMPLICATION': ' \u21D2 ',
    'DISJUNCTION': ' \u2228 ',
    'CONJUNCTION': ' \u2227 ',
    'NEGATION': '\u00AC ',
    'TRUE': '\u22a4',
    'FALSE': '\u22A5'
}


class Proposition:
    """
    Base proposition class, overloads default bitwise operators
    + Disjunction
    * Conjunction
    ~ Negation
    >> Implication
    """

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__)

    def __add__(self, other):
        if all(isinstance(prop, (TrueProp, FalseProp)) for prop in [self, other]):
            if isinstance(self, TrueProp) or isinstance(other, TrueProp):
                return TrueProp()
            return FalseProp()
        return DisjunctionOp(self, other)

    def __radd__(self, other):
        return other.__or__(self)

    def __mul__(self, other):
        if all(isinstance(prop, (TrueProp, FalseProp)) for prop in [self, other]):
            if isinstance(self, FalseProp) or isinstance(other, FalseProp):
                return FalseProp()
            return TrueProp()
        return ConjunctionOp(self, other)

    def __rmul__(self, other):
        return other.__and__(self)

    def __invert__(self):
        if isinstance(self, TrueProp):
            return FalseProp()
        elif isinstance(self, FalseProp):
            return TrueProp()
        return NegationOp(self)

    def __rshift__(self, other):
        if all(isinstance(prop, (TrueProp, FalseProp)) for prop in [self, other]):
            return ~self + other
        return ImplicationOp(self, other)


class Variable(Proposition):

    def __init__(self, name: str) -> None:
        self._name = str(name)

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({repr(self._name)})'

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self._name == other.name

    def __lt__(self, other) -> bool:
        return self._name < other.name

    def __hash__(self) -> int:
        return hash(self._name)

    @property
    def name(self):
        return self._name


class TrueProp(Proposition):
    symbol = SYMBOLS['TRUE']

    def __str__(self) -> str:
        return self.symbol

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}'

    def __bool__(self) -> bool:
        return True


class FalseProp(Proposition):
    symbol = SYMBOLS['FALSE']

    def __str__(self) -> str:
        return self.symbol

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}'

    def __bool__(self) -> bool:
        return False


class UnaryOp(Proposition):
    symbol = SYMBOLS['UNARY']

    def __init__(self, prop) -> None:
        self._prop = prop

    def __str__(self):
        if isinstance(self._prop, UnaryOp):
            return f'{self.__class__.symbol}({str(self._prop)})'
        else:
            return f'{self.__class__.symbol}{str(self._prop)}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({repr(self._prop)})'

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self._prop == other._prop

    @property
    def prop(self):
        return self._prop


class BinaryOp(Proposition):
    symbol = SYMBOLS['BINARY']

    def __init__(self, prop_l, prop_r) -> None:
        self._prop_l = prop_l
        self._prop_r = prop_r

    def __str__(self):
        return f'({str(self._prop_l)}{self.__class__.symbol}{str(self._prop_r)})'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({repr(self._prop_l)}, {repr(self._prop_r)})'

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self._prop_l == other._prop_l and self._prop_r == other._prop_r

    @property
    def prop_l(self):
        return self._prop_l

    @property
    def prop_r(self):
        return self._prop_r


class Operation(ABC):
    """
    Interface for all operations to implement an evaluation method.
    """

    @abstractmethod
    def eval(self):
        raise NotImplementedError


class NegationOp(UnaryOp, Operation):
    symbol = SYMBOLS['NEGATION']

    def eval(self):
        return ~self.prop


class DisjunctionOp(BinaryOp, Operation):
    symbol = SYMBOLS['DISJUNCTION']

    def eval(self):
        return self.prop_l + self.prop_r


class ConjunctionOp(BinaryOp, Operation):
    symbol = SYMBOLS['CONJUNCTION']

    def eval(self):
        return self.prop_l * self.prop_r


class ImplicationOp(BinaryOp, Operation):
    symbol = SYMBOLS['IMPLICATION']

    def eval(self):
        return self.prop_l >> self.prop_r


class EquivalenceOp(BinaryOp, Operation):
    symbol = SYMBOLS['EQUIVALENCE']

    def eval(self):
        return (self.prop_l >> self.prop_r) * (self.prop_r >> self.prop_l)

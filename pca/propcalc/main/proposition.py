# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from __future__ import annotations
from typing import Tuple, Optional
# from dataclasses import dataclass
# from abc import ABC, abstractmethod

from pca.propcalc.tools.config import LogicSymbols


# @dataclass(frozen=True)
class Proposition:

    def __init__(self) -> None:
        self._value = False

    def __eq__(self, other: Proposition) -> bool:
        return self.value == other.value

    def __repr__(self) -> str:
        return f'{self._value}'

    @property
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, value: bool) -> None:
        self._value = value


class Operation(Proposition):

    def __init__(self, op: LogicSymbols = None) -> None:
        super().__init__()
        self.op = op


class UnaryOp(Operation):

    def __init__(self, op: LogicSymbols, prop: Proposition) -> None:
        super().__init__(op)
        self.prop = prop

    def __repr__(self) -> str:
        return f'{self.op} {self.prop.value}'


class BinaryOp(Operation):

    def __init__(self, op: LogicSymbols, prop_l: Proposition, prop_r: Proposition) -> None:
        super().__init__(op)
        self.prop_l = prop_l
        self.prop_r = prop_r

    def __repr__(self) -> str:
        return f'{self.prop_l.value} {self.op} {self.prop_r.value}'


class NegationOp(UnaryOp):

    def __init__(self, prop) -> None:
        super().__init__(LogicSymbols.NEGATION, prop)
        self.value = not self.prop.value


class DisjunctionOp(BinaryOp):

    def __init__(self, prop_l: Proposition, prop_r: Proposition) -> None:
        super().__init__(LogicSymbols.DISJUNCTION, prop_l, prop_r)
        self.value = self.prop_l.value or self.prop_r.value


class ConjunctionOp(BinaryOp):

    def __init__(self, prop_l: Proposition, prop_r: Proposition) -> None:
        super().__init__(LogicSymbols.CONJUNCTION, prop_l, prop_r)
        self.value = self.prop_l.value and self.prop_r.value


class ImplicationOp(BinaryOp):

    def __init__(self, prop_l: Proposition, prop_r: Proposition) -> None:
        super().__init__(LogicSymbols.IMPLICATION, prop_l, prop_r, )
        self.value = not self.prop_l.value or self.prop_r.value


class EquivalenceOp(BinaryOp):

    def __init__(self, prop_l: Proposition, prop_r: Proposition) -> None:
        super().__init__(LogicSymbols.EQUIVALENCE, prop_l, prop_r)
        self.value = (self.prop_l.value or not self.prop_r.value) and (not self.prop_l.value or self.prop_r.value)

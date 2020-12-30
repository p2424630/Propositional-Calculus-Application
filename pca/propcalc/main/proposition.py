# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Dict
from pca.propcalc.tools.config import LogicSymbols
from operator import or_


@dataclass(frozen=True)
class Proposition(ABC):

    # TODO: Structurally equivalence
    # def __eq__(self, other: Proposition) -> bool:
    #     return self.value == other.value

    @abstractmethod
    def eval(self):
        raise NotImplementedError


class Variable(Proposition, ABC):
    pass


class Operation(Proposition, ABC):
    pass


class UnaryOp(Operation, ABC):

    def __repr__(self):
        return f'{self.op} {self.prop.value}'


class BinaryOp(Operation, ABC):

    def __repr__(self) -> str:
        return f'{self.prop_l.value} {self.op} {self.prop_r.value}'


class NegationOp(UnaryOp):

    def eval(self, to_eval: Dict):
        return not eval(self.prop)


class DisjunctionOp(BinaryOp):

    def __init__(self, prop_l: Proposition, prop_r: Proposition) -> None:
        super().__init__(LogicSymbols.DISJUNCTION, prop_l, prop_r)
        # self.value = self.prop_l.value or self.prop_r.value


class ConjunctionOp(BinaryOp):

    def __init__(self, prop_l: Proposition, prop_r: Proposition) -> None:
        super().__init__(LogicSymbols.CONJUNCTION, prop_l, prop_r)
        # self.value = self.prop_l.value and self.prop_r.value


class ImplicationOp(BinaryOp):

    def __init__(self, prop_l: Proposition, prop_r: Proposition) -> None:
        super().__init__(LogicSymbols.IMPLICATION, prop_l, prop_r, )
        # self.value = not self.prop_l.value or self.prop_r.value


class EquivalenceOp(BinaryOp):

    def __init__(self, prop_l: Proposition, prop_r: Proposition) -> None:
        super().__init__(LogicSymbols.EQUIVALENCE, prop_l, prop_r)
        # self.value = (self.prop_l.value or not self.prop_r.value) and (not self.prop_l.value or self.prop_r.value)


class TrueProp(Proposition):

    def eval(self):
        return True

    def __repr__(self) -> str:
        return f'{self.eval()}'


class FalseProp(Proposition):

    def eval(self):
        return False

    def __repr__(self) -> str:
        return f'{self.eval()}'

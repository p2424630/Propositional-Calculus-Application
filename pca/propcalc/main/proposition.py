# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from itertools import permutations
from typing import Dict
from pca.propcalc.tools.config import LogicSymbols, PARSER


# @dataclass(frozen=True)
class Proposition(ABC):

    def __init__(self, prop):
        self.parsed = PARSER.parse(prop)
        pass

    # TODO: Structurally equivalence
    # def __eq__(self, other: Proposition) -> bool:
    #     return self.value == other.value

    # @abstractmethod
    def eval(self, prop_l: Proposition, prop_r: Proposition, to_eval: list):
        raise NotImplementedError


# def satisfiable(prop: Proposition):
#     return any(permutations{True, False} Proposition == True)
#
#
# def tautology(prop: Proposition):
#     return all(permutations{True, False} Proposition == True)
#
#
# def contradiction(prop: Proposition):
#     return all(permutations{True, False} Proposition == False)


class Variable(Proposition, ABC):
    pass


class Operation(Proposition, ABC):
    pass


class UnaryOp(Operation):

    def __repr__(self):
        return f'{self.op} {self.prop.value}'

    def eval(self, prop_l: Proposition, prop_r: None, to_eval: bool):
        raise NotImplementedError


class BinaryOp(Operation, ABC):

    def __repr__(self) -> str:
        return f'{self.prop_l.value} {self.op} {self.prop_r.value}'


class NegationOp(UnaryOp):

    def eval(self, prop_l: Proposition, prop_r: None, to_eval: bool):
        return not prop_l


class DisjunctionOp(BinaryOp):

    def __init__(self, prop_l: Proposition, prop_r: Proposition, to_eval=None) -> None:
        self.eval(prop_l, prop_r, to_eval)

    def eval(self, prop_l, prop_r, to_eval):
         return prop_l or prop_r


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

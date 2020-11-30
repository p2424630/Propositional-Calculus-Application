# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from pca.propcalc.calctools.tree import Node

from dataclasses import dataclass
from abc import ABC, abstractmethod


# @dataclass(frozen=True)
class Proposition:

    def __eq__(self, other) -> bool:
        return self.__repr__() == other.__repr__()

    def __repr__(self) -> str:
        return str(self)


class Operation(Proposition):

    def __init__(self) -> None:
        super().__init__()


class UnaryOp(Operation):
    raise NotImplementedError


class BinaryOp(Operation):
    raise NotImplementedError


class Negation(UnaryOp):
    raise NotImplementedError


class ImplicationOp(BinaryOp):
    raise NotImplementedError


class ConjunctionOp(BinaryOp):
    raise NotImplementedError


class DisjunctionOp(BinaryOp):
    raise NotImplementedError


class EquivalenceOp(BinaryOp):
    raise NotImplementedError

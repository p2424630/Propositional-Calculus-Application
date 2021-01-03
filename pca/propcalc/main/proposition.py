# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from itertools import permutations
from typing import Dict

'''
Predicates are functions of zero or more variables that return Boolean values. 
Thus predicates can be true sometimes and false sometimes, depending on the values of their arguments
'''


# @dataclass(frozen=True)
class Proposition:
    pass

    # TODO: Structurally equivalence
    # def __eq__(self, other: Proposition) -> bool:
    #     return self.value == other.value


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


class Variable(Proposition):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.__class__.__name__ + '("' + self.name + '")'

    pass


class Operation(Proposition):
    pass


class UnaryOp(Operation):

    def __init__(self, elem):
        self.elem = elem

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.elem) + ")"

    @abstractmethod
    def eval(self):
        raise NotImplementedError

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.elem == other.elem


class BinaryOp(Operation):

    def __init__(self, *elems):
        self.elems = elems

    def __repr__(self):
        return self.__class__.__name__ + "(" + ", ".join((repr(x) for x in self.elems)) + ")"

    @abstractmethod
    def eval(self, prop_l: Proposition, prop_r: Proposition):
        raise NotImplementedError


class NegationOp(UnaryOp):

    def eval(self):
        return not self


class DisjunctionOp(BinaryOp):

    def eval(self, prop_l: Proposition, prop_r: Proposition):
        return prop_l or prop_r


class ConjunctionOp(BinaryOp):

    def eval(self, prop_l: Proposition, prop_r: Proposition):
        return prop_l and prop_r


class ImplicationOp(BinaryOp):

    def eval(self, prop_l: Proposition, prop_r: Proposition):
        return not prop_l or prop_r


class EquivalenceOp(BinaryOp):

    def eval(self, prop_l: Proposition, prop_r: Proposition):
        return (prop_l or not prop_r) and (not prop_l or prop_r)


class TrueProp(Proposition):

    def eval(self):
        return True

    def __repr__(self) -> str:
        return 'true'

    def __bool__(self):
        return True


class FalseProp(Proposition):

    def eval(self):
        return False

    def __repr__(self) -> str:
        return 'false'

    def __bool__(self):
        return False

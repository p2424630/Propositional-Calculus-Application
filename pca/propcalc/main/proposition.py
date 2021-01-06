# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from __future__ import annotations
from itertools import product

from lark import Token
import numpy as np

from pca.propcalc.tools.prop import AtomTransformer, TrueProp, FalseProp
from pca.propcalc.tools.parser import PARSER, SimpleTransformer


class InitProp:
    __slots__ = ('_prop', '_parsed')

    def __init__(self, prop: str):
        self._prop = prop
        self._parsed = PARSER.parse(prop)

    def truth(self, max_vars: int = 5):
        tr = SimpleTransformer()
        tr.transform(self._parsed)
        prop_vars = tr.prop_vars
        vars_len = len(prop_vars)
        if vars_len < 1:
            raise ValueError('Number of variables must be at least 1')
        if vars_len > max_vars:
            raise ValueError(f'Variable length {vars_len} exceeded the allowed {max_vars}')
        combs = list(product([FalseProp(), TrueProp()], repeat=vars_len))
        all_interp = []
        for comb in combs:
            interp = dict(zip(prop_vars, comb))
            interp_prop = AtomTransformer(interp).transform(self._parsed)
            all_interp.append(interp_prop)

    def satisfiable(self):
        # return any(permutations{True, False} Proposition == True)
        pass

    def tautology(self):
        # return all(permutations{True, False} Proposition == True)
        pass

    def contradiction(self):
        # return all(permutations{True, False} Proposition == False)
        pass

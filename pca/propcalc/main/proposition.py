# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from __future__ import annotations
from itertools import product

from pca.propcalc.tools.prop import AtomTransformer, TrueProp, FalseProp, NegationOp, get_ev
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
            all_interp.append(eval_prop(interp_prop))

    def satisfiable(self):
        # return any(permutations{True, False} Proposition == True)
        pass

    def tautology(self):
        # return all(permutations{True, False} Proposition == True)
        pass

    def contradiction(self):
        # return all(permutations{True, False} Proposition == False)
        pass


def eval_prop(op):
    if isinstance(op, (bool, TrueProp, FalseProp)):
        return op
    if isinstance(op, NegationOp):
        if isinstance(op.prop, (bool, TrueProp, FalseProp)):
            return op.eval()
        return not eval_prop(op.prop)
    if all(isinstance(prop, (bool, TrueProp, FalseProp)) for prop in [op.prop_l, op.prop_r]):
        return op.eval()
    if isinstance(op.prop_l, (bool, TrueProp, FalseProp)):
        return get_ev(op.prop_l, eval_prop(op.prop_r))[op.__class__]
    if isinstance(op.prop_r, (bool, TrueProp, FalseProp)):
        return get_ev(eval_prop(op.prop_l), op.prop_r)[op.__class__]
    return get_ev(eval_prop(op.prop_l), eval_prop(op.prop_r))[op.__class__]

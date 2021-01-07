# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from __future__ import annotations
from itertools import product

from pca.propcalc.tools.prop import AtomTransformer, TrueProp, FalseProp, NegationOp, get_binary_eval, get_unary_eval
from pca.propcalc.tools.parser import PARSER, SimpleTransformer


class InitProp:
    __slots__ = ('_prop', '_parsed')

    def __init__(self, prop: str):
        self._prop = prop
        self._parsed = PARSER.parse(prop)

    def get_vars(self):
        tr = SimpleTransformer()
        tr.transform(self._parsed)
        return tr.prop_vars

    def build_interp(self, max_vars: int = 5):
        prop_vars = self.get_vars()
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
        return all_interp

    # TODO: Implement better & faster SAT solver.
    def satisfiable(self):
        return any(self.build_interp())

    def tautology(self):
        return all(self.build_interp())

    def contradiction(self):
        return not any(self.build_interp())


def eval_prop(op):
    if isinstance(op, (bool, TrueProp, FalseProp)):
        return op
    if isinstance(op, NegationOp):
        if isinstance(op.prop, (bool, TrueProp, FalseProp)):
            return get_unary_eval(op.__class__, op.eval())
        return not eval_prop(op.prop)
    if all(isinstance(prop, (bool, TrueProp, FalseProp)) for prop in [op.prop_l, op.prop_r]):
        return op.eval()
    if isinstance(op.prop_l, (bool, TrueProp, FalseProp)):
        return get_binary_eval(op.__class__, op.prop_l, eval_prop(op.prop_r))
    if isinstance(op.prop_r, (bool, TrueProp, FalseProp)):
        return get_binary_eval(op.__class__, eval_prop(op.prop_l), op.prop_r)
    return get_binary_eval(op.__class__, eval_prop(op.prop_l), eval_prop(op.prop_r))

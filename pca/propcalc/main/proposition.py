# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from __future__ import annotations
from itertools import product

from pca.propcalc.tools.prop import AtomTransformer, NegationOp
from pca.propcalc.tools.parser import PARSER, VarsVisitor


class InitProp:
    __slots__ = ('_prop', '_parsed')

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._parsed == other._parsed

    def __init__(self, prop: str) -> None:
        self._prop = prop
        self._parsed = PARSER.parse(prop)

    def _get_vars(self):
        tr = VarsVisitor()
        tr.visit(self._parsed)
        return sorted(tr.prop_vars)

    def _get_combs(self, max_vars):
        prop_vars = self._get_vars()
        vars_len = len(prop_vars)
        if vars_len < 1:
            raise ValueError('Number of variables must be at least 1')
        if vars_len > max_vars:
            raise ValueError(f'Variable length {vars_len} exceeded the allowed {max_vars}')
        return list(product([False, True], repeat=vars_len))

    def build_interp(self, max_vars: int = 5):
        combs = self._get_combs(max_vars)
        all_interp = []
        for comb in combs:
            interp = dict(zip(self._get_vars(), comb))
            interp_prop = AtomTransformer(interp).transform(self._parsed)
            all_interp.append((interp, eval_prop(interp_prop)))
        return all_interp

    # TODO: Implement better SAT solver.
    def satisfiable(self):
        for i in self.build_interp():
            for j in i:
                if isinstance(j, bool) and j:
                    return True
        return False

    def tautology(self):
        for i in self.build_interp():
            for j in i:
                if isinstance(j, bool) and not j:
                    return False
        return True

    def contradiction(self):
        return not self.satisfiable()

    def cnf(self):
        raise NotImplementedError

    def dnf(self):
        raise NotImplementedError


def eval_prop(op):
    if isinstance(op, bool):
        return op
    if isinstance(op, NegationOp):
        if isinstance(op.prop, bool):
            return op.eval()
        return not eval_prop(op.prop)
    if all(isinstance(prop, bool) for prop in [op.prop_l, op.prop_r]):
        return op.eval()
    if isinstance(op.prop_l, bool):
        return op.__class__(op.prop_l, eval_prop(op.prop_r)).eval()
    if isinstance(op.prop_r, bool):
        return op.__class__(eval_prop(op.prop_l), op.prop_r).eval()
    return op.__class__(eval_prop(op.prop_l), eval_prop(op.prop_r)).eval()

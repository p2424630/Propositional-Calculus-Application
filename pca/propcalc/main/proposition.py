# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from __future__ import annotations
from typing import Iterator, List, Set, Dict, Tuple
from itertools import product
from lark import Visitor

from pca.propcalc.tools.prop import AtomTransformer, ConjunctionOp, DisjunctionOp, EquivalenceOp, FalseProp
from pca.propcalc.tools.prop import ImplicationOp, NegationOp, TrueProp
from pca.propcalc.tools.parser import PARSER


class InitProp:
    __slots__ = ('_prop', '_parsed')

    def __init__(self, prop: str) -> None:
        self._prop = prop
        self._parsed = PARSER.parse(prop)

    def __eq__(self, other) -> bool:
        """
        Structural equivalence - works with exact locations (parenthesis are taken into account).
        'A or B' != 'B or A'
        'A or B' != '(A or B)'
        :param other:
        :return: bool
        """
        return isinstance(other, self.__class__) and self._parsed == other._parsed

    def _get_vars(self) -> List[str]:
        tr = VarsVisitor()
        tr.visit(self._parsed)
        return sorted(tr.prop_vars)

    def _get_combs(self, max_vars) -> Iterator[Tuple[bool, ...]]:
        prop_vars = self._get_vars()
        vars_len = len(prop_vars)
        if vars_len < 1:
            raise ValueError('Number of variables must be at least 1')
        if vars_len > max_vars:
            raise ValueError(f'Variable length {vars_len}, exceeded the allowed {max_vars}')
        return product([FalseProp(), TrueProp()], repeat=vars_len)

    def build_interp(self, max_vars: int = 5) -> List[Tuple[Dict[str, bool], bool]]:
        prop_vars = self._get_vars()
        all_interp = []
        for comb in self._get_combs(max_vars):
            interp = dict(zip(prop_vars, comb))
            interp_prop = AtomTransformer(interp).transform(self._parsed)
            all_interp.append((interp, eval_prop(interp_prop)))
        return all_interp

    # TODO: Implement better SAT solver.
    def satisfiable(self) -> bool:
        for i in self.build_interp():
            for j in i:
                if isinstance(j, (bool, TrueProp, FalseProp)) and j:
                    return True
        return False

    def tautology(self) -> bool:
        for i in self.build_interp():
            for j in i:
                if isinstance(j, (bool, TrueProp, FalseProp)) and not j:
                    return False
        return True

    def contradiction(self) -> bool:
        return not self.satisfiable()

    def cnf(self):
        raise NotImplementedError

    def dnf(self):
        raise NotImplementedError


def eval_prop(op):
    if isinstance(op, (bool, TrueProp, FalseProp)):
        return op
    elif isinstance(op, NegationOp):
        if isinstance(op.prop, (bool, TrueProp, FalseProp)):
            return op.eval()
        return op.__class__(eval_prop(op.prop)).eval()
    elif isinstance(op, (DisjunctionOp, ConjunctionOp, ImplicationOp, EquivalenceOp)):
        if all(isinstance(prop, (bool, TrueProp, FalseProp)) for prop in [op.prop_l, op.prop_r]):
            return op.eval()
        if isinstance(op.prop_l, (bool, TrueProp, FalseProp)):
            return op.__class__(op.prop_l, eval_prop(op.prop_r)).eval()
        if isinstance(op.prop_r, (bool, TrueProp, FalseProp)):
            return op.__class__(eval_prop(op.prop_l), op.prop_r).eval()
        return op.__class__(eval_prop(op.prop_l), eval_prop(op.prop_r)).eval()
    else:
        raise TypeError({type(op)})


class VarsVisitor(Visitor):

    def __init__(self):
        super().__init__()
        self._prop_vars = set()

    def atom_var(self, tree):
        assert tree.data == 'atom_var'
        self._prop_vars.add(tree.children[0].value)

    @property
    def prop_vars(self):
        return self._prop_vars

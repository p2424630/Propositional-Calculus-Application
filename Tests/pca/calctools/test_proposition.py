# @Author: GKarseras
# @Date:   15 Nov 2020 11:15
from copy import deepcopy

from pca.propcalc.main.proposition import *

import pytest


class TestProposition:

    def test_simple(self, simple_propositions):
        a, b = simple_propositions
        c = NegationOp(a)
        d = deepcopy(b)
        d.value = True
        assert not a.value
        assert c.value
        assert not DisjunctionOp(a, b).eval()
        assert DisjunctionOp(c, a).value
        assert not ConjunctionOp(c, a).value
        assert ConjunctionOp(c, d).value
        assert not ImplicationOp(c, a).value
        assert ImplicationOp(a, d).value
        assert not EquivalenceOp(d, a).value
        assert EquivalenceOp(c, d).value

    def test_chaining(self, simple_propositions):
        a, b = simple_propositions
        a.value = True
        res = DisjunctionOp(ConjunctionOp(a, b), a)
        assert res.value
        res = EquivalenceOp(DisjunctionOp(ConjunctionOp(a, b), a), DisjunctionOp(ConjunctionOp(a, b), a))
        assert res.value
        res = ConjunctionOp(DisjunctionOp(a, b), ImplicationOp(a, DisjunctionOp(NegationOp(a), b)))
        assert not res.value

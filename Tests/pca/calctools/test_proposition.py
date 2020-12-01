# @Author: GKarseras
# @Date:   15 Nov 2020 11:15

from pca.propcalc.main.proposition import *

import pytest


class TestProposition:

    def test_simple_negation(self):
        a = Proposition()
        assert not a.value
        assert NegationOp(a).value

    def test_chaining(self, simple_propositions):
        a, b = simple_propositions
        a.value = True
        res = DisjunctionOp(ConjunctionOp(a, b), a).value
        assert res
        res = ConjunctionOp(DisjunctionOp(a, b), b).value
        assert not res

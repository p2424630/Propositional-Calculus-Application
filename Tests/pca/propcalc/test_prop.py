# @Author: GKarseras
# @Date:   15 Nov 2020 11:36

from copy import deepcopy
import pytest


from pca.propcalc.tools.prop import ConjunctionOp, DisjunctionOp, EquivalenceOp, ImplicationOp
from pca.propcalc.tools.prop import NegationOp, AtomTransformer


class TestProp:

    def test_prop(self):
        a = True
        b = NegationOp(a)
        assert a
        assert not b.eval()
        assert DisjunctionOp(a, b.eval()).eval()
        assert not ConjunctionOp(b.eval(), a).eval()

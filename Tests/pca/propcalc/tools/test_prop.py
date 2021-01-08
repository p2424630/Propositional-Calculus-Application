# @Author: GKarseras
# @Date:   15 Nov 2020 11:36

from copy import deepcopy
import pytest


from pca.propcalc.tools.prop import AtomTransformer, ConjunctionOp, DisjunctionOp, EquivalenceOp, FalseProp
from pca.propcalc.tools.prop import ImplicationOp, NegationOp, TrueProp


class TestProp:

    def test_prop(self):
        a = TrueProp()
        b = NegationOp(a)
        assert a
        assert not b.eval()
        assert DisjunctionOp(a, b.eval()).eval()
        assert not ConjunctionOp(b.eval(), a).eval()

# @Author: GKarseras
# @Date:   15 Nov 2020 11:15

from pca.propcalc.main.proposition import InitProp, eval_prop
from pca.propcalc.tools.prop import ConjunctionOp, DisjunctionOp, EquivalenceOp, FalseProp, ImplicationOp
from pca.propcalc.tools.prop import NegationOp, TrueProp, Variable, AtomTransformer


# TODO: Mock the parser results if possible.
class TestProposition:

    def test_simple_props(self):
        a = InitProp('A')
        to_test = [FalseProp(), TrueProp()]
        assert a.build_interp() == to_test

        a = InitProp('A or B')
        to_test = [FalseProp(), TrueProp(), TrueProp(), TrueProp()]
        assert a.build_interp() == to_test

        a = InitProp('A and B')
        to_test = [FalseProp(), FalseProp(), FalseProp(), TrueProp()]
        assert a.build_interp() == to_test

    def test_sat_taut_contr(self):
        a = InitProp('A')
        assert a.satisfiable()
        assert not a.tautology()
        assert not a.contradiction()


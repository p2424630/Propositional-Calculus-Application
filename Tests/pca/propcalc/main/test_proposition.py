# @Author: GKarseras
# @Date:   15 Nov 2020 11:15

from pca.propcalc.main.proposition import InitProp, TrueProp, FalseProp
import pytest


class TestProposition:

    def test_simple_props(self):
        to_test = [({'A': FalseProp()}, FalseProp()), ({'A': TrueProp()}, TrueProp())]
        assert InitProp('A').build_interp() == to_test
        to_test = [({'A': FalseProp()}, TrueProp()), ({'A': TrueProp()}, FalseProp())]
        assert InitProp('not (not (not A))').build_interp() == to_test

    def test_disjunction(self):
        to_test = [({'A': FalseProp(), 'B': FalseProp()}, FalseProp()),
                   ({'A': FalseProp(), 'B': TrueProp()}, TrueProp()),
                   ({'A': TrueProp(), 'B': FalseProp()}, TrueProp()),
                   ({'A': TrueProp(), 'B': TrueProp()}, TrueProp())]
        assert InitProp('A or B').build_interp() == to_test
        to_test = [({'A': FalseProp()}, TrueProp()),
                   ({'A': TrueProp()}, TrueProp())]
        assert InitProp('A or true').build_interp() == to_test

    def test_conjunction(self):
        to_test = [({'A': FalseProp(), 'B': FalseProp()}, FalseProp()),
                   ({'A': FalseProp(), 'B': TrueProp()}, FalseProp()),
                   ({'A': TrueProp(), 'B': FalseProp()}, FalseProp()),
                   ({'A': TrueProp(), 'B': TrueProp()}, TrueProp())]
        assert InitProp('A and B').build_interp() == to_test
        to_test = [({'A': FalseProp()}, FalseProp()),
                   ({'A': TrueProp()}, TrueProp())]
        assert InitProp('A and true').build_interp() == to_test

    def test_sat(self):
        assert InitProp('A').satisfiable()
        assert not InitProp('A and not A').satisfiable()

    def test_taut(self):
        assert not InitProp('A').tautology()
        assert not InitProp('A or B').tautology()
        # Excluded middle
        assert InitProp('A or not A').tautology()
        assert not InitProp('A and B implies C').tautology()
        # Contraposition
        assert InitProp('(A implies B) iff (not B implies not A)').tautology()
        # proof by exh
        assert InitProp('(((A or B) and (A implies C)) and (B implies C)) implies C').tautology()

    def test_contr(self, propositions):
        assert not InitProp('A').contradiction()
        assert InitProp('A and not A').contradiction()
        assert not propositions['de_morgan'].contradiction()

    def test_distributivity(self):
        assert InitProp('A ∨ (B ∧ C)').build_interp() == InitProp('(A ∨ B) ∧ (A ∨ C)').build_interp()

    def test_de_morgan(self, propositions):
        assert InitProp('not(A or B)').build_interp() == InitProp('(not A) and (not B)').build_interp()
        assert propositions['de_morgan'].tautology()
        assert InitProp('(not(A or B)) ⇔ ((not A) and (not B))').tautology()

    def test_dijkstra_rule(self):
        assert InitProp('(((A ∧ B) ⇔ A) ⇔ B) ⇔ (A ∨ B)').tautology()

    def test_contrapositive(self):
        assert InitProp('C ⇒ (A ∧ B)').build_interp() == InitProp('(C ⇒ A) ∧ (C ⇒ B)').build_interp()

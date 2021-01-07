# @Author: GKarseras
# @Date:   15 Nov 2020 11:15

from pca.propcalc.main.proposition import InitProp
import pytest


# TODO: Implement mock results.
class TestProposition:

    def test_simple_props(self):
        to_test = [({'A': False}, False), ({'A': True}, True)]
        assert InitProp('A').build_interp() == to_test

    def test_disjunction(self):
        to_test = [({'A': False, 'B': False}, False),
                   ({'A': False, 'B': True}, True),
                   ({'A': True, 'B': False}, True),
                   ({'A': True, 'B': True}, True)]
        assert InitProp('A or B').build_interp() == to_test

    def test_conjunction(self):
        to_test = [({'A': False, 'B': False}, False),
                   ({'A': False, 'B': True}, False),
                   ({'A': True, 'B': False}, False),
                   ({'A': True, 'B': True}, True)]
        assert InitProp('A and B').build_interp() == to_test

    def test_sat(self):
        assert InitProp('A').satisfiable()
        assert not InitProp('A and not A').satisfiable()

    def test_taut(self):
        assert not InitProp('A').tautology()
        assert not InitProp('A or A').tautology()
        assert InitProp('A or not A').tautology()
        assert not InitProp('A and B implies C').tautology()
        assert InitProp('(A implies B) iff (not B implies not A)').tautology()
        assert InitProp('(((A or B) and (A implies C)) and (B implies C)) implies C').tautology()

    def test_contr(self, propositions):
        assert not InitProp('A').contradiction()
        assert InitProp('A and not A').contradiction()
        assert not propositions['de_morgan'].contradiction()

    def test_distributivity(self):
        assert InitProp('A ∨ (B ∧ C)').build_interp() == InitProp('(A ∨ B) ∧ (A ∨ C)').build_interp()

    def test_de_morgan(self, propositions):
        assert propositions['de_morgan'].tautology()
        assert InitProp('(not(A or B)) ⇔ ((not A) and (not B))').tautology()

    def test_dijkstra_rule(self):
        assert InitProp('(((A ∧ B) ⇔ A) ⇔ B) ⇔ (A ∨ B)').tautology()

    def test_contrapositive(self):
        assert InitProp('C ⇒ (A ∧ B)').build_interp() == InitProp('(C ⇒ A) ∧ (C ⇒ B)').build_interp()


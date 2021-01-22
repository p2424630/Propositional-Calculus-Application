import unittest

from pca.propcalc.prop_builder import InitProp, TrueProp, FalseProp, Variable


class TestInitProp(unittest.TestCase):

    def setUp(self) -> None:
        return

    def test_structural_equality(self):
        self.assertEqual(InitProp('A or B'), InitProp('(A or B)'))
        self.assertNotEqual(InitProp('A or B'), InitProp('B or A'))

    def test_simple_props(self):
        to_test = [({Variable('A'): FalseProp()}, FalseProp()), ({Variable('A'): TrueProp()}, TrueProp())]
        self.assertEqual(InitProp('A').build_interp(), to_test)
        to_test = [({Variable('A'): FalseProp()}, TrueProp()), ({Variable('A'): TrueProp()}, FalseProp())]
        self.assertEqual(InitProp('not (not (not A))').build_interp(), to_test)

    def test_disjunction(self):
        to_test = [({Variable('A'): FalseProp(), Variable('B'): FalseProp()}, FalseProp()),
                   ({Variable('A'): FalseProp(), Variable('B'): TrueProp()}, TrueProp()),
                   ({Variable('A'): TrueProp(), Variable('B'): FalseProp()}, TrueProp()),
                   ({Variable('A'): TrueProp(), Variable('B'): TrueProp()}, TrueProp())]
        self.assertEqual(InitProp('A or B').build_interp(), to_test)
        to_test = [({Variable('A'): FalseProp()}, TrueProp()),
                   ({Variable('A'): TrueProp()}, TrueProp())]
        self.assertEqual(InitProp('A or true').build_interp(), to_test)

    def test_conjunction(self):
        to_test = [({Variable('A'): FalseProp(), Variable('B'): FalseProp()}, FalseProp()),
                   ({Variable('A'): FalseProp(), Variable('B'): TrueProp()}, FalseProp()),
                   ({Variable('A'): TrueProp(), Variable('B'): FalseProp()}, FalseProp()),
                   ({Variable('A'): TrueProp(), Variable('B'): TrueProp()}, TrueProp())]
        self.assertEqual(InitProp('A and B').build_interp(), to_test)
        to_test = [({Variable('A'): FalseProp()}, FalseProp()),
                   ({Variable('A'): TrueProp()}, TrueProp())]
        self.assertEqual(InitProp('A and true').build_interp(), to_test)

    def test_comb(self):
        to_test = [({Variable('A'): FalseProp(), Variable('B'): FalseProp(), Variable('C'): FalseProp(),
                     Variable('D'): FalseProp()}, TrueProp()),
                   ({Variable('A'): FalseProp(), Variable('B'): FalseProp(), Variable('C'): FalseProp(),
                     Variable('D'): TrueProp()}, TrueProp()),
                   ({Variable('A'): FalseProp(), Variable('B'): FalseProp(), Variable('C'): TrueProp(),
                     Variable('D'): FalseProp()}, FalseProp()),
                   ({Variable('A'): FalseProp(), Variable('B'): FalseProp(), Variable('C'): TrueProp(),
                     Variable('D'): TrueProp()}, FalseProp()),
                   ({Variable('A'): FalseProp(), Variable('B'): TrueProp(), Variable('C'): FalseProp(),
                     Variable('D'): FalseProp()}, TrueProp()),
                   ({Variable('A'): FalseProp(), Variable('B'): TrueProp(), Variable('C'): FalseProp(),
                     Variable('D'): TrueProp()}, TrueProp()),
                   ({Variable('A'): FalseProp(), Variable('B'): TrueProp(), Variable('C'): TrueProp(),
                     Variable('D'): FalseProp()}, FalseProp()),
                   ({Variable('A'): FalseProp(), Variable('B'): TrueProp(), Variable('C'): TrueProp(),
                     Variable('D'): TrueProp()}, FalseProp()),
                   ({Variable('A'): TrueProp(), Variable('B'): FalseProp(), Variable('C'): FalseProp(),
                     Variable('D'): FalseProp()}, FalseProp()),
                   ({Variable('A'): TrueProp(), Variable('B'): FalseProp(), Variable('C'): FalseProp(),
                     Variable('D'): TrueProp()}, FalseProp()),
                   ({Variable('A'): TrueProp(), Variable('B'): FalseProp(), Variable('C'): TrueProp(),
                     Variable('D'): FalseProp()}, TrueProp()),
                   ({Variable('A'): TrueProp(), Variable('B'): FalseProp(), Variable('C'): TrueProp(),
                     Variable('D'): TrueProp()}, FalseProp()),
                   ({Variable('A'): TrueProp(), Variable('B'): TrueProp(), Variable('C'): FalseProp(),
                     Variable('D'): FalseProp()}, TrueProp()),
                   ({Variable('A'): TrueProp(), Variable('B'): TrueProp(), Variable('C'): FalseProp(),
                     Variable('D'): TrueProp()}, TrueProp()),
                   ({Variable('A'): TrueProp(), Variable('B'): TrueProp(), Variable('C'): TrueProp(),
                     Variable('D'): FalseProp()}, FalseProp()),
                   ({Variable('A'): TrueProp(), Variable('B'): TrueProp(), Variable('C'): TrueProp(),
                     Variable('D'): TrueProp()}, TrueProp())]
        self.assertEqual(InitProp('A and D or not C iff A implies B').build_interp(), to_test)

    def test_sat(self):
        self.assertTrue(InitProp('A').satisfiable())
        self.assertFalse(InitProp('A and not A').satisfiable())

    def test_taut(self):
        self.assertFalse(InitProp('A').tautology())
        self.assertFalse(InitProp('A or B').tautology())
        # Excluded middle
        self.assertTrue(InitProp('A or not A').tautology())
        self.assertFalse(InitProp('A and B implies C').tautology())
        # Contraposition
        self.assertTrue(InitProp('(A implies B) iff (not B implies not A)').tautology())
        # proof by exh
        self.assertTrue(InitProp('(((A or B) and (A implies C)) and (B implies C)) implies C').tautology())

    def test_contr(self):
        self.assertFalse(InitProp('A').contradiction())
        self.assertTrue(InitProp('A and not A').contradiction())
        self.assertFalse(InitProp('(not(A and B)) ⇔ ((not A) or (not B))').contradiction())

    def test_distributivity(self):
        self.assertEqual(InitProp('A ∨ (B ∧ C)').build_interp(), InitProp('(A ∨ B) ∧ (A ∨ C)').build_interp())

    def test_de_morgan(self):
        self.assertEqual(InitProp('not(A or B)').build_interp(), InitProp('(not A) and (not B)').build_interp())
        self.assertTrue(InitProp('(not(A and B)) ⇔ ((not A) or (not B))').tautology())
        self.assertTrue(InitProp('(not(A or B)) ⇔ ((not A) and (not B))').tautology())

    def test_dijkstra_rule(self):
        self.assertTrue(InitProp('(((A ∧ B) ⇔ A) ⇔ B) ⇔ (A ∨ B)').tautology())

    def test_contrapositive(self):
        self.assertEqual(InitProp('C ⇒ (A ∧ B)').build_interp(), InitProp('(C ⇒ A) ∧ (C ⇒ B)').build_interp())


if __name__ == '__main__':
    unittest.main()

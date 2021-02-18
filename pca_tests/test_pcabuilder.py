import unittest

from pca_main import pcabuilder, pcaprop


class TestInitProp(unittest.TestCase):

    def setUp(self) -> None:
        return

    def test_structural_equality(self):
        self.assertEqual(pcabuilder.InitProp('A or B'), pcabuilder.InitProp('(A or B)'))
        self.assertNotEqual(pcabuilder.InitProp('A or B'), pcabuilder.InitProp('B or A'))

    def test_unique_vars(self):
        to_test = [pcaprop.Variable('A'), pcaprop.Variable('B')]
        self.assertEqual(pcabuilder.InitProp('Bor A iff B and A').unique_vars(), to_test)
        self.assertEqual([variable.name for variable in pcabuilder.InitProp('Bor A iff B and A').unique_vars()],
                         ['A', 'B'])

    def test_simple_props(self):
        to_test = [[pcaprop.FalseProp(), pcaprop.FalseProp()], [pcaprop.TrueProp(), pcaprop.TrueProp()]]
        self.assertEqual(list(pcabuilder.InitProp('A').interpretations()), to_test)
        to_test = [[pcaprop.FalseProp(), pcaprop.TrueProp()], [pcaprop.TrueProp(), pcaprop.FalseProp()]]
        self.assertEqual(list(pcabuilder.InitProp('not (not (not A))').interpretations()), to_test)

    def test_disjunction(self):
        to_test = [[pcaprop.FalseProp(), pcaprop.FalseProp(), pcaprop.FalseProp()],
                   [pcaprop.FalseProp(), pcaprop.TrueProp(), pcaprop.TrueProp()],
                   [pcaprop.TrueProp(), pcaprop.FalseProp(), pcaprop.TrueProp()],
                   [pcaprop.TrueProp(), pcaprop.TrueProp(), pcaprop.TrueProp()]]
        self.assertEqual(list(pcabuilder.InitProp('A or B').interpretations()), to_test)
        to_test = [[pcaprop.FalseProp(), pcaprop.TrueProp()], [pcaprop.TrueProp(), pcaprop.TrueProp()]]
        self.assertEqual(list(pcabuilder.InitProp('A or true').interpretations()), to_test)

    def test_conjunction(self):
        to_test = [[pcaprop.FalseProp(), pcaprop.FalseProp(), pcaprop.FalseProp()],
                   [pcaprop.FalseProp(), pcaprop.TrueProp(), pcaprop.FalseProp()],
                   [pcaprop.TrueProp(), pcaprop.FalseProp(), pcaprop.FalseProp()],
                   [pcaprop.TrueProp(), pcaprop.TrueProp(), pcaprop.TrueProp()]]
        self.assertEqual(list(pcabuilder.InitProp('A and B').interpretations()), to_test)
        to_test = [[pcaprop.FalseProp(), pcaprop.FalseProp()], [pcaprop.TrueProp(), pcaprop.TrueProp()]]
        self.assertEqual(list(pcabuilder.InitProp('A and true').interpretations()), to_test)

    def test_comb(self):
        to_test = [
            [pcaprop.FalseProp(), pcaprop.FalseProp(), pcaprop.FalseProp(), pcaprop.FalseProp(), pcaprop.TrueProp()],
            [pcaprop.FalseProp(), pcaprop.FalseProp(), pcaprop.FalseProp(), pcaprop.TrueProp(), pcaprop.TrueProp()],
            [pcaprop.FalseProp(), pcaprop.FalseProp(), pcaprop.TrueProp(), pcaprop.FalseProp(), pcaprop.FalseProp()],
            [pcaprop.FalseProp(), pcaprop.FalseProp(), pcaprop.TrueProp(), pcaprop.TrueProp(), pcaprop.FalseProp()],
            [pcaprop.FalseProp(), pcaprop.TrueProp(), pcaprop.FalseProp(), pcaprop.FalseProp(), pcaprop.TrueProp()],
            [pcaprop.FalseProp(), pcaprop.TrueProp(), pcaprop.FalseProp(), pcaprop.TrueProp(), pcaprop.TrueProp()],
            [pcaprop.FalseProp(), pcaprop.TrueProp(), pcaprop.TrueProp(), pcaprop.FalseProp(), pcaprop.FalseProp()],
            [pcaprop.FalseProp(), pcaprop.TrueProp(), pcaprop.TrueProp(), pcaprop.TrueProp(), pcaprop.FalseProp()],
            [pcaprop.TrueProp(), pcaprop.FalseProp(), pcaprop.FalseProp(), pcaprop.FalseProp(), pcaprop.FalseProp()],
            [pcaprop.TrueProp(), pcaprop.FalseProp(), pcaprop.FalseProp(), pcaprop.TrueProp(), pcaprop.FalseProp()],
            [pcaprop.TrueProp(), pcaprop.FalseProp(), pcaprop.TrueProp(), pcaprop.FalseProp(), pcaprop.TrueProp()],
            [pcaprop.TrueProp(), pcaprop.FalseProp(), pcaprop.TrueProp(), pcaprop.TrueProp(), pcaprop.FalseProp()],
            [pcaprop.TrueProp(), pcaprop.TrueProp(), pcaprop.FalseProp(), pcaprop.FalseProp(), pcaprop.TrueProp()],
            [pcaprop.TrueProp(), pcaprop.TrueProp(), pcaprop.FalseProp(), pcaprop.TrueProp(), pcaprop.TrueProp()],
            [pcaprop.TrueProp(), pcaprop.TrueProp(), pcaprop.TrueProp(), pcaprop.FalseProp(), pcaprop.FalseProp()],
            [pcaprop.TrueProp(), pcaprop.TrueProp(), pcaprop.TrueProp(), pcaprop.TrueProp(), pcaprop.TrueProp()]]
        self.assertEqual(list(pcabuilder.InitProp('A and D or not C iff A implies B').interpretations()), to_test)

    def test_sat(self):
        self.assertTrue(pcabuilder.InitProp('A').satisfiable())
        self.assertFalse(pcabuilder.InitProp('A and not A').satisfiable())

    def test_taut(self):
        self.assertFalse(pcabuilder.InitProp('A').tautology())
        self.assertFalse(pcabuilder.InitProp('A or B').tautology())
        # Excluded middle
        self.assertTrue(pcabuilder.InitProp('A or not A').tautology())
        self.assertFalse(pcabuilder.InitProp('A and B implies C').tautology())
        # Contraposition
        self.assertTrue(pcabuilder.InitProp('(A implies B) iff (not B implies not A)').tautology())
        # proof by exh
        self.assertTrue(pcabuilder.InitProp('(((A or B) and (A implies C)) and (B implies C)) implies C').tautology())

    def test_contr(self):
        self.assertFalse(pcabuilder.InitProp('A').contradiction())
        self.assertTrue(pcabuilder.InitProp('A and not A').contradiction())
        self.assertFalse(pcabuilder.InitProp('(not(A and B)) ⇔ ((not A) or (not B))').contradiction())

    def test_distributivity(self):
        self.assertEqual(list(pcabuilder.InitProp('A ∨ (B ∧ C)').interpretations()),
                         list(pcabuilder.InitProp('(A ∨ B) ∧ (A ∨ C)').interpretations()))

    def test_de_morgan(self):
        self.assertEqual(list(pcabuilder.InitProp('not(A or B)').interpretations()),
                         list(pcabuilder.InitProp('(not A) and (not B)').interpretations()))
        self.assertTrue(pcabuilder.InitProp('(not(A and B)) ⇔ ((not A) or (not B))').tautology())
        self.assertTrue(pcabuilder.InitProp('(not(A or B)) ⇔ ((not A) and (not B))').tautology())
        self.assertEqual(pcabuilder.InitProp('¬(A or B)').de_morgan(),
                         pcaprop.ConjunctionOp(pcaprop.NegationOp(pcaprop.Variable('A')),
                                               pcaprop.NegationOp(pcaprop.Variable('B'))))
        self.assertEqual(pcabuilder.InitProp('¬(A and B)').de_morgan(),
                         pcaprop.DisjunctionOp(pcaprop.NegationOp(pcaprop.Variable('A')),
                                               pcaprop.NegationOp(pcaprop.Variable('B'))))
        self.assertEqual(pcabuilder.InitProp('A or ¬(A and B)').de_morgan(),
                         pcaprop.DisjunctionOp(pcaprop.Variable('A'),
                                               pcaprop.DisjunctionOp(pcaprop.NegationOp(pcaprop.Variable('A')),
                                                                     pcaprop.NegationOp(pcaprop.Variable('B')))))

    def test_dijkstra_rule(self):
        self.assertTrue(pcabuilder.InitProp('(((A ∧ B) ⇔ A) ⇔ B) ⇔ (A ∨ B)').tautology())

    def test_contrapositive(self):
        self.assertEqual(list(pcabuilder.InitProp('C ⇒ (A ∧ B)').interpretations()),
                         list(pcabuilder.InitProp('(C ⇒ A) ∧ (C ⇒ B)').interpretations()))

    def test_idempotence(self):
        self.assertTrue(pcabuilder.InitProp('A and A').idempotence() == pcaprop.Variable('A'))
        self.assertTrue(pcabuilder.InitProp('not not (A and A)').idempotence() ==
                        pcaprop.NegationOp(pcaprop.NegationOp(pcaprop.Variable('A'))))
        self.assertTrue(pcabuilder.InitProp('B or not (A and A)').idempotence() ==
                        pcaprop.DisjunctionOp(pcaprop.Variable('B'),
                                              pcaprop.NegationOp(pcaprop.Variable('A'))))
        self.assertTrue(pcabuilder.InitProp('B or not (A and ( A or A))').idempotence() ==
                        pcaprop.DisjunctionOp(pcaprop.Variable('B'), pcaprop.NegationOp(pcaprop.Variable('A'))))
        self.assertFalse(pcabuilder.InitProp('not not (A and B)').idempotence() ==
                         pcaprop.NegationOp(pcaprop.NegationOp(pcaprop.Variable('A'))))

    def test_commutativity(self):
        self.assertTrue(pcabuilder.InitProp('A and B').commutativity() ==
                        pcaprop.ConjunctionOp(pcaprop.Variable('B'), pcaprop.Variable('A')))
        self.assertTrue(pcabuilder.InitProp('A and (C and B)').commutativity() == pcaprop.ConjunctionOp(
            pcaprop.ConjunctionOp(pcaprop.Variable('B'), pcaprop.Variable('C')), pcaprop.Variable('A')))
        self.assertTrue(pcabuilder.InitProp('A or (C and ( D or B))').commutativity() == pcaprop.DisjunctionOp(
            pcaprop.ConjunctionOp(pcaprop.DisjunctionOp(pcaprop.Variable('B'), pcaprop.Variable('D')),
                                  pcaprop.Variable('C')), pcaprop.Variable('A')))
        self.assertTrue(pcabuilder.InitProp('B implies (A and B)').commutativity() == pcaprop.ImplicationOp(
            pcaprop.Variable('B'), pcaprop.ConjunctionOp(pcaprop.Variable('B'), pcaprop.Variable('A'))))
        self.assertTrue(pcabuilder.InitProp('not not (A and B)').commutativity() == pcaprop.NegationOp(
            pcaprop.NegationOp(pcaprop.ConjunctionOp(pcaprop.Variable('B'), pcaprop.Variable('A')))))

    def test_maximum(self):
        self.assertTrue(pcabuilder.InitProp('A or true').maximum() == pcaprop.TrueProp())
        self.assertTrue(pcabuilder.InitProp('true or (A iff B)').maximum() == pcaprop.TrueProp())
        self.assertTrue(pcabuilder.InitProp('B iff (A and (true or (A iff B)))').maximum() ==
                        pcaprop.EquivalenceOp(pcaprop.Variable('B'), pcaprop.Variable('A')))
        self.assertTrue(pcabuilder.InitProp('A and true').maximum() == pcaprop.Variable('A'))
        self.assertTrue(pcabuilder.InitProp('true and (A iff B)').maximum() ==
                        pcaprop.EquivalenceOp(pcaprop.Variable('A'), pcaprop.Variable('B')))

    def test_minimum(self):
        self.assertTrue(pcabuilder.InitProp('A or false').minimum() == pcaprop.Variable('A'))
        self.assertTrue(pcabuilder.InitProp('false or (A iff B)').minimum() ==
                        pcaprop.EquivalenceOp(pcaprop.Variable('A'), pcaprop.Variable('B')))
        self.assertTrue(pcabuilder.InitProp('A and false').minimum() == pcaprop.FalseProp())
        self.assertTrue(pcabuilder.InitProp('false and (A iff B)').minimum() == pcaprop.FalseProp())
        self.assertTrue(pcabuilder.InitProp('B iff (A and (false and (A iff B)))').minimum() ==
                        pcaprop.EquivalenceOp(pcaprop.Variable('B'), pcaprop.FalseProp()))

    def test_involution(self):
        self.assertTrue(pcabuilder.InitProp('not not not not A').involution() == pcaprop.Variable('A'))
        self.assertTrue(pcabuilder.InitProp('not not (B or not not A)').involution() ==
                        pcaprop.DisjunctionOp(pcaprop.Variable('B'), pcaprop.Variable('A')))

    def test_implication(self):
        self.assertTrue(pcabuilder.InitProp('A implies B').implication() ==
                        pcaprop.DisjunctionOp(pcaprop.NegationOp(pcaprop.Variable('A')), pcaprop.Variable('B')))
        self.assertTrue(pcabuilder.InitProp('A or not (A implies B)').implication() ==
                        pcaprop.DisjunctionOp(pcaprop.Variable('A'), pcaprop.NegationOp(
                            pcaprop.DisjunctionOp(pcaprop.NegationOp(pcaprop.Variable('A')), pcaprop.Variable('B')))))

    def test_associativity(self):
        return

    def test_absorption(self):
        return

    def test_excluded_middle(self):
        return

    def test_equivalence(self):
        return


if __name__ == '__main__':
    unittest.main()

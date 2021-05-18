import unittest

from pca_main import pcaprop, pcaparser


class TestParser(unittest.TestCase):

    def test_simple_var(self):
        a = pcaparser.PARSER.parse('P')
        to_assert = pcaprop.Variable('P')
        self.assertEqual(a, to_assert)

    def test_prop(self):
        a = pcaparser.PARSER.parse('P or B iff C and A implies (P and C)')
        to_assert = pcaprop.EquivalenceOp(pcaprop.DisjunctionOp(pcaprop.Variable('P'), pcaprop.Variable('B')),
                                          pcaprop.ImplicationOp(
                                              pcaprop.ConjunctionOp(pcaprop.Variable('C'), pcaprop.Variable('A')),
                                              pcaprop.ConjunctionOp(pcaprop.Variable('P'), pcaprop.Variable('C'))))
        self.assertEqual(a, to_assert)
        a = pcaparser.PARSER.parse('true or not A implies false and not not not B or A')
        to_assert = pcaprop.ImplicationOp(
            pcaprop.DisjunctionOp(pcaprop.TrueProp(), pcaprop.NegationOp(pcaprop.Variable('A'))),
            pcaprop.DisjunctionOp(
                pcaprop.ConjunctionOp(pcaprop.FalseProp(), pcaprop.NegationOp(
                    pcaprop.NegationOp(pcaprop.NegationOp(pcaprop.Variable('B'))))),
                pcaprop.Variable('A')))
        self.assertEqual(a, to_assert)

    def test_multiples(self):
        a = pcaparser.PARSER.parse('A and B and C or D or F')
        to_assert = pcaprop.DisjunctionOp(pcaprop.DisjunctionOp(
            pcaprop.ConjunctionOp(pcaprop.ConjunctionOp(pcaprop.Variable('A'), pcaprop.Variable('B')),
                                  pcaprop.Variable('C')), pcaprop.Variable('D')), pcaprop.Variable('F'))
        self.assertEqual(a, to_assert)
        a = pcaparser.PARSER.parse('A implies B implies C iff D iff F')
        to_assert = pcaprop.EquivalenceOp(pcaprop.EquivalenceOp(
            pcaprop.ImplicationOp(pcaprop.ImplicationOp(pcaprop.Variable('A'), pcaprop.Variable('B')),
                                  pcaprop.Variable('C')), pcaprop.Variable('D')), pcaprop.Variable('F'))
        self.assertEqual(a, to_assert)


if __name__ == '__main__':
    unittest.main()

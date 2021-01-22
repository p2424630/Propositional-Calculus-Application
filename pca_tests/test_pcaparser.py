import unittest

from pca_main.pcaparser import PARSER
from pca_main import pcaprop


class TestParser(unittest.TestCase):

    def test_simple_var(self):
        a = PARSER.parse('P')
        to_assert = pcaprop.Variable('P')
        self.assertEqual(a, to_assert)

    def test_prop(self):
        a = PARSER.parse('P or B iff C and A implies (P and C)')
        to_assert = pcaprop.EquivalenceOp(pcaprop.DisjunctionOp(pcaprop.Variable('P'), pcaprop.Variable('B')),
                                          pcaprop.ImplicationOp(
                                              pcaprop.ConjunctionOp(pcaprop.Variable('C'), pcaprop.Variable('A')),
                                              pcaprop.ConjunctionOp(pcaprop.Variable('P'), pcaprop.Variable('C'))))
        self.assertEqual(a, to_assert)
        a = PARSER.parse('true or not A implies false and not not not B or A')
        to_assert = pcaprop.ImplicationOp(
            pcaprop.DisjunctionOp(pcaprop.TrueProp(), pcaprop.NegationOp(pcaprop.Variable('A'))),
            pcaprop.DisjunctionOp(
                pcaprop.ConjunctionOp(pcaprop.FalseProp(), pcaprop.NegationOp(
                    pcaprop.NegationOp(pcaprop.NegationOp(pcaprop.Variable('B'))))),
                pcaprop.Variable('A')))
        self.assertEqual(a, to_assert)


if __name__ == '__main__':
    unittest.main()

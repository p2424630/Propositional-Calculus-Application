import unittest

from pca.propcalc.tools.parser import PARSER
from pca.propcalc.tools.proposition import ConjunctionOp, DisjunctionOp, EquivalenceOp, FalseProp
from pca.propcalc.tools.proposition import ImplicationOp, NegationOp, TrueProp, Variable


class TestParser(unittest.TestCase):

    def test_simple_var(self):
        a = PARSER.parse('P')
        to_assert = Variable('P')
        self.assertEqual(a, to_assert)

    def test_prop(self):
        a = PARSER.parse('P or B iff C and A implies (P and C)')
        to_assert = EquivalenceOp(DisjunctionOp(Variable('P'), Variable('B')),
                                  ImplicationOp(ConjunctionOp(Variable('C'), Variable('A')),
                                                ConjunctionOp(Variable('P'), Variable('C'))))
        self.assertEqual(a, to_assert)
        a = PARSER.parse('true or not A implies false and not not not B or A')
        to_assert = ImplicationOp(DisjunctionOp(TrueProp(), NegationOp(Variable('A'))),
                                  DisjunctionOp(
                                      ConjunctionOp(FalseProp(),NegationOp(NegationOp(NegationOp(Variable('B'))))),
                                                    Variable('A')))
        self.assertEqual(a, to_assert)

    if __name__ == '__main__':
        unittest.main()

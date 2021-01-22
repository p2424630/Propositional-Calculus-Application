import unittest

from pca.propcalc.proposition import ConjunctionOp, DisjunctionOp
from pca.propcalc.proposition import NegationOp, TrueProp


class TestProposition(unittest.TestCase):

    def test_prop(self):
        a = TrueProp()
        b = NegationOp(a)
        self.assertTrue(a)
        self.assertFalse(b.eval())
        self.assertTrue(DisjunctionOp(a, b.eval()).eval())
        self.assertFalse(ConjunctionOp(b.eval(), a).eval())


if __name__ == '__main__':
    unittest.main()

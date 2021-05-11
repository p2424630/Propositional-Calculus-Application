import unittest

from pca_main import pcaprop


class TestProposition(unittest.TestCase):

    def test_prop(self):
        a = pcaprop.TrueProp()
        b = pcaprop.NegationOp(a)
        self.assertTrue(a)
        self.assertFalse(b.eval())
        self.assertTrue(pcaprop.DisjunctionOp(a, b.eval()).eval())
        self.assertFalse(pcaprop.ConjunctionOp(b.eval(), a).eval())

    def test_creation(self):
        a = pcaprop.Variable("A")
        b = pcaprop.Variable("B")
        c = pcaprop.Variable("C")
        self.assertEqual(a >> (~(a * b) + c), pcaprop.ImplicationOp(
            a, pcaprop.DisjunctionOp(pcaprop.NegationOp(pcaprop.ConjunctionOp(a, b)), c)))

    def test_precedence(self):
        a = pcaprop.Variable("A")
        b = pcaprop.Variable("B")
        self.assertEqual((a + b >> ~a * b), pcaprop.ImplicationOp(
          pcaprop.DisjunctionOp(a, b), pcaprop.ConjunctionOp(pcaprop.NegationOp(a), b)))


if __name__ == '__main__':
    unittest.main()

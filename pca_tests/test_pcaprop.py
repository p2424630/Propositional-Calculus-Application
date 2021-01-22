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


if __name__ == '__main__':
    unittest.main()

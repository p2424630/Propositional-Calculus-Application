import unittest
from lark import Tree, Token
from pca.propcalc.tools.parser import PARSER


class TestParser(unittest.TestCase):

    def test_simple_var(self):
        a = PARSER.parse('P')
        to_assert = Tree('atom_var', [Token('VAR', 'P')])
        self.assertEqual(a, to_assert)


if __name__ == '__main__':
    unittest.main()

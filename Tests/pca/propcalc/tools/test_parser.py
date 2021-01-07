# @Author: GKarseras
# @Date:   17 Nov 2020 08:28

from lark import Tree, Token
from pytest_mock import mocker

from pca.propcalc.tools.parser import PARSER


class TestParser:

    def test_simple_var(self):
        a = PARSER.parse('P')
        to_assert = Tree('atom_var', [Token('VAR', 'P')])
        assert a == to_assert

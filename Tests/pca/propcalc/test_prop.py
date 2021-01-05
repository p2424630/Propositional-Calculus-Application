# @Author: GKarseras
# @Date:   15 Nov 2020 11:36


from lark import Tree, Token
from pytest_mock import mocker

from pca.propcalc.tools.grammar import PARSER
from pca.propcalc.tools.prop import ConjunctionOp, DisjunctionOp, EquivalenceOp, FalseProp, ImplicationOp
from pca.propcalc.tools.prop import NegationOp, TrueProp, Variable, AtomTransformer


class TestParser:

    def test_simple_var(self):
        a = PARSER.parse('P')
        to_assert = Tree('start', [Tree('var', [Token('VAR', 'P')])])
        assert a == to_assert
        b = AtomTransformer().transform(a)
        to_assert = [Variable('P')]
        assert b == to_assert

    def test_sequence(self):
        a = PARSER.parse('P or true')
        b = AtomTransformer().transform(a)
        to_assert = [DisjunctionOp(Variable('P'), TrueProp())]
        assert b == to_assert

    def test_precedence(self):
        a = PARSER.parse('P or Q and F implies P and not Q')
        b = AtomTransformer().transform(a)
        to_assert = [ImplicationOp(DisjunctionOp(Variable('P'), ConjunctionOp(
            Variable('Q'), Variable('F'))), ConjunctionOp(Variable('P'), NegationOp(Variable('Q'))))]
        assert b == to_assert

    # def test_mocking_class_method(self, mocker):
    #     expected = 'xyz'
    #
    #     def mock_load():
    #         return 'xyz'
    #
    #     mocker.patch(
    #         'mock_examples.main.Dataset.load_data',
    #         mock_load
    #     )
    #     actual = slow_dataset()
    #     assert expected == actual
    #


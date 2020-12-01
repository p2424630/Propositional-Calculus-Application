import pytest
from pca.propcalc.tools.tree import *
from pca.propcalc.main.proposition import *


@pytest.fixture
def simple_nodes():
    return [Node(x) for x in range(3)]


@pytest.fixture
def parsed_tree():
    return Node('and', Node('B'), Node('and', Node('implies', Node('A'), Node('B')), Node('A')))


@pytest.fixture
def simple_propositions():
    a = Proposition()
    b = Proposition()
    return a, b

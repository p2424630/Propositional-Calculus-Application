import pytest
from pca.propcalc.main.tree import Node


@pytest.fixture
def simple_nodes():
    return [Node(x) for x in range(3)]


@pytest.fixture
def parsed_tree():
    return Node('and', Node('B'), Node('and', Node('implies', Node('A'), Node('B')), Node('A')))

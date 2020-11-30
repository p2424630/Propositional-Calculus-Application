# @Author: GKarseras
# @Date:   19 Nov 2020 20:21

from pca.propcalc.main.tree import Node

import pytest
from copy import deepcopy


class TestTree:

    def test_initialization_with_children(self, simple_nodes):
        n1 = Node(1, simple_nodes[0], simple_nodes[1])
        assert n1.left == simple_nodes[0] and n1.right == simple_nodes[1]
        n1copy = deepcopy(n1)
        assert n1 != n1copy
        n1copy.left = simple_nodes[0]
        n1copy.right = simple_nodes[1]
        assert n1 != n1copy
        assert n1copy.left == n1.left and n1copy.right == n1.right

    def test_initialization_no_children(self, simple_nodes):
        no_children = [x.right is None and x.left is None for x in simple_nodes]
        assert no_children == [True, True, True]

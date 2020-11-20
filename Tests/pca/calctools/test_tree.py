# @Author: GKarseras
# @Date:   19 Nov 2020 20:21

from pca.propcalc.calctools.tree import Node
import pytest


class TestTree:

    def test_no_children(self):
        assert Node("No Child").left is None and Node("No Child").right is None
        tree = [Node(x) for x in range(3)]
        tree[0].left = tree[1]
        tree[0].right = tree[2]
        no_children = [x.right is None and x.left is None for x in tree]
        assert no_children == [False, True, True]
        tree.append(Node(4))
        tree[2].left = tree[3]
        no_children = [x.right is None and x.left is None for x in tree]
        assert no_children == [False, True, False, True]


# @Author: GKarseras
# @Date:   19 Nov 2020 20:21
from typing import List
from pca.propcalc.tools.config import *


class Node:
    __slots__ = ('value', 'left', 'right')

    def __init__(self, value, left=None, right=None) -> None:
        self.value = value
        self.left = left
        self.right = right


def preOrder(root: Node) -> list:
    return [root.value] + preOrder(root.left) + preOrder(root.right) if root else []


def buildTree(formula: List[str]) -> Node:
    temp_l = []
    for e in formula:
        if e in NEGATION:
            n = Node(e, temp_l.pop())
            if e != 'not':
                n.right = temp_l.pop()
            temp_l.append(n)
        else:
            temp_l.append(Node(e))
    return temp_l.pop()

# @Author: GKarseras
# @Date:   19 Nov 2020 20:21


class Node:
    __slots__ = ('value', 'left', 'right')

    def __init__(self, value, left=None, right=None) -> None:
        self.value = value
        self.left = left
        self.right = right


def inOrder(root: Node) -> list:
    return inOrder(root.left) + [root.value] + inOrder(root.right) if root else []


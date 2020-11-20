# @Author: GKarseras
# @Date:   19 Nov 2020 20:21


class Node:
    __slots__ = ('value', 'left', 'right')

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

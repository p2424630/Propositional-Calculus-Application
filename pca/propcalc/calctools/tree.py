# @Author: GKarseras
# @Date:   19 Nov 2020 20:21


class Tree:
    __slots__ = ('__data', 'left', 'right')

    def __init__(self, data, left=None, right=None):
        self.__data = data
        self.left = left
        self.right = right

    @property
    def data(self):
        return self.__data




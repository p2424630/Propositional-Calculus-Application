# @Author: GKarseras
# @Date:   16 Nov 2020 11:05

from pca.propcalc.main.proposition import *
from pca.propcalc.tools.truthtable import *
from pca.propcalc.tools.tree import *

# root = Node(1)
# n2 = Node(2)
# n3 = Node(3)
# root.left = n2
# root.right = n3
# a = inOrder(root)
# b = inOrder(n3)


parsed_tree = Node('and', Node('B'), Node('and', Node('implies', Node('A'), Node('B')), Node('A')))
formula = ['A', 'and', 'B']
print(buildTree(formula))


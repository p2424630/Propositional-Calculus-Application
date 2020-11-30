# @Author: GKarseras
# @Date:   16 Nov 2020 11:05

from pca.propcalc import mainapp as pca_main
from pca.propcalc.calctools import proposition as pca_bool
from pca.propcalc.calctools import symbol as pca_sym
from pca.propcalc.calctools import truthtable as pca_truth
from pca.propcalc.calctools.tree import Node


n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n1.left = n2
n1.right = n3

n5 = Node(5, n1, n2)

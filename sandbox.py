# @Author: GKarseras
# @Date:   16 Nov 2020 11:05

from pca.propcalc.main.proposition import *
from pca.propcalc.tools.prop import *

# a = parseANDtrans('A and B')
a = DisjunctionOp(Variable('A'), Variable('B'))

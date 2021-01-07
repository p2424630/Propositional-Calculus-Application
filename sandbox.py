# @Author: GKarseras
# @Date:   16 Nov 2020 11:05

from pca.propcalc.main.proposition import *
from pca.propcalc.tools.prop import *


a = InitProp('A implies B')
l = []
tr = SimpleTransformer()
tr.transform(a._parsed)
prop_vars = tr.prop_vars
vars_len = len(prop_vars)
combs = list(product([FalseProp(), TrueProp()], repeat=vars_len))
for comb in combs:
    interp = dict(zip(prop_vars, comb))
    interp_prop = AtomTransformer(interp).transform(a._parsed)
    l.append(eval_prop(interp_prop))
print(l)

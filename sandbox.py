# @Author: GKarseras
# @Date:   16 Nov 2020 11:05

from pca.propcalc.main.proposition import *
from pca.propcalc.tools.prop import *


def eval_prop(op):
    if isinstance(op, (bool, TrueProp, FalseProp)):
        return op
    if isinstance(op, NegationOp):
        if isinstance(op.prop, (bool, TrueProp, FalseProp)):
            return op.eval()
        return not eval_prop(op.prop)   # TODO: Change from not
    elif isinstance(op, BinaryOp):
        if all(isinstance(prop, (bool, TrueProp, FalseProp)) for prop in [op.prop_l, op.prop_r]):
            return op.eval()
        if isinstance(op.prop_l, (bool, TrueProp, FalseProp)):
            return op.prop_l and eval_prop(op.prop_r)
        if isinstance(op.prop_r, (bool, TrueProp, FalseProp)):
            return eval_prop(op.prop_l) and op.prop_r
        return eval_prop(op.prop_l) and eval_prop(op.prop_r)

# a = parseANDtrans('A and B')
# a = DisjunctionOp(Variable('A'), Variable('B'))
a = InitProp('not not B and not C and A')
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

# @Author: GKarseras
# @Date:   16 Nov 2020 11:05

from pca.propcalc.main.proposition import *
from pca.propcalc.tools.prop import *


# def eval_props(op: Operation):
#     if isinstance(op, UnaryOp):
#         print(f'UnaryOp: {op}')
#         return eval_props(op.eval())
#
#     elif isinstance(op, BinaryOp):
#         print(f'BinaryOp: {op}')
#         if isinstance(prop_l, bool):
#             if isinstance(prop_r, bool):
#                 return op.eval()
#             return [op.eval()] + eval_props(op.prop_l) + eval_props(op.prop_r) if op else []



# a = parseANDtrans('A and B')
# a = DisjunctionOp(Variable('A'), Variable('B'))
a = InitProp('not((A or B and C) or C)')
l = []
tr = SimpleTransformer()
tr.transform(a._parsed)
prop_vars = tr.prop_vars
vars_len = len(prop_vars)
combs = list(product([FalseProp(), TrueProp()], repeat=vars_len))
for comb in combs:
    interp = dict(zip(prop_vars, comb))
    interp_prop = AtomTransformer(interp).transform(a._parsed)
    l.append(interp_prop)
print(l)

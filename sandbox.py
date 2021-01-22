# @Author: GKarseras
# @Date:   16 Nov 2020 11:05

from pca.propcalc.prop_builder import *

a = InitProp('not(A ⇔ B)')
print(f'prop: {a.prop}')
print(f'parsed: {a.parsed}')
print(f'sat: {a.satisfiable()}')
print(f'taut: {a.tautology()}')
print(f'contr: {a.contradiction()}')
print(f'truth: {a.build_interp()}')

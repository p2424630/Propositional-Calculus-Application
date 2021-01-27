# @Author: GKarseras
# @Date:   16 Nov 2020 11:05

from pca_main import pcabuilder

a = pcabuilder.InitProp('A or (B iff (C and (D implies (E or (F and (G iff (L and M implies (N or (P and ('
                        'Z iff X or W))) iff H)))))))')
# print(f'prop: {a.prop}')
# print(f'parsed: {a.parsed}')
# print(f'sat: {a.satisfiable()}')
# print(f'taut: {a.tautology()}')
# print(f'contr: {a.contradiction()}')
# print(f'truth: {a.build_interp()}')

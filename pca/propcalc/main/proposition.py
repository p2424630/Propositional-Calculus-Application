# @Author: GKarseras
# @Date:   15 Nov 2020 11:13

from __future__ import annotations
from itertools import product

from pca.propcalc.tools.prop import AtomTransformer
from pca.propcalc.tools.grammar import PARSER


class InitProp:
    __slots__ = ('_prop', '_parsed', '_trans', '_vars', '_combs')

    def __init__(self, prop: str):
        self._prop = prop
        self._parsed = PARSER.parse(self._prop)
        self._trans = None
        self._vars = None
        self._combs = None

    def _transform(self) -> None:
        """
        Transform Parsed string stored in self._parsed using custom Transformer.

        Saving results in self._trans for the transformed and
        self._vars for the number of variables that were found.
        """
        tr = AtomTransformer()
        try:
            trans = tr.transform(self._parsed)
        except Exception as e:
            raise Exception(f'Transforming {self._parsed}') from e
        if not isinstance(trans, list):
            raise TypeError(f'Expected type list, got {type(trans)} instead')
        self._trans = trans[0]
        self._vars = tr.prop_vars if (len(tr.prop_vars) > 0) else None

    def _createCombinations(self, max_vars: int = 5) -> None:
        """
        If not already parsed then call parseANDtrans function,
        create all possible Interpretations of the variables in a formula.

        :param max_vars: Default set to 5 variables, overwrite if required.
        """
        if not (self._parsed and self._vars):
            self._parseANDtrans()
        if self._vars is None or (len(self._vars) < 1):
            raise ValueError('Number of variables must be at least 1')
        n = len(self._vars)
        if n > max_vars:
            raise ValueError(f'Variable length {n}, exceeded the allowed {max_vars}')
        self._combs = (False, True) if (n == 1) else product([False, True], repeat=n)

    def truth(self):
        if not self._combs:
            self._createCombinations()
        for x, i in self._combs:
            print(f'x: {x}\ni: {i}')

    def satisfiable(self):
        # return any(permutations{True, False} Proposition == True)
        pass

    def tautology(self):
        # return all(permutations{True, False} Proposition == True)
        pass

    def contradiction(self):
        # return all(permutations{True, False} Proposition == False)
        pass

# @Author: GKarseras
# @Date:   15 Nov 2020 11:15
from copy import deepcopy

from pca.propcalc.main.proposition import *

import pytest


class TestProposition:

    def test_simple(self, simple_propositions):
        a = Proposition('(q OR p)')

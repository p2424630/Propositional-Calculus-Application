import pytest
from pca.propcalc.tools.prop import *


@pytest.fixture
def simple_propositions():
    a = Proposition()
    b = Proposition()
    return a, b

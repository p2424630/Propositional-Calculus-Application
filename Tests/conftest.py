import pytest
from pca.propcalc.main.proposition import *


@pytest.fixture
def simple_propositions():
    a = Proposition()
    b = Proposition()
    return a, b

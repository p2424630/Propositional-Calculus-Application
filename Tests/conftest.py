import pytest
from pca.propcalc.main.proposition import InitProp


@pytest.fixture
def propositions():
    return {
        'de_morgan': InitProp('(not(A and B)) ⇔ ((not A) or (not B))')
    }

# @Author: GKarseras
# @Date:   6 Nov 2020 00:33

from setuptools import setup, find_packages
from import __version__

setup(
    name='propcalc',
    version=__version__,
    extras_require=dict(test=['pytest']),
    packages=find_packages(where='src'),
    package_dir={"": "src"}
)

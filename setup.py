# @Author: GKarseras
# @Date:   6 Nov 2020 00:33

from setuptools import setup, find_packages

setup(
    name='propcalc',
    extras_require=dict(test=['pytest']),
    packages=find_packages(where='src'),
    package_dir={"": "src"}
)

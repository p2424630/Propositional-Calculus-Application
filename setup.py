# @Author: GKarseras
# @Date:   6 Nov 2020 00:33

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='propcalc',
    extras_require=dict(test=['pytest']),
    packages=find_packages(where='pca_main'),
    package_dir={"": "pca_main"},
    install_requires=requirements)

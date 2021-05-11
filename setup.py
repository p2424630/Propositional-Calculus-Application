# @Author: GKarseras
# @Date:   6 Nov 2020 00:33

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='pca',
    version='1.0.0',
    description='Propositional Calculus Application',
    author='Georgios Karseras',
    url='https://github.com/p2424630/PCA',
    packages=find_packages(where='pca_main'),
    install_requires=requirements)

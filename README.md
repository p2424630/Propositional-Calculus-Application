# Propositional-Calculus-Application

This is a Python application regarding Propositional Calculus, allowing the creation of proposition given a valid string
and providing various functionalities that can be further applied.

The main usage is as a back-end API server for the [Front-End](https://github.com/p2424630/PCA-Front).

***

## Setup

1. Have python installed (recommended [miniconda](https://docs.conda.io/en/latest/miniconda.html))
2. Run `pip install -e PCA_DIRECTORY`
3. Navigate to `PCA_DIRECTORY` and run `uvicorn pcacontroller:app` to start the API server. Use `--port PORT` to specify the port and `--reload` to have automatic reload of server on file change.


***

## Usage

Main usage of this application is as an API server with a robust front-end as the one developed with it. 

It can still be
used standalone though, in this case the required libraries are only: `setuptools` and `lark-parser`.

An example is shown below, parsing a simple proposition and performing various
functions.

```python
from pca_main import pcabuilder

prop = pcabuilder.InitProp("A or B and ¬ ¬ C")
print(f'prop: {str(prop)}')

for interp in prop.interpretations():
    print(interp)
print(f'sat: {prop.satisfiable()}')
print(f'taut: {prop.tautology()}')
print(f'prop_inv: {prop.involution()}')
print(f'prop_com: {prop.commutativity()}')
```

![alt text][pcabuilder]

[pcabuilder]: images/pcabuilder_example.JPG "pcabuilder image"

### Parsing Grammar

| Input        | Accepted|
| ------------- |:-------------:|
| Variable | Capital Character or Word|
| True | `true` `top` `⊤`|
| False | `false` `bot` `⊥`|
| Negation | `not` `¬` `!` `˜`|
| Conjunction | `and` `∧` `·` `&`|
| Disjunction | `or` `∨` `+` `∥`|
| Implication | `implies` `⇒` `→`|
| Equivalence | `iff` `⇔` `↔`|

### Precedence

1. ( ) - True - False - Variable

2. Conjunction

3. Disjunction

4. Implication

5. Equivalence

> The exact grammar can be seen in [pcaparser](pca_main/pcaparser.py)



***

## License

> More info can be found [here](LICENSE)

The project is licenced under MIT.

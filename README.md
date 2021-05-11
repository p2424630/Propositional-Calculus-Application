# Propositional-Calculus-Application

This is a Python application regarding Propositional Calculus. Firstly, `pcaprop` defines the propositions,
then `pcabuilder` extends the application with law applications, truth table creation for all possible interpretations
and other functionalities. The `pcabuilder` is initialized with a string, which is parsed and transformed into
proposition with `pcaparser`. Finally, the `pcacontroller` is used to create an API back-end server which is used in
combination with the [Front-End](https://github.com/p2424630/PCA-Front).

***

## Setup

1. Have python installed (recommended miniconda)
2. Run `pip install -e PCA_DIRECTORY`
3. Navigate to `PCA_DIRECTORY` and run `uvicorn pcacontroller:app` to start the API server. Use `--port PORT` to specify
   the port and `--reload` to have automatic reload of server on file change.

***

## Usage

Main usage of this application is as an API server with a robust front-end as the one developed with it. It can still be
used standalone, in this case the installation of the libraries: `fastapi`, `pydantic`, `uvicorn`
and `starlette` is not necessary. An example is shown below, parsing a simple proposition and performing various
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

### Parsing Grammar

| Input        | Accepted|
| ------------- |:-------------:|
| Variable | Capital Character or Word|
| True | `true` `top` `⊤`|
| False | `false` `bot` `⊥`|
| Negation | `not` `¬` `!` `˜`|
| Equivalence | `iff` `⇔` `↔`|
| Implication | `implies` `⇒` `→`|
| Disjunction | `or` `∨` `+` `∥`|
| Conjunction | `and` `∧` `·` `&`|

> The exact parser grammar can be found in [pcaparser](https://github.com/p2424630/PCA/blob/main/pca_main/pcaparser.py)

***

## License

> More info can be found [here](https://github.com/p2424630/PCA/blob/main/LICENSE)

The project is licenced under MIT.

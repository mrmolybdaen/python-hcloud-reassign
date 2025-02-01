# Quality assurance

We try to implement different levels of testing.

## Linters and code style

We use `pylint` and `flake8` for linting and code styling.
`flake8` uses different plugins such as:
- bandit
- black
- bugbear
- docstrings

## unit tests

We use the `pytest` module to provide unit tests.
See units/README.md for further information.

## integration

We try to provide integration tests where possible.
See integration/README.md for further information.

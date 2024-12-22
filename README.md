# MapAction Salesforce Experiments

Experiment to programmatically manage Salesforce data.

## Usage

```
$ poetry run python -m streamlit run src/sf_demo/__main__.py
```

## Developing

### Local development environment

Requirements:

* [pyenv](https://github.com/pyenv/pyenv)
* [Poetry](https://python-poetry.org/docs/#installation) (1.8+)
* Git (`brew install git`)
* Pre-commit (`pipx install pre-commit`)

```
$ git clone ...
$ cd sf-demo/
$ pyenv install 3.12
$ poetry install
$ pre-commit install
```

Copy and update `.env.example` as `.env`.

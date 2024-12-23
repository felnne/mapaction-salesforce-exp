# MapAction Salesforce Experiments

Experiment to programmatically manage Salesforce data.

## Usage

```
$ uv run -- streamlit run main.py
```

## Developing

### Local development environment

Requirements:

* [UV](https://docs.astral.sh/uv) (`brew install uv`)
* [Git](https://git-scm.com) (`brew install git`)
* [Pre-commit](https://pre-commit.com) (`uv tool install pre-commit`)

```
$ git clone ...
$ cd sf-exp/
$ pre-commit install
```

**Note:** UV will automatically create a Python virtual environment for the project at runtime.

Copy and update `.env.example` as `.env`.

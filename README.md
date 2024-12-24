# MapAction Salesforce Experiments

Experiment to programmatically manage Salesforce data.

## Usage

```
$ uv run -- streamlit run main.py
```

## Setup

1. create a ?Salesforce app? in a test Salesforce instance:
    - ...
2. create a Google OAuth application
    - from https://console.cloud.google.com/ -> Google Auth Platform -> Clients -> Create Client
    - application type: *Web application*
    - name: `felnne-salesforce-exp`
    - authorised JavaScript origins:
      - `http://localhost:8501`
    - authorised redirect URIs:
      - `http://localhost:8501/component/streamlit_oauth.authorize_button/index.html`

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
$ cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Update any 'xxx' values in `.streamlit/secrets.toml`.

**Note:** UV will automatically create a Python virtual environment for the project at runtime.


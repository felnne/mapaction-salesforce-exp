# MapAction Salesforce Automation Experiments

Experiment to programmatically access and manage Salesforce data.

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

Setup project:

```
$ git clone https://github.com/felnne/mapaction-salesforce-exp
$ cd mapaction-salesforce-exp/
$ pre-commit install
$ cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Update any 'xxx' values in `.streamlit/secrets.toml`.

**Note:** UV will automatically create a Python virtual environment for the project at runtime.

# License

Copyright (c) 2024 MapAction.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

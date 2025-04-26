# MapAction Salesforce Automation Experiments

Experiment to programmatically access and manage Salesforce data.

## Usage

https://felnne-ma-sf-exp.streamlit.app/

## Setup

1. create a ?Salesforce app? in a test Salesforce instance:
    - ...
2. create a Google OAuth application
    - from https://console.cloud.google.com/ -> Google Auth Platform -> Clients -> Create Client
    - application type: *Web application*
    - name: `felnne-salesforce-exp`
    - authorised JavaScript origins:
      - `http://localhost:8501`
      - `https://felnne-ma-sf-exp.streamlit.app`
    - authorised redirect URIs:
      - `http://localhost:8501/oauth2callback`
      - `https://felnne-ma-sf-exp.streamlit.app/oauth2callback`
3. create a Streamlit Community Cloud deployment
    - push code to GitHub
    - if needed, create a Streamlit Community Cloud account and authorise GitHub integration
    - create a new Streamlit app:
      - deployment type: *deploy a public app from GitHub*
      - repository: (as setup in GitHub)
      - branch: `main`
      - main file path: `main.py`
      - app URL: `felnne-ma-sf-exp`
      - (advanced settings) Python version: 3.12
      - (advanced settings) secrets:
        - as per `.streamlit/secrets.toml.example`
        - set `env.platform` to `streamlit`
        - set `auth.redirect_uri` to `https://felnne-ma-sf-exp.streamlit.app/oauth2callback`
        - set `auth.cookie_secret` to a cryptographically secure random string (e.g. using `openssl rand -base64 128`)

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

Update any 'xxx' values in `.streamlit/secrets.toml`. For the cookie secret, generate a cryptographically secure random
string (e.g. using `openssl rand -base64 128`).

**Note:** UV will automatically create a Python virtual environment for the project at runtime.

Run app:

```
$ uv run -- streamlit run main.py
```

## Releasing

To create a release:

```
$ scripts/create-release.py [major|minor|patch|prerelease]
```

Create tag and push `main` branch to GitHub.

## Deployment

The Streamlit GitHub integration will automatically deploy pushed commits to the Streamlit Community Cloud.

# License

Copyright (c) 2024-2025 MapAction.

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

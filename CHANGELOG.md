# MapAction Salesforce Automation Experiments - Change log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

* Adjusting app to match changes to Streamlit auth

### Changed

* Upgrading release script

## [0.4.0] - 2024-12-27

### Added

* Release script

## [0.3.6] - 2024-12-26

### Added

* Experiment information section
* Watchdog dependency for running Streamlit locally

### Changed

* Bypassing/faking OAuth when deployed to Streamlit Community Cloud (not yet supported)

## [0.3.5] - 2024-12-26

### Changed

* Switching OAuth provider package to https://github.com/kajarenc/stauthlib to resolve auth issues in deployment
* Rearranging streamlit app

## [0.3.4] - 2024-12-25

### Changed

* Downgrading Python version to 3.12 to match deployment version
* Rearranging app

## [0.3.3] - 2024-12-25

### Fixed

- Attempting to fix OAuth pop-up URL when deployed
- Attempting to fix module resolution errors when deployed

## [0.3.2] - 2024-12-25

### Fixed

- Attempting to fix OAuth pop-up URL when deployed

## [0.3.1] - 2024-12-25

### Fixed

- Docs usage section
- Attempting to fix OAuth pop-up URL when deployed

## [0.3.0] - 2024-12-25

### Added

- Project change log

### Fixed

- Only showing balloons when user first signs in

### Changed

- Refactoring non-streamlit specific models and clients into separate modules
- Updating docs

## [0.2.0] - 2024-12-24

### Added

- Project licence

### Changed

- Switching to Streamlit secrets

## [0.1.0] - 2024-12-23

### Added

- Initial experiment using Streamlit as a framework with Google OAuth and Simple Salesforce SDK

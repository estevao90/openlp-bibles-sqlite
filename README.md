# openlp-bibles-sqlite

Web Scraping from bible.com to generate sqlite files to OpenLP software.

## Development

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![Actions Status](https://github.com/estevao90/openlp-bibles-sqlite/workflows/Tests/badge.svg)](https://github.com/estevao90/openlp-bibles-sqlite/actions?query=workflow%3ATests+branch%3Amaster+)

## Dependencies

```shell
# install pipenv globally
sudo pip install pipenv -U

# create project virtualenv
pipenv install --dev

# active virtualenv
pipenv shell
```

## Helpful developer commands

```shell
# lint
pylint --load-plugins pylint_quotes src/*
```

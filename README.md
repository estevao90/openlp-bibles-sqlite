# openlp-bibles-sqlite

Web Scraping from bible.com to generate sqlite files to OpenLP software.

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![Integration](https://github.com/estevao90/openlp-bibles-sqlite/actions/workflows/integration.yml/badge.svg)](https://github.com/estevao90/openlp-bibles-sqlite/actions/workflows/integration.yml)

## Usage

```bash
# install environment
pipenv install

# edit configurations in config.ini file

# run script
pipenv run python src/app.py 
```

## Development

### Dependencies

```shell
# create virtualenv
pipenv install --dev

# run shell
pipenv shell
```

### Helpful developer commands

```shell
# lint
pipenv run pylint --load-plugins pylint_quotes src/*
```

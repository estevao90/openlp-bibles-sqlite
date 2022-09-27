# openlp-bibles-sqlite

Web Scraping from bible.com to generate SQLite files to the OpenLP software.

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

### Parameters

| Parameter           | Description                                                                                                                                                                                                              | Default                                   |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------- |
| `sqlite.path`       | Path for the SQLite file that should be saved.                                                                                                                                                                           | `ARC.sqlite`                              |
| `bible.name`        | Name of the Bible version.                                                                                                                                                                                               | `Almeida Revista e Corrigida`             |
| `bible.copyright`   | Copyright text.                                                                                                                                                                                                          | `ARC © 2009 Sociedade Bíblica do Brasil.` |
| `bible.id`          | ID of the bible version. You can get it from the bible URL. Example: if the URL is <https://www.bible.com/pt/bible/212/GEN.1.ARC>, so the ID is 212.                                                                     | `212`                                     |
| `bible.initial_ref` | Initial book and chapter that you want to start the scraping. For a complete scraping, you can use the default `GEN.1` to start from the first book and chapter or put the book and chapter that you want to start from. | `GEN.1`                                   |

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

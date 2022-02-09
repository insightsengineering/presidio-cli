# presidio-cli

CLI tool that analyzes text for PII Entities with [Microsoft Presidio framework](https://github.com/microsoft/presidio).

## Prerequisities

`Python` version: 3.8, 3.9, 3.10

`pipenv` app installed:

```shell
# check if app is installed
pipenv --version

# install, if not available
pip install pipenv
```

## Install `presidio-cli` in a virtual env

### Install from Python Package Index

install in current python env

```shell
python -m pip install presidio-cli
```

install required apps and presidio-cli in virtual environment

```shell
pipenv install presidio-cli
```

### Install from source

```shell
# clone from git
git clone https://github.com/insightsengineering/presidio-cli
cd presidio-cli
# install required apps and presidio-cli
pipenv install --deploy --dev
```

## Install language models for `spaCy`

Load models for the English (en) language using the command presented below. For further information please visit section [models](https://spacy.io/models/en).

```shell
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_lg
```

## Configuration file syntax

The default configuration is taken from the `.presidiocli` file in a current directory.

Configuration file supports the following parameters in a yaml file:

- language - by default only models and recognizers for `en` are available.
 The list of [languages](https://microsoft.github.io/presidio/analyzer/languages/) can be extended.

- entities - limit list of recognized entities to be listed in parameter. It is mapped directly to `presidio framework`.
  List of [supported entities](https://microsoft.github.io/presidio/supported_entities/)

- ignore - list of ignored files/folders based on pattern. It is recommended to ignore `Version Control` files, for example `.git`

Note: a file requires at least one parameter to be set.

An example of yaml configuration file content:

```yaml
---
language: en
ignore: |
  .git
  *.cfg
entities:
  - PERSON
  - CREDIT_CARD
  - EMAIL_ADDRESS

```

## Run presidio_cli

Run presidio_cli to execute [Presidio Analyzer](https://microsoft.github.io/presidio/analyzer/) 
with specified configuration: language,  entities and ignore pre-configured files/paths.

### Configuration from a file

An example of running script with configuration from a file.

There are two example `.yaml` configuration files in config folder:

- default.yaml - ignore `.git` folder
- limited.yaml - limit list of entities used to only 3 of them, ignore `.git` folder and `.cfg` files.  

```shell
# run with default configuration (file `.presidiocli`) in current folder
pipenv run python -m presidio_cli .

# run with configuration limited.yaml in folder tests
pipenv run python -m presidio_cli -c presidio_cli/conf/limited.yaml tests/

# run with configuration limited.yaml in single file only tests/test_analyzer.py
pipenv run python -m presidio_cli -c presidio_cli/conf/limited.yaml tests/test_analyzer.py

```

### Configuration as a parameter

An example of using configuration as data in parameter:

```shell
# ignore paths .git and *.cfg
pipenv run python -m presidio_cli -d "ignore: |
  .git
  *.cfg" tests/

# limit list of entities to CREDIT_CARD
pipenv run python -m presidio_cli -d "entities:
  - CREDIT_CARD" tests/

# equivalent to use -c parameter 
pipenv run python -m presidio_cli -d "$(cat presidio_cli/conf/limited.yaml)" tests/

```

### Formatting output

Output can be formatted using `-f` or `--format` parameter. The default format is `auto`.

Available formats:

- standard - standard output format

```shell
pipenv run python -m presidio_cli -d "entities:
  - PERSON" -f standard tests/conftest.py
# result
tests/conftest.py
  34:58     0.85     PERSON
  37:33     0.85     PERSON
```

- github - similar to diff function in github

```shell
pipenv run python -m presidio_cli -d "entities:
  - PERSON" -f github tests/conftest.py
# result
::group::tests/conftest.py
::0.85 file=tests/conftest.py,line=34,col=58::34:58 [PERSON] 
::0.85 file=tests/conftest.py,line=37,col=33::37:33 [PERSON] 
::endgroup::
```

- colored - standard output format but with colors

- parsable - easy to parse automaticaly

```shell
pipenv run python -m presidio_cli -d "entities:
  - PERSON" -f parsable tests/conftest.py
# result
{"entity_type": "PERSON", "start": 57, "end": 62, "score": 0.85, "analysis_explanation": null}
{"entity_type": "PERSON", "start": 32, "end": 37, "score": 0.85, "analysis_explanation": null}
```

- auto - default format, switches automatically between those 2 modes:
  - github, if run on github - environment variables `GITHUB_ACTIONS` and `GITHUB_WORKFLOW` are set
  - colored, otherwise

### List of all parameters

```shell
# inside virtual env shell
pipenv shell
python -m presidio_cli --help

# run outside virtual env
pipenv run python -m presidio_cli --help

# run outside as shell command
pipenv run presidio --help

```

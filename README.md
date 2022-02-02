# presidio_cli

CLI tool that analyze Text for PII Entities with [Microsoft Presidio framework](https://github.com/microsoft/presidio).

## Prerequisities

`Python` version: 3.8, 3.9, 3.10

`pipenv` app is installed:

```shell
# check if app is installed
pipenv --version

# install, if not available
pip install pipenv
```

## Install `presidio_cli` module to the virtual env

```shell
# install required apps
pipenv install --deploy --dev
```

## Configuration file syntax

Default configuration is taken from `.presidiocli` file in current directory.

Configuration file support parameters in yaml file:
  - language - by default only models and recognizers for `en` are available. 
  [languages](https://microsoft.github.io/presidio/analyzer/languages/) list can be extended.
  - entities - limit list of recognized entites to listed in parameter. It is mapped directly to `presidio framework`.
  List of [supported entities](https://microsoft.github.io/presidio/supported_entities/)
  - ignore - list of ignored files/folders based on pattern. It is recommended to ignore `Version Control` files, for example `.git`

File require at least one parameter to be set.

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
## Run

Run presidio_cli

### Configuration from file

Example of running script with configuration from a file

```shell
# run with default configuration (file `.presidiocli`) in current folder
pipenv run python -m presidio_cli .

# run with configuration limited.yaml in folder tests
pipenv run python -m presidio_cli -c presidio_cli/conf/limited.yaml tests/

# run with configuration limited.yaml in single file only tests/test_analyzer.py
pipenv run python -m presidio_cli -c presidio_cli/conf/limited.yaml tests/test_analyzer.py

```

### Configuration as paramter

Example of use configuration as data in parameter

```shell
# ignore paths .git and *.cfg
pipenv run python -m presidio_cli -d "ignore: |
  .git
  *.cfg" tests/

# limit list of entieties to CREDIT_CARD
pipenv run python -m presidio_cli -d "entities:
  - CREDIT_CARD" tests/

# equivalent to use -c parameter 
pipenv run python -m presidio_cli -d "$(cat presidio_cli/conf/limited.yaml)" tests/

```

### Formatting output

Output can be formatted using `-f` or `--format` parameter. Default format `auto`.
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
  - github - a little bit like a diff
  ```shell
pipenv run python -m presidio_cli -d "entities:
  - PERSON" -f github tests/conftest.py
# result
::group::tests/conftest.py
::0.85 file=tests/conftest.py,line=34,col=58::34:58 [PERSON] 
::0.85 file=tests/conftest.py,line=37,col=33::37:33 [PERSON] 
::endgroup::
  ```
  - colored - like a standard but with colors
  - parsable - easy to parse automaticaly
```shell
pipenv run python -m presidio_cli -d "entities:
  - PERSON" -f parsable tests/conftest.py
# result
{"entity_type": "PERSON", "start": 57, "end": 62, "score": 0.85, "analysis_explanation": null}
{"entity_type": "PERSON", "start": 32, "end": 37, "score": 0.85, "analysis_explanation": null}
```
  - auto - default format, switch automatically between those 2 modes:
    - github, if run on github - environment variables `GITHUB_ACTIONS` and `GITHUB_WORKFLOW` are set
    - colored, otherwise
 
### List all parameters

```shell
# inside virtual env shell
pipenv shell
python -m presidio_cli --help

# run outside virtual env
pipenv run python -m presidio_cli --help

```

# presidio-cli

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

## Install module to the virtual env

```shell
# install required apps
pipenv install --deploy --dev
```

## Run
Example of running script.
### To list all supported cli parameters

```shell
# inside virtual env shell
pipenv shell
python -m presidio_cli --help

# run outside virtual env
pipenv run python -m presidio_cli --help

```


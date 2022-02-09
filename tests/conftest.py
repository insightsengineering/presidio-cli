import pytest
import tempfile
import os

import spacy
from spacy.cli import download
from presidio_cli.config import PresidioCLIConfig


def build_temp_workspace(files):
    tempdir = tempfile.mkdtemp(prefix="presidiocli-tests-")

    for path, content in files.items():
        path = os.path.join(tempdir, path).encode("utf-8")
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        if type(content) is list:
            os.mkdir(path)
        else:
            mode = "wb" if isinstance(content, bytes) else "w"
            with open(path, mode) as f:
                f.write(content)

    return tempdir


@pytest.fixture()
def temp_workspace():
    tmpdir = build_temp_workspace(
        {
            "empty.txt": "",
            "sub/directory.txt/empty.txt": "",
            "s/s/s/s/s/s/s/s/s/s/s/s/s/s/s/file": "Hello Paulo Santos.\n"
            "The latest statement for your credit card account 4111 1111 1111 1111\n"
            "was mailed to 123 Any Street, Seattle, WA 98109.\n",
            "errorfile": "Hello Paulo Santos.\n"
            "The latest statement for your credit card account 122000000000003\n"
            "The latest statement for 55-5555-5555-5544-44\n"
            "The fake card example from presidio test 5555 5555 5555 44 44"
            "The latest statement for 5555555555554444\n"
            "was mailed to 123 Any Street, Seattle, WA 98109.\n",
            # non-ASCII chars
            u"non-ascii/éçäγλνπ¥/utf-8": (
                u"---\n"
                u"- hétérogénéité\n"
                u"# 19.99 €\n"
                u"- お早う御座います。\n"
                u"# الأَبْجَدِيَّة العَرَبِيَّة\n"
            ).encode("utf-8"),
            # dos line endings yaml
            "dos.yml": "---\r\n" "credit_card: 122000000000003",
        }
    )
    with open(os.path.join(tmpdir, "binary_file"), "wb") as fout:
        fout.write(os.urandom(1024))
    return tmpdir


@pytest.fixture()
def config():
    config = PresidioCLIConfig(content="extends: default")
    return config


@pytest.fixture()
def config_pl():
    config_pl = PresidioCLIConfig(content=
#    "entities:\n"
#        "  - OSOBA\n"
#        "  - IP_ADDRESS\n"
#        "  - CREDIT_CARD\n"
        "treshold: 1.0\n"
        "language: pl\n"
        "locale: pl_PL.UTF-8\n"
        )
    return config_pl

@pytest.fixture()
def config_es():
    config_es = PresidioCLIConfig(content=
        "treshold: 1.0\n"
        "language: es\n"
        )
    return config_es


@pytest.fixture(scope="session")
def en_core_web_lg():
    try:
        spacy.load("en_core_web_lg")
    except OSError:
        # downloads model if is not installed yet
        print(download("en_core_web_lg"))


@pytest.fixture(scope="session")
def pl_core_news_lg():
    try:
        spacy.load("pl_core_news_lg")
    except OSError:
        # downloads model if is not installed yet
        print(download("pl_core_news_lg"))
#    try:
#        spacy.load("pl_core_news_md")
#    except OSError:
        # downloads model if is not installed yet
#        print(download("pl_core_news_md"))

@pytest.fixture(scope="session")
def es_core_news_lg():
    try:
        spacy.load("es_core_news_lg")
    except OSError:
        # downloads model if is not installed yet
        print(download("es_core_news_lg"))
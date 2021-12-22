import pytest

import spacy
from spacy.cli import download


@pytest.fixture(scope="session")
def en_core_web_lg():
    try:
        spacy.load("en_core_web_lg")
    except OSError:
        # downloads model if is not instlled yet
        print(download("en_core_web_lg"))

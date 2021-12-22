from presidio_cli.analyzer import analyze
from presidio_cli.cli import PII_ENTITIES


TEXT_TO_ANALYZE = """His name is Mr. Jones and his phone number is 212-555-5555
Hi my name is Charles Darwin and my email is cdarwin@hmsbeagle.org

"""


def test_analyze(en_core_web_lg):

    expected = [
        {
            "entity_type": "EMAIL_ADDRESS",
            "start": 104,
            "end": 125,
            "score": 1.0,
            "analysis_explanation": None,
            "file_path": None,
        },
        {
            "entity_type": "DOMAIN_NAME",
            "start": 112,
            "end": 125,
            "score": 1.0,
            "analysis_explanation": None,
            "file_path": None,
        },
        {
            "entity_type": "PERSON",
            "start": 16,
            "end": 21,
            "score": 0.85,
            "analysis_explanation": None,
            "file_path": None,
        },
        {
            "entity_type": "PERSON",
            "start": 73,
            "end": 87,
            "score": 0.85,
            "analysis_explanation": None,
            "file_path": None,
        },
        {
            "entity_type": "PHONE_NUMBER",
            "start": 46,
            "end": 58,
            "score": 0.75,
            "analysis_explanation": None,
            "file_path": None,
        },
    ]

    result = list(analyze(TEXT_TO_ANALYZE, PII_ENTITIES))

    assert expected == result

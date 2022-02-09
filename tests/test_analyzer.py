import pytest
from presidio_cli.analyzer import analyze, line_generator


def test_line_generator():

    e = list(line_generator(""))
    assert len(e) == 1
    assert e[0].line_no == 1
    assert e[0].start == 0
    assert e[0].end == 0

    e = list(line_generator("\n"))
    assert len(e) == 2

    e = list(line_generator(" \n"))
    assert len(e) == 2
    assert e[0].line_no == 1
    assert e[0].start == 0
    assert e[0].end == 1

    e = list(line_generator("\n\n"))
    assert len(e) == 3

    e = list(line_generator("---\n" "this is line 1\n" "line 2\n" "\n" "3\n"))
    assert len(e) == 6
    assert e[0].line_no == 1
    assert e[0].content == "---"
    assert e[2].content == "line 2"
    assert e[3].content == ""
    assert e[5].line_no == 6

    e = list(line_generator("test with\n" "no newline\n" "at the end"))
    assert len(e) == 3
    assert e[2].line_no == 3
    assert e[2].content == "at the end"


def test_analyze(en_core_web_lg, config):

    result = list(
        analyze(
            "His name is Mr. Jones and his phone number is 212-555-5555\n"
            "Hi my name is Charles Darwin and\n"
            "my email is cdarwin@hmsbeagle.org\n",
            config,
        )
    )

    assert len(result) == 5


def test_analyze_type_error(en_core_web_lg, config):
    with pytest.raises(TypeError):
        analyze({}, config)


def test_analyze_pl(pl_core_news_lg, config_pl):
    result = list(
        analyze(
            "Mam na imię Jan Nowak a mój numer telefonu to 212-555-5555\n"
            "Cześć, Mam na imię Jan Nowak i\n"
            "mój email to cdarwin@hmsbeagle.org.pl\n",
            config_pl,
        )
    )
    for res in result:
        print(f"{res.recognizer_result}")
    assert len(result) == 6


def test_analyze_pl_by_en(en_core_web_lg, config_pl):
    result = list(
        analyze(
            "Mam na imię Jan Nowak a mój numer telefonu to 212-555-5555\n"
            "Cześć, Mam na imię Jan Nowak i\n"
            "mój email to cdarwin@hmsbeagle.org.pl\n",
            config_pl,
        )
    )
    for res in result:
        print(f"{res.recognizer_result}")
    assert len(result) == 6


def test_analyze_es(es_core_news_lg, config_es):
    result = list(
        analyze(
            "Mam na imię Jan Nowak a mój numer telefonu to 212-555-5555\n"
            "Cześć, Mam na imię Jan Nowak i\n"
            "mój email to cdarwin@hmsbeagle.org.pl\n",
            config_es,
        )
    )
    for res in result:
        print(f"{res.recognizer_result}")
    assert len(result) == 6

import argparse
import os
import sys
import io
import locale


from presidio_cli import APP_NAME, APP_DESCRIPTION
from presidio_cli.analyzer import analyze
from presidio_cli.config import PresidioCLIConfig, PresidioCLIConfigError


class Format(object):
    @staticmethod
    def parsable(problem, filename):
        return "%(file)s:%(line)s:%(column)s: [%(score)s] %(type)s" % {
            "file": filename,
            "line": problem.line,
            "column": problem.column,
            "score": problem.score,
            "type": problem.type,
        }

    @staticmethod
    def standard(problem, filename):
        line = "  %d:%d" % (problem.line, problem.column)
        line += max(12 - len(line), 0) * " "
        line += problem.score
        line += max(21 - len(line), 0) * " "
        line += problem.type
        if problem.explanation:
            line += "  (%s)" % problem.explanation
        return line

    @staticmethod
    def standard_color(problem, filename):
        line = "  \033[2m%d:%d\033[0m" % (problem.line, problem.column)
        line += max(20 - len(line), 0) * " "
        if problem.score < 1:  # warning
            line += "\033[33m%s\033[0m" % problem.score
        else:
            line += "\033[31m%s\033[0m" % problem.score
        line += max(38 - len(line), 0) * " "
        line += problem.type
        if problem.explanation:
            line += "  \033[2m(%s)\033[0m" % problem.explanation
        return line

    @staticmethod
    def github(problem, filename):
        line = "::"
        line += problem.score
        line += " file=" + filename + ","
        line += "line=" + format(problem.line) + ","
        line += "col=" + format(problem.column)
        line += "::"
        line += format(problem.line)
        line += ":"
        line += format(problem.column)
        line += " "
        line += "[" + problem.type + "] "
        if problem.explanation:
            line += problem.explanation
        return line


def show_problems(problems, file, args_format=None, no_warn=None):
    i = 0
    for problem in problems:
        print(problem)
        i += i
    return i


def find_files_recursively(items, conf):
    for item in items:
        if os.path.isdir(item):
            for root, dirnames, filenames in os.walk(item):
                for f in filenames:
                    filepath = os.path.join(root, f)
                    if conf.is_text_file(filepath):
                        yield filepath
        else:
            yield item


def run(argv=None):
    parser = argparse.ArgumentParser(
        prog=APP_NAME, description=APP_DESCRIPTION
    )

    files_group = parser.add_mutually_exclusive_group(required=True)
    files_group.add_argument(
        "files",
        metavar="FILE_OR_DIR",
        nargs="*",
        default=(),
        help="files to check",
    )
    files_group.add_argument(
        "-", action="store_true", dest="stdin", help="read from standard input"
    )

    config_group = parser.add_mutually_exclusive_group()
    config_group.add_argument(
        "-c",
        "--config-file",
        dest="config_file",
        action="store",
        help="path to a custom configuration",
    )
    config_group.add_argument(
        "-d",
        "--config-data",
        dest="config_data",
        action="store",
        help="custom configuration (as YAML source)",
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=("standard", "github", "auto"),
        default="auto",
        help="format for parsing output",
    )

    parser.add_argument(
        "--no-warnings",
        action="store_true",
        help="output only error level problems",
    )

    args = parser.parse_args()

    try:
        if args.config_data is not None:
            if args.config_data != "" and ":" not in args.config_data:
                args.config_data = "extends: " + args.config_data
            conf = PresidioCLIConfig(content=args.config_data)
        elif args.config_file is not None:
            conf = PresidioCLIConfig(file=args.config_file)
        elif os.path.isfile(".presidiocli"):
            conf = PresidioCLIConfig(file=".presidiocli")
    except PresidioCLIConfigError as e:
        print(e, file=sys.stderr)
        sys.exit(-1)

    if conf.locale is not None:
        locale.setlocale(locale.LC_ALL, conf.locale)

    for file in find_files_recursively(args.files, conf):
        filepath = file[2:] if file.startswith("./") else file
        try:
            with io.open(file, newline="") as f:
                problems = analyze(f, conf, filepath)
        except EnvironmentError as e:
            print(e, file=sys.stderr)
            sys.exit(-1)
        prob_num = show_problems(
            problems, file, args_format=args.format, no_warn=args.no_warnings
        )

    if args.stdin:
        try:
            problems = analyze(sys.stdin, conf, "")
        except EnvironmentError as e:
            print(e, file=sys.stderr)
            sys.exit(-1)
        prob_num = show_problems(
            problems,
            "stdin",
            args_format=args.format,
            no_warn=args.no_warnings,
        )

    if prob_num > 0:
        return_code = 1
    else:
        return_code = 0
    sys.exit(return_code)

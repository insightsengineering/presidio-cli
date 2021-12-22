from presidio_analyzer import AnalyzerEngine


class Line(object):
    def __init__(self, line_no, buffer, start, end):
        self.line_no = line_no
        self.start = start
        self.end = end
        self.buffer = buffer

    @property
    def content(self):
        return self.buffer[self.start : self.end]


def line_generator(buffer):
    line_no = 1
    cur = 0
    next = buffer.find("\n")
    while next != -1:
        if next > 0 and buffer[next - 1] == "\r":
            yield Line(line_no, buffer, start=cur, end=next - 1)
        else:
            yield Line(line_no, buffer, start=cur, end=next)
        cur = next + 1
        next = buffer.find("\n", cur)
        line_no += 1

    yield Line(line_no, buffer, start=cur, end=len(buffer))


def _analyze(buffer, conf, filepath):
    """Analyze a text source.
    Returns a generator of LintProblem objects.
    :param buffer: buffer, string or stream to read from
    :param conf: list, list of strings with presidio supported entities #TODO
    :param filepath: string, string with path to file
    """
    assert hasattr(
        buffer, "__getitem__"
    ), "_run() argument must be a buffer, not a stream"

    analyzer = AnalyzerEngine()

    for problem in analyzer.analyze(
        text=buffer, entities=conf.entities, language=conf.language
    ):
        problem = problem.to_dict()
        problem["file_path"] = filepath
        yield problem


def analyze(input, conf, filepath=None):
    """Analyze a text source.
    Returns a generator of LintProblem objects.
    :param input: buffer, string or stream to read from
    :param conf: list, list of strings with presidio supported entities #TODO
    :param filepath: string, string with path to file
    """

    # TODO: Read line by line
    if isinstance(input, (bytes, str)):
        return _analyze(input, conf, filepath)
    elif hasattr(input, "read"):  # Python 2's file or Python 3's io.IOBase
        # We need to have everything in memory to parse correctly
        content = input.read()
        return _analyze(content, conf, filepath)
    else:
        raise TypeError("input should be a string or a stream")

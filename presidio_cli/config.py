import mimetypes
import yaml
import pathspec
import os
from presidio_analyzer import AnalyzerEngine


class PresidioCLIConfigError(Exception):
    pass


class PresidioCLIConfig(object):
    def __init__(self, content=None, file=None):
        assert (content is None) ^ (file is None)

        self.ignore = None

        self.locale = None

        self.analyzer = AnalyzerEngine()

        self.treshold = None

        self.language = "en"

        if file is not None:
            with open(file) as f:
                content = f.read()

        self.parse(content)
        self.validate()

    def is_file_ignored(self, filepath):
        return self.ignore and self.ignore.match_file(filepath)

    def is_text_file(self, filepath):
        mime = mimetypes.guess_type(filepath)
        if mime[0] is not None:
            if mime[0].startswith("text"):
                return True
        return False

    def extend(self, base_config):
        assert isinstance(base_config, PresidioCLIConfig)

        # Create list with unique entries
        if base_config.entities is not None:
            self.entities = list(set(base_config.entities + self.entities))

        if base_config.ignore is not None:
            self.ignore = base_config.ignore

    def parse(self, raw_content):
        try:
            conf = yaml.safe_load(raw_content)
        except Exception as e:
            raise PresidioCLIConfigError("invalid config: %s" % e)

        if not isinstance(conf, dict):
            raise PresidioCLIConfigError("invalid config: not a dict")

        self.entities = conf.get("entities", {})

        if "treshold" in conf:
            self.treshold = conf["treshold"]
        if "language" in conf:
            self.language = conf["language"]
        if "extends" in conf:
            path = get_extended_config_file(conf["extends"])
            base = PresidioCLIConfig(file=path)
            try:
                self.extend(base)
            except Exception as e:
                raise PresidioCLIConfigError("invalid config: %s" % e)

        if "ignore" in conf:
            if not isinstance(conf["ignore"], str):
                raise PresidioCLIConfigError(
                    "invalid config: ignore should contain file patterns"
                )
            self.ignore = pathspec.PathSpec.from_lines(
                "gitwildmatch", conf["ignore"].splitlines()
            )

        if "locale" in conf:
            if not isinstance(conf["locale"], str):
                raise PresidioCLIConfigError(
                    "invalid config: locale should be a string"
                )
            self.locale = conf["locale"]

    def validate(self):
        for id in self.entities:
            try:
                assert id in self.analyzer.get_supported_entities()
            except Exception as e:
                raise PresidioCLIConfigError("invalid config: %s" % e)


def get_extended_config_file(name):
    # Is it a standard conf shipped with yamllint...
    if "/" not in name:
        std_conf = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "conf", name + ".yaml"
        )

        if os.path.isfile(std_conf):
            return std_conf

    # or a custom conf on filesystem?
    return name

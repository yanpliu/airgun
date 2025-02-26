import logging
import os
from configparser import ConfigParser


SETTINGS_FILE_NAME = 'settings.ini'


def get_project_root():
    """Return the path to the project root directory.

    :return: A directory path.
    :rtype: str
    """
    return os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
        )
    )


class AirgunSettings:
    def __init__(self):
        self.verbosity = None
        self.tmp_dir = None


class SatelliteSettings:
    def __init__(self):
        self.hostname = None
        self.username = None
        self.password = None


class SeleniumSettings:
    def __init__(self):
        self.browser = None
        self.screenshots_path = None
        self.webdriver = None
        self.webdriver_binary = None
        self.browseroptions = None


class WebKaifukuSettings:
    def __init__(self):
        self.config = None


class Settings:
    def __init__(self):
        self.configured = False
        self.airgun = AirgunSettings()
        self.satellite = SatelliteSettings()
        self.selenium = SeleniumSettings()
        self.webkaifuku = WebKaifukuSettings()

    def _configure_logging(self):
        logging.captureWarnings(False)
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=self.airgun.verbosity,
        )
        logging.getLogger('airgun').setLevel(self.airgun.verbosity)

    def _configure_thirdparty_logging(self):
        logging.getLogger('widgetastic_null').setLevel(self.airgun.verbosity)

    def configure(self, settings=None):
        """Parses arg `settings` or settings file if None passed and sets class
        attributes accordingly
        """
        config = ConfigParser()
        # using str instead of optionxform not to .lower() options
        config.optionxform = str
        if settings is not None:
            for section in settings:
                config.add_section(section)
                for key, value in settings[section].items():
                    config.set(section, key, str(value))
        else:
            settings_path = os.path.join(get_project_root(), SETTINGS_FILE_NAME)
            config.read(settings_path)

        for section in config.sections():
            for key, value in config[section].items():
                setattr(getattr(self, section), key, value)

        self._configure_logging()
        self._configure_thirdparty_logging()

        self.configured = True

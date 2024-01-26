import configparser
import os


class ConfigReader:
    """
    Used to read from .properties files
    """

    __propertiesFileName = "app.properties"

    @classmethod
    def get(cls, section: str, name: str, as_type=None) -> str | list | float:
        configParser = configparser.ConfigParser(
            converters={"list": lambda x: [i.strip() for i in x.split(",")]}
        )
        propertiesFilePath = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), f"../{cls.__propertiesFileName}"
            )
        )
        configParser.read(propertiesFilePath)
        if as_type == list:
            return configParser.getlist(section, name)
        elif as_type == float:
            return configParser.getfloat(section, name)
        elif as_type is None:
            return configParser[section][name]
        else:
            raise ValueError(f"Type conversion for '{as_type}' not supported.")

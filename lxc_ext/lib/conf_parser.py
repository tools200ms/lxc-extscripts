import configparser
import os.path


class ConfParser:

    @staticmethod
    def Parse(conf_file='lxcext.conf') -> {}:
        config = configparser.ConfigParser()

        if not os.path.isfile(conf_file):
            print(f"Config file does not exests: {conf_file}")
            exit(2)

        for loaded in config.read(conf_file):
            print(f"File loaded: {loaded}")

        result = {}
        for section in config.sections():
            section_items = {}
            for key, value in config[section].items():
                section_items[key] = value
            result[section] = section_items
        return result



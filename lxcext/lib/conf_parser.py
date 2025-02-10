from typing import Final

import configparser
import importlib
import os.path


class ConfParser:

    DEFAULT_PATH:Final = 'lxcext.conf'
    @staticmethod
    def Parse(conf_file:str) -> {}:
        config = configparser.ConfigParser()

        if not os.path.isfile(conf_file):
            print(f"Config file does not exests: {conf_file}")
            exit(2)

        for loaded in config.read(conf_file):
            print(f"File loaded: {loaded}")

        result = {}
        for section in config.sections():

            if len(section) > 128 or not (section.isalnum() or '_' in section):
                raise SyntaxError("Incorrect section name")

            try:
                # can raise ModuleNotFoundError
                module = importlib.import_module('lxcext.lib.atoms.' + section)
            except ModuleNotFoundError as e:
                raise SyntaxError(f"Wrong section name: {section}") from e

            if section in result:
                raise SyntaxError(f"Redefined section: {section}")

            section_items = {}
            for key, value in config[section].items():
                if len(key) > 128 or not (key.isalnum() or '_' in key):
                    raise SyntaxError(f"Incorrect key name for section {section}")

                try:
                    # can raise 'AttributeError'
                    cls = getattr(module, key)
                except AttributeError as e:
                    raise SyntaxError(f"Wrong key name: '{section}.{key}'") from e

                if key in section_items:
                    raise SyntaxError(f"Redefined key '{key}' from section '{section}'")

                if len(value) > 512:
                    raise SyntaxError(f"Value of {section}.{key} too long!")

                section_items[key] = cls.get(value)

            result[section] = section_items

        return result



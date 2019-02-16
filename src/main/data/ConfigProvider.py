from typing import Dict
import yaml

class ConfigProvider:

    def get_config(self)-> Dict[str, any]:
        raise NotImplementedError()


class YAMLConfigProvider(ConfigProvider):

    def __init__(self, input_path: str):
        with open(input_path, 'r') as stream:
            try:
                self._data = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def get_config(self)-> Dict[str, any]:
        return self._data
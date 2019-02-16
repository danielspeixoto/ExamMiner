from typing import Dict


class ConfigProvider:

    def get_config(self)-> Dict[str, any]:
        raise NotImplementedError()


class YAMLConfigProvider(ConfigProvider):

    def get_config(self)-> Dict[str, any]:
        pass
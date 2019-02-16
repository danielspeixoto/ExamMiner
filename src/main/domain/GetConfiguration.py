from typing import Dict

from data.ConfigProvider import ConfigProvider


class GetConfiguration:

    def __init__(self, provider: ConfigProvider):
        self.provider = provider

    def run(self)-> Dict[str, any]:
        return self.provider.get_config()
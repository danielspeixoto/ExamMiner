from data.ConfigProvider import YAMLConfigProvider

import os

prov = YAMLConfigProvider(os.getcwd() + "/../res/config.yaml")

print(prov.get_config())
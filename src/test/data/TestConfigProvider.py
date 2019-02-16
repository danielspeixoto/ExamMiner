from data.ConfigProvider import YAMLConfigProvider

prov = YAMLConfigProvider("/home/daniel/work/enem-parser (copy 1)/src/test/res/config.yaml")

print(prov.get_config())
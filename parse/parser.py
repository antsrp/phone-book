import configparser

from parse.config import Config

# Парсинг конфиг файла
def config_parse(path) -> Config:
    config = configparser.ConfigParser()
    config.read(path)
    conf = Config()
    if conf.set(config) == False:
        return None

    return conf
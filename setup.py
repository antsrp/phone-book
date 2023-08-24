from parse import parser, config
from storage.storage import NoteStorage
from common.path import PathWorker

# Константы для задания директорий и названий конфигурационных файлов и файлов с данными
CONFIG_DIR, CONFIG_FN = "config", "config.ini" 
STORAGE_DIR, STORAGE_FN, STORAGE_SAMPLE_FN = "data", "data.pbd", "data_sample.pbd"
YES = "yes"

# Функция считывания данных из конфигурационного файла
def setup_config() -> config.Config:
    if PathWorker.is_file_exists(CONFIG_DIR, CONFIG_FN) == False:
        print("Config file {} in directory {} is not exist!".format(CONFIG_FN, CONFIG_DIR))
        return None

    return parser.config_parse(PathWorker.join_to_path(CONFIG_DIR, CONFIG_FN))

# Функция создания переменной класса NoteStorage, который хранит записи и взаимодействует с ними
def create_storage(config) -> NoteStorage:
    fn = STORAGE_SAMPLE_FN if config.Storage.is_sample == YES else STORAGE_FN
    storage = NoteStorage(STORAGE_DIR, fn, config)

    return storage
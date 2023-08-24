from collections import namedtuple
from configparser import ConfigParser

# Класс для работы с конфигурационным файлом
class Config:
    SECTION_OUTPUT = 'Output'
    SECTION_STORAGE = 'Storage'
    OPTION_NOTES_ON_PAGE = 'NotesOnPage'
    OPTION_ENCRYPTED_READ = 'EncryptedRead'
    OPTION_ENCRYPTED_WRITE = 'EncryptedWrite'
    OPTION_IS_SAMPLE = "IsSample"

    Section_Not_Found = "Error: no section %s in config file!"
    Option_Not_Found = "Error: no option %s in section %s in config file!"

    output_options = namedtuple('Output', 'notes_on_page')
    storage_options = namedtuple('Storage', 'encrypted_read encrypted_write is_sample')
    
    def __init__(self):
        self.Output = {}
        self.Storage = {}

    def set(self, config: ConfigParser) -> bool:
        # Проверки существований секций и опций в конфиг файле
        if config.has_section(self.SECTION_OUTPUT) == False:
            print(self.Section_Not_Found % self.SECTION_OUTPUT)
            return False       
        if config.has_section(self.SECTION_STORAGE) == False:
            print(self.Section_Not_Found % self.SECTION_STORAGE)
            return False

        if config.has_option(self.SECTION_OUTPUT, self.OPTION_NOTES_ON_PAGE) == False:
            print(self.Option_Not_Found % (self.OPTION_NOTES_ON_PAGE, self.SECTION_OUTPUT))
            return False
        if config.has_option(self.SECTION_STORAGE, self.OPTION_ENCRYPTED_READ) == False:
            print(self.Option_Not_Found % (self.OPTION_ENCRYPTED_READ, self.SECTION_STORAGE))
            return False
        if config.has_option(self.SECTION_STORAGE, self.OPTION_ENCRYPTED_WRITE) == False:
            print(self.Option_Not_Found % (self.OPTION_ENCRYPTED_WRITE, self.SECTION_STORAGE))
            return False
        if config.has_option(self.SECTION_STORAGE, self.OPTION_IS_SAMPLE) == False:
            print(self.Option_Not_Found % (self.OPTION_IS_SAMPLE, self.SECTION_STORAGE))
            return False

        # Сохранение данных из конфиг файла в переменную класса
        self.Output = self.output_options(config[self.SECTION_OUTPUT][self.OPTION_NOTES_ON_PAGE])
        self.Storage = self.storage_options(config[self.SECTION_STORAGE][self.OPTION_ENCRYPTED_READ], config[self.SECTION_STORAGE][self.OPTION_ENCRYPTED_WRITE], config[self.SECTION_STORAGE][self.OPTION_IS_SAMPLE])

        return True
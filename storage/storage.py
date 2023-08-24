from parse.config import Config
from storage.encoder import NoteEncoder, note_decoder
from storage.note import Note
from common.path import PathWorker
from cryptography.fernet import Fernet
import json

# Константы, определяющие директорию и название файла с ключом шифрования
KEY_DIR, KEY_FN = "key", "fernet.key"
YES = "yes"

class NoteStorage:
    def __init__(self, dir: str, fn: str, config: Config) -> None:
        self.pages_count = int(config.Output.notes_on_page)
        self.encrypted_read = config.Storage.encrypted_read
        self.encrypted_write = config.Storage.encrypted_write

        self.filepath = PathWorker.join_to_path(dir, fn)
        self.keydir = PathWorker.join_to_path(dir, KEY_DIR)
        self.notes: list[Note] = []

        if PathWorker.is_directory_exists(dir) == False:
            PathWorker.create_dir(dir)
            if PathWorker.is_directory_exists(self.keydir) == False:
                PathWorker.create_dir(self.keydir)
                self.__create_key()
        else:
            self.__read_key()
            if PathWorker.is_file_exists(dir, fn) == True:
                self.__read()

    # Добавление записи
    def add(self, note: Note):
        self.notes.append(note)

    # Предоставление списка записей для страницы page
    def list(self, page: int) -> list[Note]:
        start, l = (page - 1)* self.pages_count, self.count
        end = start + self.pages_count if start + self.pages_count < l else l
        
        return self.notes[start:end]

    # Функция, возвращает количество записей
    @property
    def count(self) -> int:
        return len(self.notes)

    # Функция, возвращает количество записей на странице вывода
    @property
    def count_pages(self) -> int:
        return (self.count - 1) // self.pages_count + 1 if self.count > 0 else 0

    # Сохранение записей в файл
    def save(self):
        if self.count > 0:
            self.__write()

    # Чтение записей из файла   
    def __read(self):
        with open(self.filepath, 'r') as f:
            data = f.read()
            if not data:
                return
            try:
                if self.encrypted_read == YES: # Если данные зашифрованы, их необходимо сначала расшифровать
                    fernet = Fernet(self.key)
                    data = fernet.decrypt(data.encode()).decode()
                self.notes = json.loads(data, object_hook=note_decoder) # Перевод данных из JSON в объект записей
            except Exception as error:
                print("can't read data from file!")

    # Запись в файл
    def __write(self):
        try:
            data = json.dumps(self.notes, cls=NoteEncoder)
            if self.encrypted_write == YES: # Если данные необходимо зашифровать
                fernet = Fernet(self.key)
                data = fernet.encrypt(data.encode()).decode()
        except Exception as error:
            print("can't save data file!")
        with open(self.filepath, 'w') as f:
            f.write(data)
    
    # Создание и сохранение в файл ключа шифрования
    def __create_key(self):
        self.key = Fernet.generate_key()
 
        with open(PathWorker.join_to_path(self.keydir, KEY_FN), 'wb') as filekey:
            filekey.write(self.key)

    # Чтение ключа шифрования из файла
    def __read_key(self):
        with open(PathWorker.join_to_path(self.keydir, KEY_FN), 'rb') as filekey:
            self.key = filekey.read()

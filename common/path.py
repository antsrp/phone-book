import os
from warnings import warn

# Класс для работы с директориями и путями
class PathWorker:
    # Директория уже существует?
    def is_directory_exists(dir) -> bool:
        return os.path.isdir(dir)

    # Файл уже существует?
    def is_file_exists(dir, filename) -> bool:
        if PathWorker.is_directory_exists(dir) == False: # если директории не существует
            return False
        
        return os.path.isfile(PathWorker.join_to_path(dir, filename))

    # Добавление к пути path частички part 
    def join_to_path(path, part):
        return os.sep.join([path, part])
    
    # Создание директории
    def create_dir(dir):
        try:
            os.mkdir(dir)
        except Exception as error:
            warn("can't create directory {}: {}".format(dir, error))

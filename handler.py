from storage.note import Note
from storage.storage import NoteStorage

# Константы
INPUT_NOTE_NUMBER, INPUT_COMMAND_NUMBER = "Введите номер изменяемой записи: ", "Введите номер команды: "
INPUT_NOTE_NUMBER_NOT_EXIST, INPUT_COMMAND_NUMBER_NOT_EXIST = "Ошибка: Записи с таким номером не существует!", "Ошибка: команды с таким номером не существует!"

INPUT_OLD_VALUE = "Старое значение поля %s: %s"
INPUT_NEW_VALUE = "Введите новое значение: "

from enum import Enum

# Класс для определения номера команды
class Commands(Enum):
    ADD_NOTE = 1
    EDIT_NOTE = 2
    LIST_NOTES = 3
    QUIT = 4

# Класс для определения изменяемого параметра записи
class EditNoteCommands(Enum):
    EDIT_NOTE_SURNAME = 1
    EDIT_NOTE_NAME = 2
    EDIT_NOTE_PATRONYM = 3
    EDIT_NOTE_ORG = 4
    EDIT_NOTE_PW = 5
    EDIT_NOTE_PD = 6
    EDIT_NOTE_QUIT = 7

# Класс для определения принципа отображения записей 
class ListNoteCommands(Enum):
    LIST_NOTE_PREV = 1
    LIST_NOTE_NEXT = 2
    LIST_NOTE_QUIT = 3

# Функция для вывода строк меню
def print_menu():
    print("")                            
    print("=" * 15)
    print("1: Добавить запись")
    print("2: Изменить запись")
    print("3: Вывести список записей")                   
    print("4: Завершить работу")
    print("=" * 15)
    print("")   

# Функция для вывода строк изменения записи
def print_edit_commands():
    print("")
    print("1: Изменить фамилию")
    print("2: Изменить имя")
    print("3: Изменить отчество")                   
    print("4: Изменить название организации")
    print("5: Изменить рабочий телефон")
    print("6: Изменить личный телефон")
    print("7: Завершить изменение")                   
    print("")

# Функция для вывода строк отображения записей
def print_list_commands():
    print("")
    print("1: Предыдущая страница")
    print("2: Следующая страница")
    print("3: Завершить просмотр")                                   
    print("")

# Функция-обработчик добавления новой записи
def add_note_handler(id: int) -> Note:
    surname = input("Фамилия: ")
    name = input("Имя: ")
    patronym = input("Отчество: ")
    org = input("Название организации: ")
    pw = input("Телефон рабочий: ")
    pd = input("Телефон личный: ")
    return Note(id, surname, name, patronym, org, pw, pd)

# Функция для отображения старого значения параметра записи и считывания нового
def __edit_note_printage(field_name: str, old_value: str) -> str:
    print(INPUT_OLD_VALUE % (field_name, old_value))
    return input(INPUT_NEW_VALUE)

# Функция для определения изменяемого параметра записи
def edit_note_handler(note: Note):
    while True:
        print_edit_commands()
        num = handle_input_number_of_line(INPUT_COMMAND_NUMBER, INPUT_COMMAND_NUMBER_NOT_EXIST, EditNoteCommands.EDIT_NOTE_QUIT.value)
        if num == EditNoteCommands.EDIT_NOTE_SURNAME.value: note.surname = __edit_note_printage("фамилия", note.surname)
        elif num == EditNoteCommands.EDIT_NOTE_NAME.value: note.name = __edit_note_printage("имя", note.name)
        elif num == EditNoteCommands.EDIT_NOTE_PATRONYM.value: note.patronym = __edit_note_printage("отчество", note.patronym)
        elif num == EditNoteCommands.EDIT_NOTE_ORG.value: note.org = __edit_note_printage("название организации", note.org)
        elif num == EditNoteCommands.EDIT_NOTE_PW.value: note.phone_work = __edit_note_printage("телефон рабочий", note.phone_work)
        elif num == EditNoteCommands.EDIT_NOTE_PD.value: note.phone_direct = __edit_note_printage("телефон личный", note.phone_direct)
        elif num == EditNoteCommands.EDIT_NOTE_QUIT.value: return 

# Функция для отображения записей страницы
def __list_notes(notes: list[Note]):
    print("")
    print("%5s|%15s|%15s|%15s|%35s|%20s|%20s|" % ("№".center(5), "Фамилия".center(15), "Имя".center(15), "Отчество".center(15), 
                                                  "Название организации".center(35), "Телефон рабочий".center(20), "Телефон личный".center(20)))
    print("-" * (125 + 7))
    for n in notes:
        print("%5s|%15s|%15s|%15s|%35s|%20s|%20s|" % (str(n.id+1).center(5), n.surname.center(15), n.name.center(15), n.patronym.center(15), 
                                                       n.org.center(35), n.phone_work.center(20), n.phone_direct.center(20)))
    print("")

# Функция для отображения записей по страницам
def list_notes(storage: NoteStorage):
    page, max_page = 1, storage.count_pages
    notes = storage.list(page)
    __list_notes(notes)
    while True:
        print_list_commands()
        num = handle_input_number_of_line(INPUT_COMMAND_NUMBER, INPUT_COMMAND_NUMBER_NOT_EXIST, ListNoteCommands.LIST_NOTE_QUIT.value)
        if num == ListNoteCommands.LIST_NOTE_PREV.value:
            page = page - 1 if page > 1 else max_page 
        elif num == ListNoteCommands.LIST_NOTE_NEXT.value:
            page = page + 1 if page < max_page else 1
        elif num == ListNoteCommands.LIST_NOTE_QUIT.value: return
        notes = storage.list(page)
        __list_notes(notes)

''' Функция-обработчик введенного значения пользователем для запроса input_line. 
В случае, если вводится некорректная команда (значение <=0 или превышает значение max)
выводится строка ошибки error_line, а также перезапускает цикл
'''
def handle_input_number_of_line(input_line: str, error_line: str, max: int) -> int:
    while True:
        try:
            option = int(input(input_line))
            if option <= 0 or option > max:
                print(error_line)            
            else:
                return option
        except ValueError:
            print(error_line)

# Функция-обработчик ввода пользователя
def handle_input(storage: NoteStorage):
    while True:
        print_menu()

        option = handle_input_number_of_line(INPUT_COMMAND_NUMBER, INPUT_COMMAND_NUMBER_NOT_EXIST, Commands.QUIT.value)
            
        if option == Commands.ADD_NOTE.value: 
            id = storage.count
            n = add_note_handler(id)
            storage.add(n)
        elif option == Commands.EDIT_NOTE.value: 
            count = storage.count
            if count == 0:
                print("Невозможно изменить запись, поскольку ни одной еще не было добавлено!")
                continue
            
            id = handle_input_number_of_line(INPUT_NOTE_NUMBER, INPUT_NOTE_NUMBER_NOT_EXIST, count)
            n = storage.notes[id-1]
            edit_note_handler(n)
        elif option == Commands.LIST_NOTES.value: list_notes(storage)
        elif option == Commands.QUIT.value: return
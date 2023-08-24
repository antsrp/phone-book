# Класс записи
class Note:
    def __init__(self, id: int, s: str, n: str, p: str, o: str, pw: str, pd: str) -> None:
        self.id = id
        self.surname = s
        self.name = n
        self.patronym = p
        self.org = o
        self.phone_work = pw
        self.phone_direct = pd
from dataclasses import dataclass


@dataclass
class LottoNum:
    num: str
    per_no: str
    set_no: str
    username: str

    def to_tuple(self):
        return self.num, self.per_no, self.set_no, self.username


@dataclass
class User:
    username: str
    password: str
    name: str
    surname: str
    phone: str

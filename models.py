from dataclasses import dataclass


@dataclass
class LottoNum:
    username: str
    num: str
    per_no: str
    set_no: str


@dataclass
class User:
    username: str
    password: str
    name: str
    surname: str
    phone: str

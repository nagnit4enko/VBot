# Various helpers
from typing import Callable, List
import asyncio

import hues


def schedule(seconds):
    def decor(func):
        async def wrapper(*args, **kwargs):
            while True:
                await asyncio.sleep(seconds)
                await func(*args, **kwargs)

        return wrapper

    return decor


# http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class Attachment(object):
    __slots__ = ('type', 'owner_id', 'id', 'access_key', 'link')

    def __init__(self, attach_type: str, owner_id: int, aid: int, access_key: str, link: str):
        self.type = attach_type
        self.owner_id = owner_id
        self.id = aid
        self.access_key = access_key
        self.link = link

    def as_str(self):
        """Возвращает приложение в формате ownerid_id_accesskey"""
        if self.access_key:
            return f'{self.owner_id}_{self.id}_{self.access_key}'

        return f'{self.owner_id}_{self.id}'

    def __repr__(self):
        return f'{self.type}{self.as_str()}'


class MessageEventData(object):
    __slots__ = ('conf', 'peer_id', 'user_id', 'body', 'time', "msg_id", "attaches")

    def __init__(self, conf: bool, pid: int, uid: int, body: str, time: int, msg_id: int, attaches: List):
        self.conf = conf
        self.peer_id = pid
        self.user_id = uid
        self.body = body
        self.time = time
        self.msg_id = msg_id
        self.attaches = attaches

    def __repr__(self):
        return self.body


def fatal(*args):
    """Отправляет args в hues.error() и выходит"""
    hues.error(*args)
    exit()


# Characters are taken from http://gsgen.ru/tools/perevod-raskladki-online/
ENGLISH = "Q-W-E-R-T-Y-U-I-O-P-A-S-D-F-G-H-J-K-L-Z-X-C-V-B-N-M"
ENG_EXPR = ENGLISH + ENGLISH.lower() + "-" + ":-^-~-`-{-[-}-]-\"-'-<-,->-.-;-?-/-&-@-#-$"
RUS_EXPR = "Й-Ц-У-К-Е-Н-Г-Ш-Щ-З-Ф-Ы-В-А-П-Р-О-Л-Д-Я-Ч-С-М-И-Т-Ь"
rus_expr = RUS_EXPR + RUS_EXPR.lower() + "-" + "Ж-:-Ё-ё-X-x-Ъ-ъ-Э-э-Б-б-Ю-ю-ж-,-.-?-\"-№-;"

ENG_TO_RUS = str.maketrans(ENG_EXPR, rus_expr)
RUS_TO_ENG = str.maketrans(rus_expr, ENG_EXPR)


def convert_to_rus(text: str) -> str:
    """Конвертировать текст, написанный на русском с английской раскладкой в русский"""
    return text.translate(ENG_TO_RUS)


def convert_to_en(text: str) -> str:
    """Конвертировать текст, написанный на русском с русской раскладкой в английскую раскладку"""
    return text.translate(RUS_TO_ENG)


keys = [
    'unread',
    'outbox',
    'replied',
    'important',
    'chat',
    'friends',
    'spam',
    'deleted',
    'fixed',
    'media'
]


def parse_msg_flags(bitmask: int) -> dict:
    """Функция для чтения битовой маски и возврата словаря значений"""
    start = 1
    values = []
    for x in range(1, 11):
        result = bitmask & start
        start *= 2
        values.append(bool(result))
    return dict(zip(keys, values))

import os
from typing import Optional

from json_db import JSONDatabase
from wordy_types import ActiveGame, UserInfo


_db = JSONDatabase(os.getenv('DATABASE_PATH', 'database.json'))


def get_info_for_user(id: int):
    try:
        raw = _db[str(id)]
        return UserInfo.parse_obj(raw)
    except KeyError:
        user = UserInfo()
        _db[str(id)] = user.dict()
        return user


def set_info_for_user(id: int, info: UserInfo):
    _db[str(id)] = info.dict()


def fetch_stored_game(id: int) -> Optional[ActiveGame]:
    user = get_info_for_user(id)
    return user.current_game


def store_game(id: int, game: ActiveGame):
    user = get_info_for_user(id)
    user.current_game = game
    set_info_for_user(id, user)


def clear_game(id: int):
    user = get_info_for_user(id)
    user.current_game = None
    set_info_for_user(id, user)


def write_to_disk():
    _db.save()

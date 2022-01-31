from pprint import pprint
from wordy_types import ActiveGame


_active_games: dict[int, ActiveGame] = {}


def fetch_stored_game(id: int):
    return _active_games.get(id, None)


def store_game(id: int, game: ActiveGame):
    _active_games[id] = game


def clear_game(id: int):
    try:
        del _active_games[id]
    except KeyError:
        pass

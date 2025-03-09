import json
from datetime import date


class GetSession:

    def __init__(self, session_id: int, date_start: date, player_name: str, level_id: int, inf: str):
        self.session_id = session_id
        self.date_start = date_start
        self.player_name = player_name
        self.level_id = level_id
        self.inf = inf


class Player:

    def __init__(self, nickname: str, player_id: int = None):
        self.player_id = player_id
        self.nickname = nickname


class Level:

    def __init__(self, level_id: int, player_start_x: int, player_start_y: int,  level_map: str, places: str = '{}'):
        self.level_id = level_id
        self.player_start_x = player_start_x
        self.player_start_y = player_start_y
        self.level_map = level_map
        self.places = places
        self.level_map = level_map

    def get_places(self):
        return json.loads(self.places)

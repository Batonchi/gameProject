import json
from datetime import date


# класс для обертки полученной сессии
class GetSession:

    def __init__(self, session_id: int, date_start: date, player_name: str, level_id: int, inf: str):
        # id сессии, дата старта, имя игрока, уровень карты и информация
        self.session_id = session_id
        self.date_start = date_start
        self.player_name = player_name
        self.level_id = level_id
        self.inf = inf


# класс для обертки полученного игрока
class Player:

    def __init__(self, nickname: str, player_id: int = None):
        # id игрока и его никнейм
        self.player_id = player_id
        self.nickname = nickname


# класс для оберткиработы с level
class Level:

    def __init__(self, level_id: int, player_start_x: int, player_start_y: int, level_map: str, places: str = '{}'):
        # определяем id уровня, стартовые координаты игрока и места
        self.level_id = level_id
        self.player_start_x = player_start_x
        self.player_start_y = player_start_y
        self.level_map = level_map
        self.places = places
        self.level_map = level_map

    def get_places(self):
        return json.loads(self.places)

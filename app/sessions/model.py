class GetSession:

    def __init__(self, session_id: int, player_id: int, place_id: int, inf: str):
        self.session_id = session_id
        self.player_id = player_id
        self.place_id = place_id
        self.inf = inf


class Player:

    def __init__(self, nickname: str, player_id: int = None):
        self.player_id = player_id
        self.nickname = nickname


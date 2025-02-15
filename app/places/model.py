from typing import Tuple


class CreatePLace:

    def __init__(self, place_name: str,  description: str, coors: Tuple[int, int]):
        self.place_name = place_name
        self.description = description
        self.coors = coors


class GetPlace:

    def __init__(self, place_id: int, place_name: str,  description: str, coors: Tuple[int, int]):
        self.place_id = place_id
        self.place_name = place_name
        self.description = description
        self.coors = coors

    def __str__(self):
        return f'{self.place_id} {self.place_name} {self.description} {self.coors}'


from database import Connection
from app.places.model import CreatePLace, GetPlace


class PlaceService:

    @staticmethod
    def save(place: CreatePLace):
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute('''INSERT INTO places (place_name, descriprion, coors) VALUES (?, ?, ?)''',
                        (place.place_name, place.description, place.coors))
            conn.commit()

    @staticmethod
    def get_place_by_id(place_id: int):
        with Connection() as conn:
            query = '''SELECT * FROM places WHERE place_id = ?'''
            result = conn.cursor().execute(query, (place_id,)).fetchone()
            return GetPlace(result[0], result[1], result[2], result[3])

    @staticmethod
    def get_place_by_name(place_name: str):
        with Connection() as conn:
            query = '''SELECT * FROM places WHERE place_name = ?'''
            result = conn.cursor().execute(query, (place_name,)).fetchone()
            return GetPlace(result[0], result[1], result[2], result[3])

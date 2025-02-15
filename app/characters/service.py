from app.characters.model import CreateCharacter, GetCharacter
from database import Connection


class CharacterService:

    @staticmethod
    def save(character: CreateCharacter):
        with Connection() as conn:
            conn.cursor().execute('''
                INSERT INTO characters (character_name, inf) VALUES (?, ?)
            ''', (character.character_name, character.inf))
            conn.commit()

    @staticmethod
    def get_character_by_name(character_name: str):
        with Connection() as conn:
            result = conn.cursor().execute('''SELECT * FROM characters WHERE character_name = ?''',
                                         (character_name, )).fetchone()
            if result is None:
                return
            return GetCharacter(result[0], result[1], result[2])

    @staticmethod
    def drop_character_by_id(character_id: int):
        with Connection() as conn:
            conn.cursor().execute('''DELETE FROM characters WHERE character_id = ?''', (character_id, ))
            conn.commit()

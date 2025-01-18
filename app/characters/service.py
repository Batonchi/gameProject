from app.characters.model import Character
from database import Connection


class CharacterService:

    @staticmethod
    def save(character: Character):
        with Connection() as conn:
            conn.cursor().execute('''
                INSERT INTO characters (character_name, info) VALUES (?, ?)
            ''', (character.character_name, character.info))
            conn.commit()

    @staticmethod
    def get_character_by_name(character_name: str):
        with Connection() as conn:
            return conn.cursor().execute('''SELECT * FROM characters WHERE character_name = ?''',
                                         (character_name, )).fetchone()

    @staticmethod
    def drop_character_by_id(character_id: int):
        with Connection() as conn:
            conn.cursor().execute('''DELETE FROM characters WHERE character_id = ?''', (character_id, ))
            conn.commit()

    def update_character_by_id(self, character_id: int, new_character: list):
        self.drop_character_by_id(character_id)
        self.save(Character(*new_character))

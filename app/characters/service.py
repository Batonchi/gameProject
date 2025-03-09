from typing import List

from app.characters.model import CreateCharacter, GetCharacter, GetCharacters
from database import Connection


class CharacterService:

    @staticmethod
    def create(character: CreateCharacter):
        with Connection() as conn:
            conn.cursor().execute('''
                INSERT INTO characters (character_name, inf) VALUES (?, ?)''',
                                  (character.character_name, character.inf))
            conn.commit()

    @staticmethod
    def get_character_by_name(character_name: str):
        with Connection() as conn:
            result = conn.cursor().execute('''SELECT * FROM characters WHERE character_name = ?''',
                                           (character_name,)).fetchone()
            if result is None:
                return
            return GetCharacter(result[0], result[1], result[2])

    @staticmethod
    def drop_character_by_name(character_name: str):
        with Connection() as conn:
            conn.cursor().execute('''DELETE FROM characters WHERE character_name = ?''', (character_name,))
            conn.commit()

    @staticmethod
    def update_inf_by_id(character_id: int, inf: str):
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute('''UPDATE characters WHERE character_id = ?
                            SET inf = ?
            ''', (character_id, inf))
            conn.commit()

    @staticmethod
    def get_all_npc_characters() -> List[GetCharacters]:
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM characters')
            result = cur.fetchall()
            characters = [GetCharacters(character[0], character[1], character[2]) for character in result]
            return [el for el in characters if el.inf['is_npc']]

    @staticmethod
    def check_characters():
        with Connection() as conn:
            cur = conn.cursor()
            return cur.execute('SELECT * FROM characters').fetchall()


npc_inform = [
    ('Незнакомец', {
        'permissions': {
            'may_move': False,
            'may_speak': True,
            'may_use_items': False,
            'may_have_backpack': False
        },
        'by_coordinate_and_num_level_data': [
            [1, [15, 45], {
                'dialog_id': 1,
                'path_to_skin_image': '11'
            }],
            [1, [49, 22], {
                'dialog_id': 4,
                'path_to_skin_image': '11'
            }],
            [1, [25, 18], {
                'dialog_id': 7,
                'path_to_skin_image': '11'
            }],
            [1, [14, 15], {
                'dialog_id': 8,
                'path_to_skin_image': '11'
            }],
            [2, [33, 51], {
                'dialog_ids': [23, 24],
                'path_to_skin_image': '11'
            }],
            [3, [40, 54], {
                'dialog_ids': [i for i in range(26, 32)],
                'path_to_skin_image': '11'
            }]
        ],
        'is_npc': True
    }),
    ('Некто', {
        'permissions': {
            'may_move': False,
            'may_speak': True,
            'may_use_items': False,
            'may_have_backpack': False
        },
        'by_coordinate_and_num_level_data': [
            [1, [31, 40], {
                'dialog_id': 2,
                'path_to_skin_image': '1'
            }],
            [1, [32, 41], {
                'dialog_id': 2,
                'path_to_skin_image': '2'
            }],
            [1, [33, 40], {
                'dialog_id': 2,
                'path_to_skin_image': '3'
            }],
            [1, [42, 40], {
                'dialog_id': 3,
                'path_to_skin_image': '4'
            }],
            [1, [43, 40], {
                'dialog_id': 3,
                'path_to_skin_image': '5'
            }],
            [1, [40, 9], {
                'dialog_id': 5,
                'path_to_skin_image': '10'
            }],
            [1, [41, 8], {
                'dialog_id': 5,
                'path_to_skin_image': '7'
            }],
            [1, [39, 18], {
                'dialog_id': 6,
                'path_to_skin_image': '8'
            }],
            [1, [40, 16], {
                'dialog_id': 6,
                'path_to_skin_image': '9'
            }],
        ],
        'is_npc': True
    }),
]

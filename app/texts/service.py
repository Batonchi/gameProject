from database import Connection
from app.texts.model import GetText, CreateText


class TextService:

    @staticmethod
    def save(text: CreateText):
        with Connection() as connection:
            cur = connection.cursor()
            cur.execute('''INSERT INTO texts content VALUES ?''', (text.content,))

    @staticmethod
    def get_text_by_id(text_id: int) -> GetText:
        with Connection() as connection:
            cur = connection.cursor()
            result = cur.execute('''SELECT * FROM texts WHERE text_id = ?''', (text_id,)).fetchone()
            return GetText(result[0], result[1])


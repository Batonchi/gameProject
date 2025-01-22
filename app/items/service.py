from database import Connection
from app.items.model import Item


class ItemService:

    @staticmethod
    def save(item: Item):
        with Connection() as conn:
            conn.cursor().execute('''INSERT INTO items VALUES (item_name, description)''',
                                  (item.item_name, item.description))
            conn.commit()

    @staticmethod
    def get_item_by_id(item_id: int):
        with Connection() as conn:
            conn.cursor().execute('''SELECT * FROM items WHERE item_id = ?''', (item_id,))

    @staticmethod
    def drop_item_by_id(item_id: int):
        with Connection() as conn:
            conn.cursor().execute('''DELETE FROM items WHERE item_id = ?''', (item_id,))

    def update_item_by_id(self, new_item: list, item_id: int):
        self.drop_item_by_id(item_id)
        self.save(Item(*new_item))

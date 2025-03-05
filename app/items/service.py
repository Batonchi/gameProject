# from database import Connection
# from app.items.model import CreateItem, GetItem
#
#
# class ItemService:
#
#     @staticmethod
#     def save(item: CreateItem):
#         with Connection() as conn:
#             conn.cursor().execute('''INSERT INTO items VALUES (item_name, inf)''',
#                                   (item.item_name, item.inf))
#             conn.commit()
#
#     @staticmethod
#     def get_item_by_id_or_name(item_id: int, item_name: str):
#         with Connection() as conn:
#             result = conn.cursor().execute('''SELECT * FROM items WHERE item_id = ? or item_name = ?''',
#                                            (item_id, item_name)).fetchone()
#             if result is None:
#                 return
#             return GetItem(result[0], result[1], result[2])
#
#     @staticmethod
#     def drop_item_by_id(item_id: int):
#         with Connection() as conn:
#             conn.cursor().execute('''DELETE FROM items WHERE item_id = ?''', (item_id,))
#             conn.commit()
#
#
# doors = [
#     ('door', {'is_closed': False, 'key_value': '1'})
# ]
#
# keys = [
#     ('key', {'value': '1'}),
# ]
#
# notes = [
#     ('note', {'content': 'id'})
# ]

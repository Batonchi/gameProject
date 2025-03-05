# import json
#
#
# class CreateItem:
#
#     def __init__(self, item_name: str, inf: dict):
#         self.item_name = item_name
#         self.inf = json.dumps(inf)
#
#
# class GetItem:
#
#     def __init__(self, item_id: int, item_name: str, inf: str, func):
#         self.item_id = item_id
#         self.item_name = item_name
#         self.inf = inf
#         self.use_func = func
#
#     def get_info(self):
#         self.use_func()
#
#     def do_affect(self, character: Character):
#         character

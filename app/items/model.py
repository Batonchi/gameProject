import json


class Item:

    def __init__(self, item_name: str, description: str, item_id: int = None):
        self.item_name = item_name
        self.description = description
        if item_id:
            self.item_id = item_id
        self.inf = json.loads(self.description)

    def get_info(self):
        return self.inf

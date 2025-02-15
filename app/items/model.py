import json


class CreateItem:

    def __init__(self, item_name: str, inf: dict):
        self.item_name = item_name
        self.inf = json.dumps(inf)


class GetItem:

    def __init__(self, item_id: int, item_name: str, inf: str):
        self.item_id = item_id
        self.item_name = item_name
        self.inf = json.loads(inf)

    def get_info(self):
        return self.inf

    def use_item(self):
        self.inf['endurance'] -= 1
        if self.inf['endurance'] == 0:
            self.inf.get('is_deleted', True)
            self.inf['is_deleted'] = True

    def do_affect(self):
        pass

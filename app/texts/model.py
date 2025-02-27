import json


class CreateText:

    def __init__(self, content: dict):
        self.content = json.dumps(content)


class GetText:

    def __init__(self, text_id: int, content: str):
        self.text_id = text_id
        self.content = json.loads(content)
        {
            'text': 'hi',
            'next': {
                'text': content,
                'next': {

                }
            }
        }
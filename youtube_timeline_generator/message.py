from enum import Enum
import json


class Role(Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content


class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return {'role': obj.role, 'content': obj.content}
        return super().default(obj)

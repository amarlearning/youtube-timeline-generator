import json
import requests

from message import Message, MessageEncoder



class UndercoverLLMAgent:
    def __init__(self, model_name, system_prompt, api_endpoint):
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.api_endpoint = api_endpoint
        self.system_prompt_message = Message(
            role="system", content=system_prompt)

    def find_answer_for(self, message: Message):
        payload = {
            "model": self.model_name,
            "messages": [
                self.system_prompt_message,
                message
            ],
        }

        response = requests.post(
            self.api_endpoint,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload, cls=MessageEncoder))
        return self.return_message(response.json())

    def return_message(self, response):
        parsed_data = {}
        parsed_data['role'] = response.get(
            'choices')[0].get('message').get('role')
        parsed_data['content'] = response.get(
            'choices')[0].get('message').get('content')

        return Message(role=parsed_data['role'], content=parsed_data['content'])

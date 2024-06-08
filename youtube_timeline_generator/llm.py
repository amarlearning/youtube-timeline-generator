import json
import requests

from youtube_timeline_generator.message import Message, MessageEncoder


class UndercoverLLMAgent:
    def __init__(self, system_prompt, model_name="meta-llama-3-8b-instruct",
                 api_endpoint="http://0.0.0.0:8080/v1/chat/completions"):
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

    @staticmethod
    def return_message(response):
        parsed_data = {'role': response.get('choices')[0].get('message').get('role'),
                       'content': response.get('choices')[0].get('message').get('content')}

        return Message(role=parsed_data['role'], content=parsed_data['content'])

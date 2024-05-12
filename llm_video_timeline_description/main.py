from llm_video_timeline_description.message import Message
from llm_video_timeline_description.llm import UndercoverLLMAgent
from llm_video_timeline_description.prompt import SYSTEM_QUERY_PROMPT
from flask import Flask, jsonify


app = Flask(__name__)
agent = UndercoverLLMAgent(system_prompt=SYSTEM_QUERY_PROMPT)


@app.route("/")
def health_check():
    return agent.find_answer_for(Message(role="user", content="hello")).content, 200


if __name__ == "__main__":
    app.run()

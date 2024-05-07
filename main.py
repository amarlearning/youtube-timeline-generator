from message import Message
from llm_model import UndercoverLLMAgent


def main():
    model_name = "meta-llama-3-8b-instruct.Q8_0.gguf"
    api_endpoint = "http://0.0.0.0:8080/v1/chat/completions"
    system_prompt = "this is a long system prompt - fire up the engines"

    agent = UndercoverLLMAgent(
        model_name=model_name, system_prompt=system_prompt, api_endpoint=api_endpoint)

    response = agent.find_answer_for(
        Message(role="user", content='hello world'))

    print(f'Role: {response.role}')
    print(f'Content: {response.content}')


if __name__ == "__main__":
    main()

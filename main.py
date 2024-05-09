from message import Message
from llm import UndercoverLLMAgent
from utils import clean_srt_content, get_time_bucketing


def main():
    model_name = "meta-llama-3-8b-instruct.Q8_0.gguf"
    api_endpoint = "http://0.0.0.0:8080/v1/chat/completions"
    system_prompt = '''
    Being a language expert please create buckets of time with short summary(in a single phrase) of topic discussed in the conversation.
    Create a new bucket when there is a change in the topic. You will be given a part of the SRT file by the user. Please make use of it. 
    Do not exceed the timestamps given by the user while bucketing.
        Example, 
        00:01:06 - 00:01:35 = Introduction 
        00:01:35 - 00:02:47 = Overview of civil engineering
    '''
    agent = UndercoverLLMAgent(
        model_name=model_name, system_prompt=system_prompt, api_endpoint=api_endpoint)

    system_prompt_aggregation = '''
       Being a language expert please aggregate the below time intervals into 5-10 buckets with short summary of topic discussed in the conversation in a phrase. 
            Example, 
            00:01:06 - 00:01:35 = Introduction 
            00:01:35 - 00:02:47 = Overview of civil engineering
        '''

    agent2 = UndercoverLLMAgent(
        model_name=model_name, system_prompt=system_prompt_aggregation, api_endpoint=api_endpoint)

    split_srt_content = clean_srt_content(input_file="main_srt.srt")

    time_buckets = get_time_bucketing(split_srt_content, agent)
    print(f"time_buckets: {time_buckets}")

    response = agent2.find_answer_for(
        Message(role="user", content=time_buckets))
    print(f'Role: {response.role}')
    print(f'Content: {response.content}')


if __name__ == "__main__":
    main()

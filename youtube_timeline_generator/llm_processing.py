from youtube_timeline_generator.llm import UndercoverLLMAgent
from youtube_timeline_generator.message import Message
from youtube_timeline_generator.prompt import SUMMARY_PROMPT, SYSTEM_AGGREGATION_PROMPT, SYSTEM_QUERY_PROMPT


def get_time_bucketing(split_srt_content):
    model_answers = list(
        map(
            lambda srt_chunk: UndercoverLLMAgent(system_prompt=SYSTEM_QUERY_PROMPT).find_answer_for(
                Message(
                    role="user",
                    content=srt_chunk
                )
            ).content,
            split_srt_content
        )
    )
    time_buckets = '\n'.join(model_answers)
    return time_buckets


def get_aggregated_time_buckets(time_buckets):
    return UndercoverLLMAgent(
        system_prompt=SYSTEM_AGGREGATION_PROMPT).find_answer_for(
        Message(role="user", content=time_buckets)
    ).content


def get_summary(time_buckets):
    return UndercoverLLMAgent(system_prompt=SUMMARY_PROMPT).find_answer_for(
        Message(role="user", content=time_buckets)
    ).content

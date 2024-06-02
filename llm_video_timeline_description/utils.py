from llm_video_timeline_description.message import Message
import re


def split_and_clean_srt_content(srt_content):
    cleaned_content = ""
    split_srt = []
    pattern_second_timestamp = r'(-->\s\d{2}:\d{2}:\d{2},\d{3})'
    pattern_comma_three_digits = r',\d{3}'
    for line in srt_content.splitlines():
        stripped_line = line.strip()
        if not stripped_line or stripped_line.isdigit():
            cleaned_content += "\n"
            continue
        stripped_line_with_space = stripped_line + " "
        line_with_one_timestamp = re.sub(
            pattern_second_timestamp, '', stripped_line_with_space)
        processed_line = re.sub(
            pattern_comma_three_digits, '', line_with_one_timestamp)
        cleaned_content += processed_line
        if len(cleaned_content) > 7950:
            split_srt.append(cleaned_content)
            cleaned_content = ""
    split_srt.append(cleaned_content)
    return split_srt


def get_time_bucketing(split_srt_content, agent):
    model_answers = list(
        map(
            lambda srt_chunk: agent.find_answer_for(
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

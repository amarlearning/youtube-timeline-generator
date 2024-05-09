from message import Message


def clean_srt_content(srt_content):
    cleaned_content = ""
    split_srt = []
    for line in srt_content.splitlines():
        stripped_line = line.strip()
        if not stripped_line or stripped_line.isdigit():
            cleaned_content += "\n"
            continue
        stripped_line_with_space = stripped_line + " "
        cleaned_content += stripped_line_with_space
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

import re

from llm_video_timeline_description.postprocessing import UndercoverPostprocessingAgent


def clean_srt_content(srt_content):
    cleaned_srt_content = ""
    pattern_for_second_timestamp = r'(-->\s\d{2}:\d{2}:\d{2},\d{3})'
    pattern_for_comma_followed_by_three_digits = r',\d{3}'
    for line in srt_content.splitlines():
        stripped_line = line.strip()
        if not stripped_line or stripped_line.isdigit():
            cleaned_srt_content += "\n"
            continue
        line_with_appended_space = stripped_line + " "
        line_without_second_timestamp = re.sub(
            pattern_for_second_timestamp, '', line_with_appended_space)
        line_without_comma_and_three_digits = re.sub(
            pattern_for_comma_followed_by_three_digits, '', line_without_second_timestamp)
        cleaned_srt_content += line_without_comma_and_three_digits
    return cleaned_srt_content


def split_cleaned_content(cleaned_srt_content):
    split_srt_content = []
    while len(cleaned_srt_content) > 7950:
        split_srt_content.append(cleaned_srt_content[:7950])
        cleaned_srt_content = cleaned_srt_content[7950:]
    split_srt_content.append(cleaned_srt_content)
    return split_srt_content


def process_srt_content(srt_content):
    cleaned_content = clean_srt_content(srt_content)
    split_content = split_cleaned_content(cleaned_content)
    return split_content


def clean_aggregated_timeline(data):
    return UndercoverPostprocessingAgent(data) \
        .filter_lines_with_at_least_one_timestamp() \
        .remove_enumeration_before_first_timestamp() \
        .remove_second_timestamp() \
        .remove_colon_after_last_timestamp().text

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
        line_with_one_timestamp = re.sub(pattern_second_timestamp, '', stripped_line_with_space)
        processed_line = re.sub(pattern_comma_three_digits, '', line_with_one_timestamp)
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


def postprocessing(input_text):
    # Split the input into lines
    lines = input_text.split('\n')

    # Define a regex pattern to detect timestamps
    timestamp_pattern = re.compile(r'\b\d{2}:\d{2}:\d{2}\b')

    # Filter out lines that do not contain at least one timestamp
    filtered_lines = [line for line in lines if timestamp_pattern.search(line)]

    # Remove enumeration before the first timestamp of the line
    processed_lines = []
    for line in filtered_lines:
        match = timestamp_pattern.search(line)
        if match:
            processed_line = line[match.start():].strip()
            processed_lines.append(processed_line)

    # Join the processed lines back into a single string
    processed_aggregated_time_buckets = '\n'.join(processed_lines)

    print(
        f"after removing lines without timestamp and enumeration before timestamp: {processed_aggregated_time_buckets}")
    print("\n")

    ################################################

    # Split the input text into lines
    lines = processed_aggregated_time_buckets.strip().split('\n')

    # Initialize an empty list to store the processed lines
    processed_lines = []

    # Iterate through each line
    for line in lines:
        # Split the line at the first occurrence of ':' after the timestamp range
        first_part, second_part = line.split(': ', 1)

        # Remove the second timestamp by splitting at the hyphen and taking the first part
        start_timestamp = first_part.split('-')[0]

        # Concatenate the start timestamp with the rest of the line
        processed_line = f"{start_timestamp}: {second_part}"

        # Append the processed line to the list
        processed_lines.append(processed_line)

    # Join the processed lines back into a single string
    output_text = '\n'.join(processed_lines)

    # Print the result
    print(f"after removing second timestamp: {output_text}")
    print("\n")
    first_output_text = output_text

    #################################

    # Remove last colon

    output_text = ""
    for line in first_output_text.split('\n'):
        if line.strip():  # Check if the line is not empty
            parts = line.split(':')
            modified_line = ':'.join(parts[:-1]) + ' ' + parts[
                -1].strip()  # Join except the last part, stripping whitespace
            output_text += modified_line + '\n'

    print(f"output_text: {output_text}")

    return output_text

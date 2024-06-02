from llm_video_timeline_description.utils import process_srt_content


def test_process_data():
    data = "sample data"
    result = process_srt_content(data)
    expected_result = ["sample data "]
    assert result == expected_result, f'Expected {expected_result}, got {result}'

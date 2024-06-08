from youtube_timeline_generator.utils import process_srt_content


def test_process_data():
    data = """
        1
        00:00:01,000 --> 00:00:04,000
        This is the first subtitle.

        2
        00:00:05,000 --> 00:00:09,000
        This is the second subtitle.

        3
        00:00:10,000 --> 00:00:14,000
        This is the third subtitle.
    """

    result = process_srt_content(data)
    expected_result = [
        "\n\n00:00:01  This is the first subtitle. \n\n00:00:05  This is the second subtitle. \n\n00:00:10  This is the third subtitle. \n"]
    assert result == expected_result, f'Expected {expected_result}, got {result}'

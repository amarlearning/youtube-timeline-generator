from unittest.mock import Mock, patch
from llm_video_timeline_description.video_srt import get_srt_from_youtube_video


@patch('llm_video_timeline_description.video_srt.YouTubeTranscriptApi')
@patch('llm_video_timeline_description.video_srt.SRTFormatter')
def test_get_srt_from_youtube_video(mock_formatter, mock_transcript_api):
    # Arrange
    mock_transcript = [
        {'text': 'Hello, world!', 'start': 0.0, 'duration': 5.0}]
    mock_transcript_api.get_transcript.return_value = mock_transcript
    mock_formatter_instance = Mock()
    mock_formatter.return_value = mock_formatter_instance
    mock_formatter_instance.format_transcript.return_value = '1\n00:00:00,000 --> 00:00:05,000\nHello, world!\n\n'
    test_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

    result = get_srt_from_youtube_video(test_url)

    mock_transcript_api.get_transcript.assert_called_once_with('dQw4w9WgXcQ')
    mock_formatter_instance.format_transcript.assert_called_once_with(
        mock_transcript)
    assert result == '1\n00:00:00,000 --> 00:00:05,000\nHello, world!\n\n'

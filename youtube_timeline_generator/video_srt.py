from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter


def get_srt_from_youtube_video(video_url: str) -> str:
    formatter = SRTFormatter()
    video_id = video_url.split("v=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    srt_formatted = formatter.format_transcript(transcript)

    return srt_formatted

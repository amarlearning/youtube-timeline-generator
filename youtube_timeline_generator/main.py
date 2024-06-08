from flask import Flask
from flask import render_template, request

from youtube_timeline_generator.logger import get_logger
from youtube_timeline_generator.utils import clean_aggregated_timeline, process_srt_content
from youtube_timeline_generator.llm_processing import get_aggregated_time_buckets, get_summary, get_time_bucketing
from youtube_timeline_generator.video_srt import get_srt_from_youtube_video

app = Flask(__name__)
logger = get_logger()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


@app.route('/submit', methods=['POST'])
def submit_video():
    video_url = request.form['video_url']

    srt_content = get_srt_from_youtube_video(video_url)
    split_description_content = process_srt_content(srt_content)

    time_buckets = get_time_bucketing(split_description_content)
    logger.info(f"Time buckets: {time_buckets}")

    aggregated_time_buckets = get_aggregated_time_buckets(time_buckets)
    logger.info(f"Aggregated time buckets: {aggregated_time_buckets}")

    processed_timeline = clean_aggregated_timeline(aggregated_time_buckets)
    logger.info(f"Processed timeline: {processed_timeline}")

    summary = get_summary(time_buckets)
    logger.info(f"Summary: {summary}")

    response = {
        "summary": summary,
        "timeline": processed_timeline
    }
    return response, 200


if __name__ == "__main__":
    app.run(debug=True)
    app.run()

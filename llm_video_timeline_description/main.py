from flask import Flask
from flask import render_template, request

from llm_video_timeline_description.llm import UndercoverLLMAgent
from llm_video_timeline_description.logger import get_logger
from llm_video_timeline_description.message import Message
from llm_video_timeline_description.prompt import SYSTEM_QUERY_PROMPT, SYSTEM_AGGREGATION_PROMPT, SUMMARY_PROMPT
from llm_video_timeline_description.utils import split_and_clean_srt_content, get_time_bucketing
from llm_video_timeline_description.video_srt import get_srt_from_youtube_video
from llm_video_timeline_description.postprocessing import UndercoverPostprocessingAgent

app = Flask(__name__)
logger = get_logger()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit_video():
    video_url = request.form['video_url']

    srt_content = get_srt_from_youtube_video(video_url)

    split_description_content = split_and_clean_srt_content(srt_content)

    time_buckets = get_time_bucketing(
        split_description_content, UndercoverLLMAgent(system_prompt=SYSTEM_QUERY_PROMPT))
    logger.info(f"Time buckets: {time_buckets}")

    aggregated_time_buckets = UndercoverLLMAgent(
        system_prompt=SYSTEM_AGGREGATION_PROMPT).find_answer_for(
        Message(role="user", content=time_buckets)
    ).content
    logger.info(f"Aggregated time buckets: {aggregated_time_buckets}")

    processed_timeline = UndercoverPostprocessingAgent(aggregated_time_buckets) \
        .filter_lines_with_at_least_one_timestamp() \
        .remove_enumeration_before_first_timestamp() \
        .remove_second_timestamp() \
        .remove_colon_after_last_timestamp().text
    logger.info(f"Processed timeline: {processed_timeline}")

    summary = UndercoverLLMAgent(system_prompt=SUMMARY_PROMPT).find_answer_for(
        Message(role="user", content=time_buckets)
    ).content
    logger.info(f"Summary: {summary}")

    response = {
        "summary": summary,
        "timeline": processed_timeline
    }
    return response, 200


if __name__ == "__main__":
    app.run(debug=True)
    app.run()

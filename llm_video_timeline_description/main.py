from flask import Flask
from flask import render_template, request

from llm_video_timeline_description.llm import UndercoverLLMAgent
from llm_video_timeline_description.message import Message
from llm_video_timeline_description.prompt import SYSTEM_QUERY_PROMPT, SYSTEM_AGGREGATION_PROMPT, SUMMARY_PROMPT
from llm_video_timeline_description.utils import split_and_clean_srt_content, get_time_bucketing
from llm_video_timeline_description.video_srt import get_srt_from_youtube_video
from llm_video_timeline_description.postprocessing import UndercoverPostprocessingAgent

app = Flask(__name__)
time_bucketing_agent = UndercoverLLMAgent(system_prompt=SYSTEM_QUERY_PROMPT)
time_bucketing_aggregation_agent = UndercoverLLMAgent(
    system_prompt=SYSTEM_AGGREGATION_PROMPT)
summary_agent = UndercoverLLMAgent(system_prompt=SUMMARY_PROMPT)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit_video():
    video_url = request.form['video_url']

    srt_content = get_srt_from_youtube_video(video_url)

    split_description_content = split_and_clean_srt_content(srt_content)

    time_buckets = get_time_bucketing(
        split_description_content, time_bucketing_agent)

    aggregated_time_buckets = time_bucketing_aggregation_agent.find_answer_for(
        Message(role="user", content=time_buckets)
    ).content

    processed_timeline = UndercoverPostprocessingAgent(aggregated_time_buckets) \
        .filter_lines_with_at_least_one_timestamp() \
        .remove_enumeration_before_first_timestamp() \
        .remove_second_timestamp() \
        .remove_colon_after_last_timestamp().text

    summary = summary_agent.find_answer_for(
        Message(role="user", content=time_buckets)
    ).content

    response = {
        "summary": summary,
        "timeline": processed_timeline
    }
    return response, 200


if __name__ == "__main__":
    app.run(debug=True)
    app.run()

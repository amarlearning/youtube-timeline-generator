from flask import Flask
from flask import render_template, request

from llm_video_timeline_description.llm import UndercoverLLMAgent
from llm_video_timeline_description.message import Message
from llm_video_timeline_description.prompt import SYSTEM_QUERY_PROMPT, SYSTEM_AGGREGATION_PROMPT, SUMMARY_PROMPT
from llm_video_timeline_description.utils import split_and_clean_srt_content, get_time_bucketing
from llm_video_timeline_description.video_srt import get_srt_from_youtube_video

app = Flask(__name__)
time_bucketing_agent = UndercoverLLMAgent(system_prompt=SYSTEM_QUERY_PROMPT)
time_bucketing_aggregation_agent = UndercoverLLMAgent(system_prompt=SYSTEM_AGGREGATION_PROMPT)
summary_agent = UndercoverLLMAgent(system_prompt=SUMMARY_PROMPT)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit_video():
    video_url = request.form['video_url']
    srt_content = get_srt_from_youtube_video(video_url)
    split_description_content = split_and_clean_srt_content(srt_content)
    print(f"split_description_content: {split_description_content[2][:200]}")
    print(f"length split_description_content: {len(split_description_content)}")
    time_buckets = get_time_bucketing(split_description_content, time_bucketing_agent)
    print(f"time_buckets: {time_buckets}")
    aggregated_time_buckets = time_bucketing_aggregation_agent.find_answer_for(
        Message(role="user", content=time_buckets)
    ).content
    print(f"aggregated_time_buckets: {aggregated_time_buckets}")
    summary = summary_agent.find_answer_for(
        Message(role="user", content=time_buckets)
    ).content
    print(f"summary: {summary}")
    return aggregated_time_buckets + "\n" + summary, 200


if __name__ == "__main__":
    app.run(debug=True)
    app.run()

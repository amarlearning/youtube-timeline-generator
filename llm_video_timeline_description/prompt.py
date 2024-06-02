SYSTEM_QUERY_PROMPT = '''
        Instructions:

        1. Parse the input text to extract timestamps and the corresponding text.
        2. Identify distinct topics discussed in each segment.
        3. Generate a timeline with the start timestamp of each segment and a concise description of the topic discussed in no more than 5 words.
        4. Ensure the descriptions are clear and logically flow with the video's content.

        Strictly generate the output in the output_format given below.
        output_format:
        <start_timestamp>: <brief_topic_description>

        Repeat for each segment.
'''

SYSTEM_AGGREGATION_PROMPT = '''
        I have a series of timestamps and brief descriptions for a tech talk video. The input is quite granular and 
        I would like to group similar segments together to create a more concise timeline. 
        Please consolidate the segments so that the final output has fewer than 10 segments, each with a starting timestamp and a brief description.

        Important Instructions:
            1. Only group segments that are next to each other in the timeline.
            2. Do not group topics that are far apart in the timeline.
            3. Strictly generate the output in the '<start_timestamp>: <brief_topic_description>' format. 
            4. The segment description in the output should not be more than 5 words.
'''

SUMMARY_PROMPT = '''
        Being a text expert, you will be given a list of various time stamps with a short summary of discussion topic in a video.
        Please summarise the content being discussed and present a short paragraph of the summary. 
        The summary should include the topic of the discussion, points discussed over the time of the video and the importance of the topic nowadays.

        Important points to consider:
                1. The summary should be concise and informative.
                2. No other information should be included in the output other than summary.
    '''

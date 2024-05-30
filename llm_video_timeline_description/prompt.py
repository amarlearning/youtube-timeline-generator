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
        Instructions:
        
        1. Parse the input text to extract timestamps and the corresponding text.
        2. Aggregate topics discussed in each segment.
        3. Generate the entire timeline with the start timestamp of aggregated segment and a concise description of the topic discussed in no more than 5 words.
        4. Ensure the descriptions are clear and logically flow with the video's content.
        
        Strictly generate the output in the output_format given below and the number of entries should strictly be more than 2 and less than 10.
        output_format:
        <start_timestamp>: <brief_topic_description>
        
        Repeat for each segment.
'''

SUMMARY_PROMPT = '''
    Being a text expert, you will be given a list of various time stamps with a short summary of discussion topic in a video.
    Please summarise the content being discussed and present a short paragraph of the summary. 
    The summary should include the topic of the discussion, points discussed over the time of the video and the importance of the topic nowadays.
    '''

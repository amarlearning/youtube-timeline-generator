SYSTEM_QUERY_PROMPT = '''
    Being a language expert, you will be given a part of the transcript of a tech talk video in a input_format. Each line represents the script said in the video in the given timestamp.
    input_format:
    01:02:14  be across uh multiple clusters and
    01:02:18  there's already a lot of work that's 
    
    The output should be a structured list with each entry containing the start timestamp and a brief description of the topic discussed during that segment.
    
    Strictly generate the output in the output_format given below.
    output_format:
        00:01:06 : Introduction 
        00:03:35 : What is NlP
        00:15:35 : Why Multilingual NLP 
        00:17:29 : How to perform multilingual NLP
    '''

SYSTEM_AGGREGATION_PROMPT = '''
       Being a language expert, you will be given entries of various time stamps with a short summary of discussion topic.
       Please combine and aggregate these entries into a fewer samples.
       Number of entries should strictly be more than 2 and less than 10. 
       Perform this action for the entire time duration present in the given input.
       The output should contain each timestamp entry with a short phrase summary of discussion topic.
    '''

SUMMARY_PROMPT = '''
    Being a text expert, you will be given a list of various time stamps with a short summary of discussion topic in a video.
    Please summarise the content being discussed and present a short paragraph of the summary. 
    The summary should include the topic of the discussion, points discussed over the time of the video and the importance of the topic nowadays.
    '''

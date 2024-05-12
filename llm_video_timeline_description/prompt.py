SYSTEM_QUERY_PROMPT = '''
    Being a language expert please create buckets of time with short summary(in a single phrase) of topic discussed in the conversation.
    Create a new bucket when there is a change in the topic. You will be given a part of the SRT file by the user. Please make use of it. 
    Do not exceed the timestamps given by the user while bucketing.
        Example, 
        00:01:06 - 00:01:35 = Introduction 
        00:01:35 - 00:02:47 = Overview of civil engineering
    '''

SYSTEM_AGGREGATION_PROMPT = '''
       For a given video a list of various time buckets with a short summary will be provided by a user.
       Please group the time buckets into not more than 5 to 10 time buckets. Group them over the similarity of the been topics discussed.
       Do not exceed the timestamps given by the user while grouping. Consider the entire time period.
            Example of output- 
            00:01:06 - 00:01:35 = Introduction 
            00:01:35 - 00:02:47 = Overview of civil engineering
        '''

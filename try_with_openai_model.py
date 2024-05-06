import openai

def clean_srt_content(input_file):
      cleaned_content = ""
      split_srt = []
      with open(input_file, 'r') as f_in:
            for line in f_in:
                  stripped_line = line.strip()
                  if not stripped_line or stripped_line.isdigit():
                        cleaned_content += "\n"
                        continue
                  stripped_line_with_space = stripped_line + " "
                  cleaned_content += stripped_line_with_space
                  if len(cleaned_content) > 15950:
                        split_srt.append(cleaned_content)
                        cleaned_content = ""
            split_srt.append(cleaned_content)
      return split_srt

def get_time_bucketing_from_openai(cleaned_content):
      openai.api_key = ""
      messages = []
      prompt = '''
            Being a language expert please create buckets of time with short summary of topic discussed in the conversation in a phrase. 
            Example, 
            00:01:06 - 00:01:35 = Introduction 
            00:01:35 - 00:02:47 = Overview of threads
            The conversation is as below -
            '''
      messages.append({'role': 'system', 'content': prompt})

      messages.append({'role': 'user', 'content': cleaned_content})

      response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=messages,
          temperature=1)
      response_text = response.choices[0].message["content"]
      return str(response_text)

def get_time_aggregation_from_openai(time_intervals):
      openai.api_key = ""
      messages = []
      prompt = '''
            Being a language expert please aggregate the below time intervals into 5-10 buckets with short summary of topic discussed in the conversation in a phrase. 
            Example, 
            00:01:06 - 00:01:35 = Introduction 
            00:01:35 - 00:02:47 = Overview of threads
            The time intervals are as below -
            '''
      messages.append({'role': 'system', 'content': prompt})

      messages.append({'role': 'user', 'content': time_intervals})

      response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=messages,
          temperature=1)
      response_text = response.choices[0].message["content"]
      return str(response_text)

split_srt = clean_srt_content("/Users/shrutid/learnings_from_pandey_ji/sample_solution/main_srt.srt")

model_answers = []
for content in split_srt:
      model_answer = get_time_bucketing_from_openai(content)
      model_answers.append(model_answer)

time_intervals = '\n'.join(model_answers)

print(f"video description: {get_time_aggregation_from_openai(time_intervals)}")



import re


class UndercoverPostprocessingAgent:
    def __init__(self, text):
        self.text = text

    def filter_lines_with_at_least_one_timestamp(self):
        lines = self.text.split('\n')
        timestamp_pattern = re.compile(r'\b\d{2}:\d{2}:\d{2}\b')
        filtered_lines = [
            line for line in lines if timestamp_pattern.search(line)]
        self.text = '\n'.join(filtered_lines)
        return self

    def remove_enumeration_before_first_timestamp(self):
        lines = self.text.split('\n')
        timestamp_pattern = re.compile(r'\b\d{2}:\d{2}:\d{2}\b')
        processed_lines = []
        for line in lines:
            match = timestamp_pattern.search(line)
            if match:
                processed_line = line[match.start():].strip()
                processed_lines.append(processed_line)
        self.text = '\n'.join(processed_lines)
        return self

    def remove_second_timestamp(self):
        lines = self.text.strip().split('\n')
        processed_lines = []
        for line in lines:
            first_part, second_part = line.split(': ', 1)
            start_timestamp = first_part.split('-')[0]
            processed_line = f"{start_timestamp}: {second_part}"
            processed_lines.append(processed_line)
        self.text = '\n'.join(processed_lines)
        return self

    def remove_colon_after_last_timestamp(self):
        output_text = ""
        for line in self.text.split('\n'):
            if line.strip():
                parts = line.split(':')
                modified_line = ':'.join(parts[:-1]) + ' ' + parts[-1].strip()
                output_text += modified_line + '\n'
        self.text = output_text
        return self

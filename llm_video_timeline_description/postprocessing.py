import re


class UndercoverPostprocessingAgent:
    def __init__(self):
        pass

    def perform_postprocessing(self, text_to_process):
        text_with_at_least_one_timestamp = self.filter_lines_with_at_least_one_timestamp(text_to_process)
        text_with_removed_enumeration = self.remove_enumeration_before_first_timestamp(text_with_at_least_one_timestamp)
        text_with_only_one_timestamp = self.remove_second_timestamp(text_with_removed_enumeration)
        processed_text = self.remove_colon_after_last_timestamp(text_with_only_one_timestamp)
        return processed_text

    @staticmethod
    def filter_lines_with_at_least_one_timestamp(text_to_process):
        lines = text_to_process.split('\n')
        timestamp_pattern = re.compile(r'\b\d{2}:\d{2}:\d{2}\b')
        filtered_lines = [line for line in lines if timestamp_pattern.search(line)]
        return '\n'.join(filtered_lines)

    @staticmethod
    def remove_enumeration_before_first_timestamp(text_to_process):
        lines = text_to_process.split('\n')
        timestamp_pattern = re.compile(r'\b\d{2}:\d{2}:\d{2}\b')
        processed_lines = []
        for line in lines:
            match = timestamp_pattern.search(line)
            if match:
                processed_line = line[match.start():].strip()
                processed_lines.append(processed_line)
        return '\n'.join(processed_lines)

    @staticmethod
    def remove_second_timestamp(text_to_process):
        lines = text_to_process.strip().split('\n')
        processed_lines = []
        for line in lines:
            first_part, second_part = line.split(': ', 1)
            start_timestamp = first_part.split('-')[0]
            processed_line = f"{start_timestamp}: {second_part}"
            processed_lines.append(processed_line)
        return '\n'.join(processed_lines)

    @staticmethod
    def remove_colon_after_last_timestamp(text_to_process):
        output_text = ""
        for line in text_to_process.split('\n'):
            if line.strip():
                parts = line.split(':')
                modified_line = ':'.join(parts[:-1]) + ' ' + parts[-1].strip()
                output_text += modified_line + '\n'
        return output_text

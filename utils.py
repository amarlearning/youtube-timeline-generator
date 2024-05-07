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
            if len(cleaned_content) > 10:
                split_srt.append(cleaned_content)
                cleaned_content = ""
        split_srt.append(cleaned_content)
    return split_srt

def find_substring_between(text, start):
    start_index = text.find(start)
    if start_index == -1:
        return None
    start_index += len(start)
    return text[start_index:]

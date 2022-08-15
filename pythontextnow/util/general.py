import re


def replace_newlines(text: str):
    return re.sub(r'(?<!\\)\n', r'\\n', text)

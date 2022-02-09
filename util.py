#! /usr/bin/env python
# coding=utf-8
import re


def clear_text(text):
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if len(line) > 0:
            lines.append(line)
    return ' '.join(lines)


def preprocessing(text):  # 将 i++ 预处理为 i = i  + 1
    def convert(match):
        group = match.group()
        identifier_pattern = '[a-zA-Z_]+'
        identifier = re.findall(identifier_pattern, group)[0]
        return identifier + ' = ' + identifier + ' + 1'

    pattern = r'[a-zA-Z_]+\+\+'
    return re.sub(pattern, convert, text)

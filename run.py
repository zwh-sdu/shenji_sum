from baichuan_llm import Baichuan
import json
import pandas as pd
from tqdm import trange
from docx import Document
import re

# llm = Baichuan("http://10.102.33.19:1707/")


llm = Baichuan("http://127.0.0.1:1707/")


def get_res(content):
    messages = [{
        "role": "user",
        "content": "你将被提供一个会议纪要文本，请利用这个会议纪要完成后续任务。\n"
                   f"会议纪要：\n{content}\n"
                   "任务：\n总结出会议名称、会议中包含的所有事件、事件中所涉及到的金额信息。注意对事件进行适当的简要总结。\n"
                   "请严格按照如下格式回复，事件总结和金额信息之间用 | 符号分割：\n"
                   "会议时间：xx\n会议名称：xx\n事件：\n1. 事件1总结 | 金额信息\n2. 事件2总结 | 金额信息"
    }]
    response = llm(messages)
    return response


def getDocText(fileName):
    doc = Document(fileName)
    TextList = []
    for paragraph in doc.paragraphs:
        TextList.append(paragraph.text)

    return '\n'.join(TextList)


text = getDocText('./会议纪要例子.docx')
res = get_res(text)

print(res)

file_path = "output.txt"

# 使用 open 函数创建并打开一个文本文件，以写入模式打开
with open(file_path, 'w') as file:
    # 将字符串写入文件
    file.write(res)

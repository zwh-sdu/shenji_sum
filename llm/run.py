import argparse

from baichuan_llm import Baichuan
import json
import pandas as pd
from tqdm import trange
from docx import Document
import re
import os

llm = Baichuan("http://10.102.33.19:1707/")


# llm = Baichuan("http://127.0.0.1:1707/")


def get_res(content):
    messages = [{
        "role": "user",
        "content": "你将被提供一个会议纪要文本，请利用这个会议纪要完成后续任务。\n"
                   f"会议纪要：\n{content}\n"
                   "任务：\n找出会议的具体名称（包括第几次会议）、会议中讨论的所有事件、事件中所涉及到的金额信息。对事件进行适当总结，删除“会议听取”、“有关情况”等与事件本身无关的文字。\n"
                   "请严格按照如下格式回复，事件总结和金额信息之间用 | 符号分割：\n"
                   "会议时间：xx\n会议名称：xx\n事件：\n1. 讨论的第一个事件 | 金额信息\n2. 讨论的第二个事件 | 金额信息"
    }]
    response = llm(messages)
    return response


def get_sum(content):
    messages = [{
        "role": "user",
        "content": "你将被提供一个会议纪要文本，请利用这个会议纪要完成后续任务。\n"
                   f"会议纪要：\n{content}\n"
                   "任务：\n总结这个会议纪要，确保不丢失会议纪要中的重要信息。\n"
                   "会议纪要总结："
    }]
    response = llm(messages)
    return response


def getDocText(fileName):
    doc = Document(fileName)
    TextList = []
    for paragraph in doc.paragraphs:
        TextList.append(paragraph.text)

    return '\n'.join(TextList)


def get_all_files_in_folder(folder_path):
    """
    获取指定文件夹下的所有文件名

    :param folder_path: 文件夹路径
    :return: 包含所有文件名的列表
    """
    file_names = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_names.append(os.path.join(root, file))
    return file_names


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--file_dir", default="./data/txt", type=str, help="txt 文件读取目录")
    parser.add_argument("--result_file_dir", default="./data/llm_out", type=str, help="解析后txt输出目录")
    args = parser.parse_args()

    file_dir = args.file_dir
    result_file_dir = args.result_file_dir
    all_files = get_all_files_in_folder(file_dir)

    for file in all_files:
        result_file_path = file.replace(file_dir, result_file_dir)
        with open(file, 'r', encoding='UTF-8') as f:
            text = f.readlines()
            text = ''.join(text)

        res = get_res(text)
        with open(result_file_path, 'w', encoding='UTF-8') as f:
            f.write(res)

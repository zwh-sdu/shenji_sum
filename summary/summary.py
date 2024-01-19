import argparse

from baichuan_llm import Baichuan
import os

llm = Baichuan("http://10.102.33.19:1707/")


def get_sum(content):
    # v1
    messages = [{
        "role": "user",
        "content": "你将被提供一个会议纪要文本，请利用这个会议纪要完成后续任务。\n"
                   f"会议纪要：\n{content}\n"
                   "任务：\n总结这个会议纪要，确保不丢失会议纪要中的重要信息。\n"
                   "会议纪要总结："
    }]
    # v2 更凝练的版本
    messages = [{
        "role": "user",
        "content": "你将被提供一个会议纪要文本，请利用这个会议纪要完成后续任务。\n"
                   f"会议纪要：\n{content}\n"
                   "任务：\n尽可能简洁凝练地总结这个会议纪要，同时不要丢失会议纪要中的重要信息。\n"
                   "会议纪要总结："
    }]
    response = llm(messages)
    return response


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
    parser.add_argument("--file_dir", default="./data/txt", type=str, help="大模型抽取结果的 txt 所在目录")
    parser.add_argument("--result_file_dir", default="./data/summary", type=str, help="会议纪要总结输出目录")
    args = parser.parse_args()

    file_dir = args.file_dir
    result_file_dir = args.result_file_dir
    all_files = get_all_files_in_folder(file_dir)

    for file in all_files:
        result_file_path = file.replace(file_dir, result_file_dir)
        with open(file, 'r', encoding='UTF-8') as f:
            text = f.readlines()
            text = ''.join(text)

        res = get_sum(text)
        with open(result_file_path, 'w', encoding='UTF-8') as f:
            f.write(res)

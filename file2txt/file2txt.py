import sys
import pickle
import re
import  codecs
import string
import shutil
from win32com import client as wc
import docx
from docx import Document
import pdfplumber
import codecs
import os

def str_save_To_txt(data, file_path):
    with open(file_path, 'w', encoding='UTF-8') as f:
        f.write(data) 


def read_docx(file_path):
    doc = Document(file_path)
    TextList = []
    for paragraph in doc.paragraphs:
        TextList.append(paragraph.text)
    
    return '\n'.join(TextList)

# text = read_docx(r'F:\宝贝派的活儿\知识图谱\file2txt\files\会议纪要例子.docx')
# print(text)

def doc2docx(doc_file_path, docx_save_path):
    word = wc.Dispatch('Word.Application')
    doc = word.Documents.Open(doc_file_path)        # 目标路径下的文件
    doc.SaveAs(docx_save_path, 12, False, "", True, "", False, False, False, False)  # 转化后路径下的文件    
    doc.Close()
    word.Quit()

# doc_file_path = r'F:\宝贝派的活儿\知识图谱\会议纪要例子.doc'
# docx_save_path = r'F:\宝贝派的活儿\知识图谱\会议纪要例子_from_doc.docx'
# doc2docx(doc_file_path, docx_save_path)

def read_doc(file_path):
    docx_save_path = file_path.replace('.doc', '_from_doc.docx')
    print('doc save to', docx_save_path)
    doc2docx(file_path, docx_save_path)
    return read_docx(docx_save_path)
 
# doc_file_path = r'F:\宝贝派的活儿\知识图谱\会议纪要例子.doc'
# print(read_doc(doc_file_path))

def read_txt(file_path):
    with open(file_path, 'r', encoding='UTF-8') as f:
        data = f.readlines()
    return ''.join(data)

# print(read_txt('./会议纪要.txt'))

def pdf2txt(file_path, result_file_path):
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            f1=codecs.open(result_file_path, 'a', 'utf-8')
            f1.write(page.extract_text())
            f1.close()

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
    # # doc转docx
    # file_dir = r'F:\宝贝派的活儿\知识图谱\file2txt\files' # 完整路径，不能是相对路径，否则dox转docx会找不到文件
    # all_files = get_all_files_in_folder(file_dir)
    # for file in all_files:
    #     if file[-4:] == '.doc':
    #         docx_save_path = file.replace('.doc', '_from_doc.docx')
    #         doc2docx(file, docx_save_path)


    file_dir = r'F:\宝贝派的活儿\知识图谱\shenji_sum\data\file'
    reault_file_dir = r'F:\宝贝派的活儿\知识图谱\shenji_sum\data\txt'
    all_files = get_all_files_in_folder(file_dir)

    for file in all_files:
        if file[-4:] == '.pdf':
            result_file_path = file.replace('.pdf', '_pdf.txt')
            result_file_path = result_file_path.replace(file_dir, reault_file_dir)
            pdf2txt(file, result_file_path)
        elif file[-5:] == '.docx':
            result_file_path = file.replace('.docx', '_docx.txt')
            result_file_path = result_file_path.replace(file_dir, reault_file_dir)
            docx_data = read_docx(file)
            str_save_To_txt(docx_data, result_file_path)
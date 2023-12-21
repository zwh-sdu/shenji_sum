import re
import os


def get_nodes_and_lines(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.readlines()
        data = list(map(lambda x: x.strip(), data))

    nodes = [
        {"id": data[0], "group": 1},  # 会议时间
        {"id": data[1], "group": 2}  # 会议名称
    ]
    links = [{"source": data[0], "target": data[1]}]

    # 事件
    event_money_list = data[3:]
    for event_money in event_money_list:
        event_money = event_money[event_money.index('.') + 1:].strip()
        event, money = event_money.split('| ')
        nodes.append({"id": event, "group": 2})
        links.append({"source": data[1], "target": event})
        if bool(re.search(r'\d', money)):
            nodes.append({"id": money, "group": 3})
            links.append({"source": event, "target": money})

    # nodes [{'id': '会议时间：2022年4月15日', 'group': 1}, ...]
    # links [{'source': '会议名称：中共XX市XX区XX局党组会', 'target': '会议听取内审办关于修订、制定区XX局内部审计相关工作办法的情况汇报。'}, ...]
    return nodes, links


# file_path = './data/output.txt'
# nodes, links = get_nodes_and_lines(file_path)
# print(nodes, links)

# 编辑距离是指两个字符串之间，由一个转成另一个所需的最少编辑操作次数。许可的编辑操作仅包括删除、加入、取代字符串中的任何一个字符。
def edit_distance(str1, str2):
    # 数字必须相同
    num1_list = re.findall(r"\d+\.?\d*", str1)
    num2_list = re.findall(r"\d+\.?\d*", str2)
    if len(num1_list) != len(num2_list):
        return 1000
    for i in range(len(num1_list)):
        if num1_list[i] != num2_list[i]:
            return 1000

    # 数字不算
    str1 = str1.rstrip('0123456789')
    str2 = str2.rstrip('0123456789')
    matrix = [[i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                d = 0
            else:
                d = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)
    return matrix[len(str1)][len(str2)]


# print(edit_distance('abd', 'abhh'))

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


def merge(all_nodes, all_links, d_threshold):
    node_mapping = {}
    node_set = []
    for node in all_nodes:
        node_id = node['id']

        add_flag = 1  # 判断是否添加节点
        for i in range(len(node_set)):  # 找是否有相似或者相同的节点
            if node_id == node_set[i]['id']:  # 有相同节点
                # node_mapping[node_id] = node_set[i]['id']
                add_flag = 0
                break

            elif node_set[i]['group'] != 1 and edit_distance(node_id,
                                                             node_set[i]['id']) < d_threshold:  # 有相似节点（时间不算编辑距离）
                # if len(node_set[i]['id']) > len(node_id): # 保留短的那个,保留node_id
                #     node_mapping[node_set[i]['id']] = node_id # 这样直接替换会出问题，因为node_set[i]['id']之前可能被用于被替换别的字符，不能就这样不要node_set[i]['id']了
                #     node_set[i]['id'] = node_id
                # else: # 保留node_set[i]['id']
                #     node_mapping[node_id] = node_set[i]['id']
                node_mapping[node_id] = node_set[i][
                    'id']  # 避免修改node_set中已有的数据，只修改后来要加入node_set的数据 以避免a->b b->c的发生，只能a->b c->b
                add_flag = 0
                break
        if add_flag:  # 没有相似节点，添加至
            node_set.append(node)

    link_set = []
    for link in all_links:
        # 看是否要做节点映射
        if link['source'] in node_mapping.keys():
            link['source'] = node_mapping[link['source']]
        if link['target'] in node_mapping.keys():
            link['target'] = node_mapping[link['target']]

        add_flag = 1  # 判断是否添加边
        for i in range(len(link_set)):
            if link['source'] == link_set[i]['source'] and link['target'] == link_set[i]['target']:
                add_flag = 0
                break

        if add_flag:
            link_set.append(link)

    return node_set, link_set, node_mapping


if __name__ == "__main__":
    print(edit_distance('拨付武汉路小学房租经费', '拨付武汉路小学房租经费'))
    print(edit_distance('理顺教育局内部审计工作', '进一步理顺教育局内部审计工作'))

    # d_threshold = 5
    # file_dir = r'.\data'
    # all_files = get_all_files_in_folder(file_dir)
    # print("file num", len(all_files))
    #
    # all_nodes = []
    # all_links = []
    # for file in all_files:
    #     nodes,links = get_nodes_and_lines(file)
    #     all_nodes += nodes
    #     all_links += links
    #
    # node_set, link_set, node_mapping = merge(all_nodes, all_links, d_threshold)
    # print('node num', len(node_set))
    # print('link num', len(link_set))
    # print(node_set)
    # print(link_set)
    # print(node_mapping)
    #

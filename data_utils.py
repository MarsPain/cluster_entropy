import pandas as pd
import itertools
import operator
import sys
import pickle


def get_data(path):
    """
    从中药的原csv文件读取原始数据，并删除缺失数据
    :param path:中药csv文件的路径
    :return:datafram
    """
    df = pd.read_csv(path, encoding='utf8')
    series = df['symptom']
    series.dropna(inplace=True)  # 删掉nan
    return series


def root_to_word(path):
    """
    根据同义词表创建词根到词的dict
    :param path:同义词表的路径
    :return:dict{'词根0':['词','词','词']}
    """
    word_dict = {}
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            # seperate_word = line.strip().split(' ')
            seperate_word = line.strip().split()
            word_dict[seperate_word[0]] = seperate_word
    # print("combine_dict:",combine_dict)
    return word_dict


def word_to_root(path):
    """
    根据同义词表创建词到词根的dict
    :param path:同义词表的路径
    :return:dict{'词1':'词根0','词2':'词根0'...,'词n':'词根0'}
    """
    root_dict = {}
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            # words = lines[i].strip().split(' ')
            words = lines[i].strip().split()
            for word in words:
                # combine_dict[word]=i
                root_dict[word] = words[0]
    # print("combine_dict:",combine_dict)
    return root_dict


def dict_sort(root):
    """
    对词根出现的频率进行降序排列，然后将排序后的词根名称和出现的频数作为list返回
    :param root:词根出现频数的字典，键值对为（词根-出现频数）
    :return:list_name["词根1","词根2","词根3"..."词根n"]
    :return:list_frequecy[int,int,int...int]
    """
    list_name, list_frequecy = [], []
    reversed_list = sorted(root.items(), key=lambda x: x[1], reverse=True)
    # print("reversed_list", type(reversed_list), reversed_list)
    for i in reversed_list:
        list_name.append(i[0])
        list_frequecy.append(i[-1])
    print("list_name:", list_name, "\n", "list_frequecy:", list_frequecy)
    return list_name, list_frequecy


def combine_count(one_hot_data):
    """
    对属于同一个样本的词根进行两两组合，并获取每个组合的频数，如(0,1):5
    :param one_hot_data: type;dataFrame
    :return: dict{(0,1):15, (0,2):13,...,(n-1,n):2}
    """
    # row_len = one_hot_data.iloc[:,0].size
    row_len = len(one_hot_data)
    cols = list(one_hot_data.columns)
    # print("cols:", len(cols))
    word_map = dict(zip(cols, range(len(cols))))
    # print("wordMap:", wordMap)
    combinations_fre = {}
    for i in range(row_len):
        row = one_hot_data.iloc[i, :]   # 逐行选取一整行的数据
        # print("row:", row)
        list_word = list(row[row == 1].index)   # 获取值为1所在列的索引，即该行中出现的具体病症
        # print(("list_word:", list_word))
        combinations = list(itertools.combinations(list_word, 2))   # 对list_word中的元素进行两两组合
        # print("combinations:", combinations)
        for item in combinations:
            pre, suf = item  # 两两组合中的两个病症名称
            item = word_map[pre], word_map[suf]   # 获得病症到索引的映射
            combinations_fre[item] = (combinations_fre[item] if item in combinations_fre else 0) + 1
    # print("combinations_fre",combinations_fre.items())
    key_list = sorted(combinations_fre.items(), key=operator.itemgetter(0))  # 按照两两组合的大小进行排序(其实在这里进行排序没有意义，转成dict仍然无序)
    # print("key_list:", type(key_list), key_list)
    combinations_fre = dict(key_list)
    # print("combinations_fre", type(combinations_fre), combinations_fre)
    return combinations_fre


def index_2_word(root_name, combine_index):
    """
    通过list_name生成（0：当归）这样的dict，把list_num转成对应的中文
    :param root_name: 所有中药名的list
    :param combine_index:以数字组成的list/set/tuple（任意层）
    :return:list_num对应的中文
    """
    word_map = dict(enumerate(root_name))
    # 利用递归
    if isinstance(combine_index, (list, tuple, set)):
        new_list = list()
        for item in combine_index:
            new_list.append(index_2_word(root_name, item))
        return new_list
    else:
        return word_map[combine_index]


def word_2_index(list_name, list_word):
    word_map = dict(zip(list_name, range(len(list_name))))
    list_num = [[word_map[word] if word in word_map else word for word in i] for i in list_word]
    return list_num


def write_csv(name_list, file_path, *args):
    """
    将两两组合的互信息以及聚类结果输出到CSV文件中
    :param name_list:位于输出的csv第一行的列索引
    :param file_path:输出的csv路径
    :param args:参数列表，表示需要输出的内容，对应参数name_list中提到的内容
    :return:
    """
    if len(name_list) != len(args):
        print('list长度不对应！')
        sys.exit(1)
    series_list = []
    # 注意这里输出数据的技巧
    for i, name in enumerate(name_list):
        # print("i:", i, "\n", "name:", name)
        # 注意这里Series的用法，args是参数列表，代表两个列表，直接用整个列表构造Series，设置name为列索引
        column = pd.Series(args[i], name=name)
        # print("column:", column)
        series_list.append(column)
    data = pd.concat(series_list, axis=1)   # 对两个Series进行拼接
    # print("data:", data)
    # data = data.sort_values(by=name_list[1], ascending=False)
    data.to_csv(file_path, index=False, encoding='utf-8')
    return data


def cut_by_num(relatives_list, max_relatives_nums):
    """
    对list每个子list进行删除操作，保留前max_relatives_nums项
    :param relatives_list:亲友团列表
    :param max_relatives_nums:保留的亲友团个数
    :return:经过裁剪的亲友团列表
    """
    new_list = list()
    for i, row in enumerate(relatives_list):
        # print("i:", i, "\n", "row:", row)
        if len(row) > max_relatives_nums:
            new_list.append(row[:max_relatives_nums])
        else:
            new_list.append(row)
    return new_list


def save_pickle(file_name, input_data):
    with open(file_name, 'wb') as f:
        pickle.dump(input_data, f)

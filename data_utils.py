import pandas as pd
import itertools
import operator


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
    # print("list_name:", list_name, "\n", "list_frequecy:", list_frequecy)
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

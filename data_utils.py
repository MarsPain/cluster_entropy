import pandas as pd


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
    print("reversed_list", type(reversed_list), reversed_list)
    for i in reversed_list:
        list_name.append(i[0])
        list_frequecy.append(i[-1])
    # print("list_name:", list_name, "\n", "list_frequecy:", list_frequecy)
    return list_name, list_frequecy

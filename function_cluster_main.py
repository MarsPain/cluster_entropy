import pandas as pd
import numpy as np
from data_utils import get_data, root_to_word, word_to_root, dict_sort

medicine_path = 'data/test3.csv'    # 药物数据
thesaurus_path = "data/tongyici_3.txt"  # 同义词字典


class ClusterEntropy:
    def __init__(self):
        self.df = None  # 存储特征的one-hot变量
        self.list_name = None   # 存储排序后的词根名称，由于是有序的，所以可以作为词根到索引的映射字典，详见word_2_num和num_2_word
        self.list_frequency = None  # 存储排序后的词根频率

    def feature_to_vector(self):
        """
        创建并初始化ont-hot向量：从csv中读取药物数据，然后将功效特征转换为one-hot向量
        :return:
        """
        series = get_data(medicine_path)
        # print("series", series)
        word_2_root = root_to_word(thesaurus_path)  # 词到同义词根的映射字典
        root_2_word = word_to_root(thesaurus_path)     # 同义词根到词的映射字典
        # 创建并初始化一个DataFrame存储one-hot向量，第一行的列索引为词根
        self.df = pd.DataFrame(np.zeros((len(series), len(word_2_root))), columns=word_2_root.keys())
        for indexs in series.index:  # series去掉了nan值，index是不连贯的,所以用这种方法遍历
            item_str = series[indexs]
            if item_str == '':
                continue
            item_list = item_str.strip().split()
            for item in item_list:
                if item in root_2_word:
                    # 找到每个功效特征词的词根，然后在one-hot向量的相应索引处进行激活
                    self.df[root_2_word[item]].loc[indexs] = 1
                else:
                    print(item)  # 输出没有匹配的词，进行人工处理
        # 删除没有任何匹配的词根
        max_value = self.df.max()    # 返回df中每一列的最大值
        # print("max_value:", max_value)
        drop_list = list(max_value[max_value == 0].index)   # 找到最大值为0的列的索引（即没有出现过的词根）
        # print("drop_list:", len(drop_list))
        self.df = self.df.drop(drop_list, axis=1)   # 删除未出现过的词根

    def df_sort(self):
        """
        根据词频对df的列进行重新排序,并获得排列后的特征词和相应的品侧
        :return:
        """
        root_count = dict(self.df.sum())  # sum对每一列求和，即能得到每个词根出现的频数
        # print("count_dic:" ,count_dic)
        self.list_name, self.list_frequency = dict_sort(root_count)
        # print("list_name:", self.list_name, "\n", "list_frequency:", self.list_frequency)
        self.df = self.df.ix[:, self.list_name]
        # print(self.df)

if __name__ == "__main__":
    Cluster = ClusterEntropy()
    Cluster.feature_to_vector()
    Cluster.df_sort()

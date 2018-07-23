import pandas as pd
import numpy as np
from data_utils import get_data, root_to_word, word_to_root, dict_sort, combine_count, index_2_word, write_csv
from relatives import calculate_correlation, create_relatives

medicine_path = 'data/test3.csv'    # 药物数据的路径
thesaurus_path = "data/tongyici_3.txt"  # 同义词字典的路径
correlation_path = 'data/correlation.csv'   # 保存互信息的文件路径
max_relatives_nums = 8  # 最大的亲友团数量


class ClusterEntropy:
    def __init__(self):
        self.df = None  # 存储特征的one-hot变量
        self.root_name = None   # 存储排序后的词根名称，由于是有序的，所以可以作为词根到索引的映射字典，详见word_2_num和num_2_word
        self.root_fre = None    # 存储词根出现的频率，用于计算互信息
        self.combine_index = None  # 存储排序后的组合，用词根的索引表示
        self.combine_fre = None  # 存储词根的两两组合出现的频率，同样用于计算互信息
        self.combine_name = None  # 存储用词根名称表示的

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

    def root_frequency(self):
        """
        根据词频对df的列进行重新排序,并获得排列后的特征词和相应的频数,然后计算词根出现的频率
        :return:
        """
        root_count = dict(self.df.sum())  # sum对每一列求和，即能得到每个词根出现的频数
        # print("count_dic:" ,count_dic)
        self.root_name, root_nums = dict_sort(root_count)
        # print("list_name:", self.list_name, "\n", "list_frequency:", self.list_frequency)
        self.df = self.df.ix[:, self.root_name]
        # print(self.df)
        row_len = self.df.iloc[:, 0].size
        self.root_fre = [i / row_len for i in root_nums]   # 用于后面对互信息的计算
        # print(self.root_fre)

    def combine_frequency(self):
        """
        对属于同一个词根进行两两组合，并获取每个组合的频数，然后计算每个组合的频率
        :return:
        """
        combine_counts = combine_count(self.df)
        # print("combinations_dic_fre", combinations_dic_fre)
        self.combine_index, combine_nums = dict_sort(combine_counts)
        # print("combinations_list", combinations_list, "\n","combinations_frequency",combinations_frequency)
        row_len = self.df.iloc[:, 0].size
        """
        计算每个两两组合的频率，后面用于计算互信息，因为互信息是根据边缘熵和联合熵得到的，前面的单个词根的频率用于计算边缘熵
        两两组合的频率用于计算联合熵
        """
        self.combine_fre = [i / row_len for i in combine_nums]
        # print(self.combine_fre)

    def search_relatives(self):
        correlation = calculate_correlation(self.combine_index, self.combine_fre, self.root_fre)
        self.combine_name = index_2_word(self.root_name, self.combine_index)  # 将单独的词根和组合中的索引转换为词
        # 将互信息按照大小降序排列大小，然后再写入到csv中
        data = write_csv(['组合', '关联度系数'], correlation_path, self.combine_name, correlation)
        # 获取每个症状的亲友团list
        relatives_list = create_relatives(self.root_name, data, max_relatives_nums)
        # print("relatives_list", relatives_list)  # 这里的亲友团是用嵌套列表存储的，用字典存储应该更好吧？键值对为变量-亲友团列表

if __name__ == "__main__":
    Cluster = ClusterEntropy()
    Cluster.feature_to_vector()
    Cluster.root_frequency()
    Cluster.combine_frequency()
    Cluster.search_relatives()

import pandas as pd
import numpy as np
from data_utils import get_data, root_to_word, word_to_root

medicine_path = 'data/test3.csv'    # 药物数据
thesaurus_path = "data/tongyici_3.txt"  # 同义词字典

class cluster_entropy():
    def __init__(self):
        pass

    def feature_to_vector(self):
        """
        创建并初始化ont-hot向量：从csv中读取药物数据，然后将功效特征转换为one-hot向量
        :return:
        """
        series = get_data(medicine_path)
        # print("series", series)
        word_dict = root_to_word(thesaurus_path)  # 词到同义词根的映射字典
        root_dict = word_to_root(thesaurus_path)     # 同义词根到词的映射字典
        # 创建一个DataFrame存储one-hot向量，第一行的列索引为词根
        self.df = pd.DataFrame(np.zeros((len(series), len(word_dict))), columns=word_dict.keys())
        for indexs in series.index:  # series去掉了nan值，index是不连贯的,所以用这种方法遍历
            item_str = series[indexs]
            if item_str == '':
                continue
            item_list = item_str.strip().split()
            for item in item_list:
                if item in root_dict:
                    # 找到每个功效特征词的词根，然后在one-hot向量的相应索引处进行激活
                    self.df[root_dict[item]].loc[indexs] = 1
                else:
                    print(item)  # 输出没有匹配的词，进行人工处理

if __name__ == "__main__":
    Cluster = cluster_entropy()
    Cluster.feature_to_vector()

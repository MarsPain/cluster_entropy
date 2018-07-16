# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys
import itertools
import copy
import utils
import p1_preprocess as clus1
import p2_relatives as clus2
import p3_cluster as clus3


def gene_dic(path):
    """
    根据同义词表创建词根到词的dict
    :param path:同义词表的路径
    :return:{'词根0':['词','词','词']}
    """
    combine_dict = {}
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            seperate_word = line.strip().split(' ')
            combine_dict[seperate_word[0]] = seperate_word
    # print("combine_dict:",combine_dict)
    return combine_dict


def gene_dic_2(path):
    """
    根据同义词表创建词到词根的dict
    :param path:同义词表的路径
    :return:{'词1':'词根0','词2':'词根0'...,'词n':'词根0'}
    """
    combine_dict = {}
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            words = lines[i].strip().split(' ')
            for word in words:
                # combine_dict[word]=i
                combine_dict[word] = words[0]
    # print("combine_dict:",combine_dict)
    return combine_dict


def one_hot(list_name, input_data):
    # df = pd.DataFrame(np.zeros((length, len(list_name))), columns=list_name)
    pass


def group_clean(pkl_file):
    """
    把不同成员数的亲友团整理在一起
    :param pkl_file:
    :return:
    """
    group = utils.load_pickle(pkl_file)
    all_list = []
    for i in range(len(group) - 1, 1, -1):
        item = list(group[i])
        member_num = len(item[0])
        new_item = copy.deepcopy(item)
        for comb in itertools.combinations(item, 2):
            set1 = set(comb[0])
            set2 = set(comb[1])
            if len(set1 & set2) == member_num - 1:
                if comb[0] in new_item:
                    new_item.remove(comb[0])
                if comb[1] in new_item:
                    new_item.remove(comb[1])
        all_list.extend(new_item)
    return all_list


if __name__ == '__main__':
    df = pd.read_csv('data/test2.csv', encoding='utf8')
    series = df['主治实体_symptom']
    series.dropna(inplace=True)#删掉nan
    # series = series.replace(np.nan, '')
    new_dic = gene_dic('data/hebing.txt')
    new_dic_2 = gene_dic_2('data/hebing.txt')
    # 创建dataFrame存放onehot，横轴上的列索引标签为同义词的词根
    df = pd.DataFrame(np.zeros((len(series), len(new_dic))), columns=new_dic.keys())
    # print("df", df)
    # series去掉了nan值，index是不连贯的
    for indexs in series.index:
        item_str = series[indexs]
        if item_str == '':
            continue
        item_list = item_str.strip().split(' ')
        for item in item_list:
            if item in new_dic_2:
                df[new_dic_2[item]].loc[indexs] = 1 #在
            else:
                print(item)  # 输出没有匹配的字符
    # 删除没有任何匹配的词列
    max_value = df.max()    #返回df中每一行的最大值及最大值所在的列的索引
    # print("max_value:", max_value)
    drop_list = list(max_value[max_value == 0].index)
    df = df.drop(drop_list, axis=1)
    # we = df.columns.size
    # 计算所有症状中每个词的频数，排序
    count_dic = dict(df.sum())  #sum对每一列求和，即能得到每个词出现的频数
    # print("count_dic:" ,count_dic)
    list_name, list_frequency = clus1.dic_list(count_dic)
    # print(list_name, list_frequency)
    df = df.ix[:, list_name]  # 按照词频对列重新排序
    # print("df:", df)
    # 两两组合的频数，排序
    combinations_dic_fre = clus1.combinations_dic_2(df)
    # print("combinations_dic_fre", combinations_dic_fre)
    combinations_list, combinations_frequency = clus1.dic_list(combinations_dic_fre)
    # print("combinations_list", combinations_list, "\n","combinations_frequency",combinations_frequency)
    #计算每个词的频率和每个两两组合的频率，后面用于计算互信息，因为互信息是根据边缘熵和联合熵得到的，
    # 而熵又是基于每个变量的频率计算得到的
    row_len = df.iloc[:, 0].size
    # list_fre = [i/sum(list_frequency) for i in list_frequency]
    list_fre = [i / row_len for i in list_frequency]

    # aaa = sum(list_frequency)
    # combinations_fre = [i/sum(combinations_frequency) for i in combinations_frequency]
    combinations_fre = [i / row_len for i in combinations_frequency]
    # bbb = sum(combinations_frequency)

    # 2 计算互信息
    correlation = clus2.calculate_correlation(combinations_list, combinations_fre, list_fre)
    combinations_name = utils.num_2_word(list_name, combinations_list)  # num_2_word 数字转文字
    data = utils.write_csv(['组合', '关联度系数'], 'data/correlation.csv', combinations_name, correlation)
    # 得到每个症状的亲友团list
    relatives_list = clus2.relatives_2(list_name, data, 8)

    # 3 亲友团聚类
    clus3.cluster_main2(relatives_list, list_name)
    # 对每个group进行合并，得到最终的聚类
    group_5_all = group_clean('data/group5.csv.pkl')
    # group_5_all = utils.num_2_word(list_name, group_5_all)
    group_6_all = group_clean('data/group6.csv.pkl')
    # group_6_all = utils.num_2_word(list_name, group_6_all)
    group_7_all = group_clean('data/group7.csv.pkl')
    # group_7_all = utils.num_2_word(list_name, group_7_all)
    group_8_all = group_clean('data/group8.csv.pkl')
    # group_8_all = utils.num_2_word(list_name, group_8_all)
    utils.write_csv(['group_8', 'group7', 'group6', 'group5'], 'data/group_all.csv', group_8_all, group_7_all,
                    group_6_all, group_5_all)
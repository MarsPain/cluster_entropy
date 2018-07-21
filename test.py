import itertools
import pandas as pd

# [[a,b], [a,c], [a,d]]变为[b, c, d]
# def duplicate_removal(relatives_list, list_name):
#     result = []
#     for item in relatives_list:
#         new2 = []
#         for n in item:
#             for q in n:
#                 new2.append(q)
#         guo_du = list(set(new2))
#         guo_du.sort(key=new2.index)
#         if guo_du:
#             guo_du.remove(list_name[relatives_list.index(item)])
#         result.append(guo_du)
#     return result
#
# # l = [[[1,2], [1,3], [1,4]], [[4,1], [3,1], [2,1]]]
# # list_name = [1,2,3,4,5,6,7]
# l = [[["a","b"], ["a","c"], ["a","d"]], [["b","a"], ["c","b"], ["b","e"]]]
# list_name = ["a", "b", "c", "d", "e", "f"]
# #从测试结果来看，数字型列表的输出存在问题，但是字符型列表的输出又是正常的，考虑到处理的字符型列表，暂时搁置该问题
# print(duplicate_removal(l, list_name))

#itertools.combinations的使用方法
# l = [1,2,3,4,5,6]
# for i in itertools.combinations(l, 2):
#     print(i)

df = pd.DataFrame([[1,0,1,0], [0,1,1,0], [0,1,1,0], [0,0,0,0]])
row_len = df.iloc[:, 0].size
print(row_len)
print(df)
max_value = df.max()
drop_list = list(max_value[max_value == 0].index)   # 找到最大值为0所在的列的索引
print(drop_list)
# print("drop_list:", len(drop_list))
df = df.drop(drop_list, axis=1)
print(df)
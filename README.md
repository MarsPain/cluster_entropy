# 基于复杂系统熵聚类的中药聚类

代码参考了[中医方剂聚类](https://github.com/gcaxuxi/cluster_2)，主要在其基础上进行了代码的重构和优化，原项目是对中医方剂进行聚类，基于中医方剂的主治信息中的症状，本项目主要对中药进行聚类，主要基于中药的功效信息。

## 文件列表

function_cluster_main.py：包含主函数，针对中药的功效信息进行聚类

data_utils.py：包含对数据进行处理的函数

relatives.py：包含计算互信息和亲友团的函数

cluster：包含对亲友团进行聚类的函数

data：包含药物数据、同义词字典等文件

## 运行：

直接运行function_cluster_main.py即可，可设置min_relatives_nums和max_relatives_nums参数对亲友团数量进行限制。


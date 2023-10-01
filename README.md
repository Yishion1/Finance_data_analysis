# 金融数据分析

## 简介

本项目是基于python的pandas和seaborn包完成数据可视化和数据分析工作

## 分析报告
```python
print("Missing values in each column:\n{}".format(df.isnull().sum()))

检测文档中的缺失数据，结果如下所示：

Missing values in each column:
Age                   0
Sex                   0
Job                   0
Housing               0
Saving accounts     183
Checking account    394
Credit amount         0
Duration              0
Purpose               0

在Saving accounts和Checking accounts中均有数据缺失，可能是用户并没有创建这两个相关的账户导致数据缺失

![image](https://github.com/Yishion1/Finance_data_analysis/assets/66151793/503e5b26-3cb9-432f-abca-8e07dba85cbc)

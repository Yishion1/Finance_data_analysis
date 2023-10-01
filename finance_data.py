import numpy as np # linear algebra
import pandas as pd # data processing, CSV file
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.max_columns',None)
df=pd.read_csv("german_credit_data.csv")
#print(df.head)
df.drop(df.columns[0], inplace=True, axis=1)

print("Missing values in each column:\n{}".format(df.isnull().sum()))
#Out of 8 columns 2 contain missing values. Probably these are customers who don’t have one of these two accounts.


# 计算各个类别的计数
#检测性别
gender_counts = df['Sex'].value_counts()

# 绘制计数条形图
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='Sex', linewidth=3, palette="Set2", edgecolor='black')
plt.show()

#查看年龄
sns.countplot(data=df, x='Age', linewidth=3, palette="Set2", edgecolor='black')
plt.show()

#查看存款
sns.countplot(data=df, x='Saving accounts', linewidth=3, palette="Set2", edgecolor='black')
plt.show()
#性别与存款对应关系
plt.figure(figsize=(18,6))
sns.countplot(x=df['Sex'],hue=df['Saving accounts'],palette='summer',linewidth=3,edgecolor='white')
plt.title('Saving accounts')
plt.show()

#

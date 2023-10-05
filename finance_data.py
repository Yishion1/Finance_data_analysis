
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from sklearn.preprocessing import StandardScaler 
from sklearn.cluster import KMeans, AffinityPropagation
pd.set_option('display.max_columns',None)
df=pd.read_csv("german_credit_data.csv")
print(df.head)
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


sns.scatterplot(data=df,x='Credit amount',y='Duration',hue='Sex',palette="Set1")
plt.title('Saving accounts')
plt.show()

sns.scatterplot(data=df,x="Age",y="Credit amount", hue='Sex',palette=None )
plt.title('Credit VS Age')
plt.show()

import scipy.stats as stats
# 创建jointplot
r1 = sns.jointplot(x="Credit amount", y="Duration", data=df, kind="reg", height=8)

# 计算皮尔逊相关系数和p值
pearsonr, pvalue = stats.pearsonr(df["Credit amount"], df["Duration"])

# 在图上注解皮尔逊相关系数和p值
r1.ax_joint.text(0.05, 0.95, f'Pearsonr = {pearsonr:.2f}\np-value = {pvalue:.2e}', 
                 transform=r1.ax_joint.transAxes, 
                 verticalalignment='top', 
                 bbox=dict(boxstyle='round, pad=0.5', edgecolor='gray', facecolor='none'))

plt.show()

#统计信用卡开卡的不同目的计数
n_credits = df.groupby("Purpose")["Housing"].count().rename("Count").reset_index()
print(n_credits)
n_credits.sort_values(by=["Count"], ascending=False, inplace=True)
plt.figure(figsize=(10,6))
bar = sns.barplot(x="Purpose",y="Count",data=n_credits)
bar.set_xticklabels(bar.get_xticklabels(), rotation=60)
plt.ylabel("Number of granted credits")
plt.tight_layout()


#利用boxplot分析男女性别差异对于在不同变量关系之间否存在显著差异
def boxes(x,y,h,r=45):
    fig, ax = plt.subplots(figsize=(10,6))
    box = sns.boxplot(x=x,y=y, hue=h, data=df)
    box.set_xticklabels(box.get_xticklabels(), rotation=r)
    fig.subplots_adjust(bottom=0.2)
    plt.tight_layout()
boxes("Purpose","Credit amount","Sex")
boxes("Purpose","Duration","Sex")




#选择Age,Credit Amount ,Duration 进行聚类分析
cluster_data = df.loc[:,["Age","Credit amount", "Duration"]]

#观察数据分布情况
def distributions(df):
    fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=(8,8))
    sns.distplot(df["Age"], ax=ax1)
    sns.distplot(df["Credit amount"], ax=ax2)
    sns.distplot(df["Duration"], ax=ax3)
    plt.tight_layout()
distributions(cluster_data)

cluster_log = np.log(cluster_data)
distributions(cluster_log)

##寻找合适K值
#标准化距离
scaler = StandardScaler()
cluster_scaled = scaler.fit_transform(cluster_log)
from sklearn.metrics import silhouette_samples, silhouette_score

clusters_range = range(2,15)
random_range = range(210,220)
results =[]
for c in clusters_range:
    for r in random_range:
        clusterer = KMeans(n_clusters=c, random_state=r)
        cluster_labels = clusterer.fit_predict(cluster_scaled)
        silhouette_avg = silhouette_score(cluster_scaled, cluster_labels)
        results.append([c,r,silhouette_avg])
result = pd.DataFrame(results, columns=["n_clusters","seed","silhouette_score"])
pivot_km = pd.pivot_table(result, index="n_clusters", columns="seed",values="silhouette_score")
plt.figure(figsize=(15,6))
sns.heatmap(pivot_km, annot=True, linewidths=.5, fmt='.3f', cmap=sns.cm.rocket_r)
plt.tight_layout()

#选取k=3
kmeans_sel = KMeans(n_clusters=3, random_state=210).fit(cluster_scaled)
labels = pd.DataFrame(kmeans_sel.labels_)
clustered_data = cluster_data.assign(Cluster=labels)
grouped_km = clustered_data.groupby(['Cluster']).mean().round(1)
print(grouped_km)
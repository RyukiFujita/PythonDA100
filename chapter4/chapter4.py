import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 1.データ読み込み
uselog = pd.read_csv('use_log.csv')
print(uselog.isnull().sum())

customer = pd.read_csv('customer_join.csv')
print(customer.isnull().sum())

# 2.クラスタリング
customer_clustering = customer[["mean", "median", "max", "min", "membership_period"]].copy()
print(customer_clustering.head())

sc = StandardScaler()
customer_clustering_sc = sc.fit_transform(customer_clustering)
kmeans = KMeans(n_clusters=4, random_state=0)
clusters = kmeans.fit(customer_clustering_sc)
customer_clustering.loc[:,"cluster"] = clusters.labels_
print(customer_clustering["cluster"].unique())
print(customer_clustering.head())

# 3.クラスタリング結果を分析
customer_clustering.columns = ["月内平均", "月内中央値", "月内最大値", "月内最小値", "会員期間", "cluster"]
print(customer_clustering.groupby("cluster").count())
print(customer_clustering.groupby("cluster").mean())



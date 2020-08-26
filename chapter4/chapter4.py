import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

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

# 4.クラスタリング結果の可視化
X = customer_clustering_sc
pca = PCA(n_components=2)
pca.fit(X)
x_pca = pca.transform(X)
pca_df = pd.DataFrame(x_pca)
pca_df["cluster"] = customer_clustering["cluster"]

for i in customer_clustering["cluster"].unique() :
    tmp = pca_df.loc[pca_df["cluster"]==i]
    plt.scatter(tmp[0],tmp[1])

# plt.show()

# 5.クラスタリング結果をもとに退会顧客の傾向を把握
customer_clustering = pd.concat([customer_clustering, customer], axis=1)
print(customer_clustering)
print(customer_clustering.groupby(["cluster", "is_deleted"], as_index=False).count()[["cluster", "is_deleted", "customer_id"]])
print(customer_clustering.groupby(["cluster", "routine_flg"], as_index=False).count()[["cluster", "routine_flg", "customer_id"]])

# 6.翌月の利用回数予測のための準備
uselog["usedate"] = pd.to_datetime(uselog["usedate"])
uselog["年月"] = uselog["usedate"].dt.strftime("%Y%m")
uselog_months = uselog.groupby(["年月", "customer_id"], as_index=False).count()
uselog_months.rename(columns={"log_id":"count"}, inplace=True)
del uselog_months["usedate"]
# a_user = uselog_months.loc[uselog_months["customer_id"]=="AS002855", ["年月", "count"]]
# print(a_user)
print(uselog_months.head())

year_months = list(uselog_months["年月"].unique())
predict_data = pd.DataFrame()
for i in range(6, len(year_months)) :
    tmp = uselog_months.loc[uselog_months["年月"]==year_months[i]]
    tmp.rename(columns={"count":"count_pred"}, inplace=True)
    for j in range(1,7) :
        tmp_before = uselog_months.loc[uselog_months["年月"]==year_months[i-j]]
        del tmp_before["年月"]
        tmp_before.rename(columns={"count":f"count_{j-1}"}, inplace=True)
        tmp = pd.merge(tmp, tmp_before, on="customer_id", how="left")
    predict_data = pd.concat([predict_data, tmp], ignore_index=True)
print(predict_data.head())

predict_data = predict_data.dropna()
predict_data = predict_data.reset_index(drop=True)
print(predict_data.head())



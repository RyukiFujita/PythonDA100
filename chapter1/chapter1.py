import pandas as pd
import matplotlib.pyplot as plt

# 1 csv読み込みと先頭5行表示
customer_master = pd.read_csv('customer_master.csv')
print(customer_master.head())

item_master = pd.read_csv('item_master.csv')
print(item_master.head())

transaction_1 = pd.read_csv('transaction_1.csv')
print(transaction_1.head())

transaction_2 = pd.read_csv('transaction_2.csv')
print(transaction_2.head())

transaction_detail_1 = pd.read_csv('transaction_detail_1.csv')
print(transaction_detail_1.head())

transaction_detail_2 = pd.read_csv('transaction_detail_2.csv')
print(transaction_detail_2.head())

# 2 ユニオン
transaction = pd.concat([transaction_1, transaction_2], ignore_index=True)
transaction_detail = pd.concat([transaction_detail_1, transaction_detail_2], ignore_index=True)

# 3 ジョイン1
join_data = pd.merge(transaction_detail, transaction[["transaction_id", "payment_date", "customer_id"]], on="transaction_id", how="left")
print(join_data.head())

# 4 ジョイン2
join_data = pd.merge(join_data, customer_master, on="customer_id", how="left")
print(join_data.head())
join_data = pd.merge(join_data, item_master, on="item_id", how="left")
print(join_data.head())

# 5 priceの列を作る
join_data["price"] = join_data["quantity"] * join_data["item_price"]
print(join_data[["quantity", "item_price"]].head())

# 6 データ検算
print(join_data["price"].sum())
print(transaction["price"].sum())

# 7 各種統計量の把握
print(join_data.isnull().sum())
print(join_data.describe())
print(join_data["payment_date"].min())
print(join_data["payment_date"].max())

# 8 月別の集計
print(join_data.dtypes)
join_data["payment_date"] = pd.to_datetime(join_data["payment_date"])
join_data["payment_month"] = join_data["payment_date"].dt.strftime("%Y%m")
print(join_data[["payment_date", "payment_month"]].head())
print(join_data.groupby("payment_month").sum()["price"])

# 9 月別かつ商品別の集計
print(join_data.groupby(["payment_month", "item_name"]).sum()[["price", "quantity"]])
print(pd.pivot_table(join_data, index="item_name", columns="payment_month", values=["price", "quantity"], aggfunc="sum"))

# 10 商品別の売上推移を可視化
graph_data = pd.pivot_table(join_data, index="payment_month", columns="item_name", values="price", aggfunc="sum")
print(graph_data.head())
plt.plot(list(graph_data.index), graph_data["PC-A"], label="PC-A")
plt.plot(list(graph_data.index), graph_data["PC-B"], label="PC-B")
plt.plot(list(graph_data.index), graph_data["PC-C"], label="PC-C")
plt.plot(list(graph_data.index), graph_data["PC-E"], label="PC-E")
plt.plot(list(graph_data.index), graph_data["PC-D"], label="PC-D")
plt.legend()
plt.show()

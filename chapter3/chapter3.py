import pandas as pd

# 1.データ読み込み
use_log = pd.read_csv("use_log.csv")
print(len(use_log))
print(use_log.head())

customer = pd.read_csv("customer_master.csv")
print(len(customer))
print(customer.head())

class_master = pd.read_csv("class_master.csv")
print(len(class_master))
print(class_master.head())

campaign_master = pd.read_csv("campaign_master.csv")
print(len(campaign_master))
campaign_master.head()

# 2.顧客データを整形しよう
customer_join = pd.merge(customer, class_master, on="class", how="left")
customer_join = pd.merge(customer_join, campaign_master, on="campaign_id", how="left")
print(customer_join.head())

customer_join.isnull().sum()

# 3.顧客データの基礎集計をしよう
customer_join.groupby("class_name").count()["customer_id"]
customer_join.groupby("gender").count()["customer_id"]
customer_join.groupby("is_deleted").count()["customer_id"]

customer_join["start_date"] = pd.to_datetime(customer_join["start_date"])
customer_start = customer_join.loc[customer_join["start_date"] > pd.to_datetime("20180401")]
print(len(customer_start))

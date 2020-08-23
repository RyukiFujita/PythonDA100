import pandas as pd
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from copy import copy

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
print(customer_join.groupby("class_name").count()["customer_id"])
print(customer_join.groupby("gender").count()["customer_id"])
print(customer_join.groupby("is_deleted").count()["customer_id"])

customer_join["start_date"] = pd.to_datetime(customer_join["start_date"])
customer_start = customer_join.loc[customer_join["start_date"] > pd.to_datetime("20180401")]
print(len(customer_start))

# 4.最新月の顧客を集計
customer_join["end_date"] = pd.to_datetime(customer_join["end_date"])
customer_newer = customer_join.loc[(customer_join["end_date"] >= pd.to_datetime("20190331")) | (customer_join["end_date"].isna())]
# customer_newer = customer_join.loc[(customer_join["end_date"].isna())]
print(len(customer_newer))
print(customer_newer["end_date"].unique())

print(customer_newer.groupby("class_name").count()["customer_id"])
print(customer_newer.groupby("campaign_name").count()["customer_id"])
print(customer_newer.groupby("gender").count()["customer_id"])

# 5.利用履歴データの集計
use_log["usedate"] = pd.to_datetime(use_log["usedate"])
use_log["年月"] = use_log["usedate"].dt.strftime("%Y%m")
use_log_months = use_log.groupby(["年月", "customer_id"], as_index=False).count()
use_log_months.rename(columns={"log_id":"count"}, inplace=True)
del use_log_months["usedate"]
print(use_log_months.head())
use_log_customer = use_log_months.groupby("customer_id").agg(["mean", "median", "max", "min"])["count"]
use_log_customer = use_log_customer.reset_index(drop= False)
print(use_log_customer.head())

# 6.定期利用フラグの作成
use_log["weekday"] = use_log["usedate"].dt.weekday
print(use_log.head())
use_log_weekday = use_log.groupby(["customer_id", "年月", "weekday"], as_index = False).count()[["customer_id", "年月", "weekday", "log_id"]]
use_log_weekday.rename(columns={"log_id":"count"}, inplace=True)
print(use_log_weekday.head())

use_log_weekday = use_log_weekday.groupby("customer_id", as_index=False).max()[["customer_id", "count"]]
use_log_weekday["routine_flag"] = 0
use_log_weekday["routine_flag"] = use_log_weekday["routine_flag"].where(use_log_weekday["count"]<4, 1)
print(use_log_weekday.head())

# 7.顧客データと利用履歴データの結合
customer_join = pd.merge(customer_join, use_log_customer, on="customer_id", how="left")
customer_join = pd.merge(customer_join, use_log_weekday[["customer_id", "routine_flag"]], on="customer_id", how="left")
print(customer_join.head())

# 8.会員期間の計算
customer_join["calc_date"] = customer_join["end_date"]
customer_join["calc_date"] = customer_join["calc_date"].fillna(pd.to_datetime("20190430"))
customer_join["membership_period"] = 0
for i in range(len(customer_join)) :
    delta = relativedelta(customer_join.loc[i, "calc_date"], customer_join.loc[i, "start_date"])
    customer_join.loc[i, "membership_period"] = delta.years*12 + delta.months
print(customer_join.head())

# 9.顧客行動の各種統計量の把握
print(customer_join[["mean", "median", "max", "min"]].describe())
print(customer_join.groupby("routine_flag").count()["customer_id"])

plt.hist(customer_join["membership_period"])
plt.show()

# 10.退会ユーザと継続ユーザの違いを把握する
customer_end = customer_join.loc[customer_join["is_deleted"]==1]
print(customer_end.describe())
customer_stay = customer_join.loc[customer_join["is_deleted"]==0]
print(customer_stay.describe())

customer_join.to_csv("customer_join.csv", index=False)

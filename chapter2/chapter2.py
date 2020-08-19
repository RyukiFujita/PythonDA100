import pandas as pd

# 1.データの読み込み
uriage_data = pd.read_csv("uriage.csv")
print(uriage_data.head())

kokyaku_data = pd.read_excel("kokyaku_daicho.xlsx")
print(kokyaku_data.head())

# 2.データの揺れをチェック
print(uriage_data["item_name"].head())
print(uriage_data["item_price"].head())

# 3.データの揺れを残したまま集計
uriage_data["purchase_date"] = pd.to_datetime(uriage_data["purchase_date"])
uriage_data["purchase_month"] = uriage_data["purchase_date"].dt.strftime("%Y%m")
res = uriage_data.pivot_table(index="purchase_month", columns="item_name", aggfunc="size", fill_value=0)
print(res)

res = uriage_data.pivot_table(index="purchase_month", columns="item_name", values="item_price", aggfunc="sum", fill_value=0)
print(res)

# 4.商品面の揺れを補正
print(pd.unique(uriage_data.item_name))
print(len(pd.unique(uriage_data.item_name)))
uriage_data["item_name"] = uriage_data["item_name"].str.upper()
uriage_data["item_name"] = uriage_data["item_name"].str.replace("　", "")
uriage_data["item_name"] = uriage_data["item_name"].str.replace(" ", "")
uriage_data.sort_values(by=["item_name"], ascending=True)
print(pd.unique(uriage_data.item_name))
print(len(pd.unique(uriage_data.item_name)))

# 5.金額欠損値の補完
print(uriage_data.isnull().any(axis=0))
flg_is_null = uriage_data["item_price"].isnull()
print(flg_is_null)
for trg in list(uriage_data.loc[flg_is_null, "item_name"].unique()) :
    price = uriage_data.loc[(~flg_is_null) & (uriage_data["item_name"] == trg), "item_price"].max()
    uriage_data["item_price"].loc[(flg_is_null) & (uriage_data["item_name"]==trg)] = price
print(uriage_data.head())
print(uriage_data.isnull().any(axis=0))

for trg in list(uriage_data["item_name"].sort_values().unique()) :
    max_price = uriage_data.loc[uriage_data["item_name"]==trg]["item_price"].max()
    min_price = uriage_data.loc[uriage_data["item_name"]==trg]["item_price"].min(skipna=False)
    print(f"{trg} max:{max_price}, min{min_price}")

# 6.顧客名の揺れを補正
print(kokyaku_data["顧客名"].head())
print(uriage_data["customer_name"].head())
kokyaku_data["顧客名"] = kokyaku_data["顧客名"].str.replace("　", "")
kokyaku_data["顧客名"] = kokyaku_data["顧客名"].str.replace(" ", "")
print(kokyaku_data["顧客名"].head())

# 7.日付の補正
flg_is_serial = kokyaku_data["登録日"].astype("str").str.isdigit()
print(flg_is_serial.sum())

from_serial = pd.to_timedelta(kokyaku_data.loc[flg_is_serial, "登録日"].astype("float"), unit="D") + pd.to_datetime("1900/01/01")
print(from_serial)
from_string = pd.to_datetime(kokyaku_data.loc[~flg_is_serial, "登録日"])
print(from_string)
kokyaku_data["登録日"] = pd.concat([from_string, from_serial])

kokyaku_data["登録年月"] = kokyaku_data["登録日"].dt.strftime("%Y%m")
result = kokyaku_data.groupby("登録年月").count()["顧客名"]
print(result)
print(len(kokyaku_data))

# 8.顧客名をキーにしてjoin
join_data = pd.merge(uriage_data, kokyaku_data, left_on="customer_name", right_on="顧客名", how="left")
join_data = join_data.drop("customer_name",axis=1)
print(join_data)

# 9.配置を整理してdump
dump_data = join_data[["purchase_date",
                       "purchase_month",
                       "item_name",
                       "item_price",
                       "顧客名",
                       "かな",
                       "地域",
                       "メールアドレス",
                       "登録日"]]
print(dump_data)
dump_data.to_csv("dump_data.csv", index=False)

# 10.データの集計
import_data = pd.read_csv("dump_data.csv")
xItem_yPurcaseMonth_vNum = import_data.pivot_table(index="purchase_month", columns="item_name", aggfunc="size", fill_value=0)
print(xItem_yPurcaseMonth_vNum)
xItem_yPurcaseMonth_vPrice = import_data.pivot_table(index="purchase_month", columns="item_name", values="item_price", aggfunc="sum", fill_value=0)
print(xItem_yPurcaseMonth_vPrice)
xCustomer_yPurcaseMonth_vNum = import_data.pivot_table(index="purchase_month", columns="顧客名", aggfunc="size", fill_value=0)
print(xCustomer_yPurcaseMonth_vNum)
xRegion_yPurcaseMonth_vNum = import_data.pivot_table(index="purchase_month", columns="地域", aggfunc="size", fill_value=0)
print(xRegion_yPurcaseMonth_vNum)
away_customers = pd.merge(uriage_data, kokyaku_data, left_on="customer_name", right_on="顧客名", how="right")
print(away_customers[away_customers["purchase_date"].isnull()][["顧客名", "メールアドレス", "登録日"]])





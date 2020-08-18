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
fig_is_null = uriage_data["item_price"].isnull()
print(fig_is_null)
for trg in list(uriage_data.loc[fig_is_null, "item_name"].unique()) :
    price = uriage_data.loc[(~fig_is_null) & (uriage_data["item_name"] == trg), "item_price"].max()
    uriage_data["item_price"].loc[(fig_is_null) & (uriage_data["item_name"]==trg)] = price
print(uriage_data.head())
print(uriage_data.isnull().any(axis=0))

for trg in list(uriage_data["item_name"].sort_values().unique()) :
    max_price = uriage_data.loc[uriage_data["item_name"]==trg]["item_price"].max()
    min_price = uriage_data.loc[uriage_data["item_name"]==trg]["item_price"].min(skipna=False)
    print(f"{trg} max:{max_price}, min{min_price}")


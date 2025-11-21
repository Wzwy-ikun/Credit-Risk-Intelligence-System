import pandas as pd

# 1. 读取数据
customers = pd.read_csv("customers.csv", parse_dates=["register_date"])
credit = pd.read_csv("credit_accounts.csv", parse_dates=["open_date"])
repay = pd.read_csv("repayment.csv", parse_dates=["due_date", "repay_date"])

print("===== 开始构建逾期风险特征 =====")

# -----------------------------------------------------------
# 1. 近 3 个月账单（2024-04、2024-05、2024-06）
# -----------------------------------------------------------
recent_repay = repay[repay["bill_month"].isin(["2024-04", "2024-05", "2024-06"])]

# 每个账户 → 最近 3 月逾期次数
recent_overdue_count = recent_repay.groupby("account_id")["overdue_days"].apply(lambda x: (x > 0).sum()).reset_index()
recent_overdue_count.columns = ["account_id", "recent_3m_overdue_cnt"]

# 最大逾期天数
max_overdue_days = repay.groupby("account_id")["overdue_days"].max().reset_index()
max_overdue_days.columns = ["account_id", "max_overdue_days"]

# 平均逾期天数
avg_overdue_days = repay.groupby("account_id")["overdue_days"].mean().reset_index()
avg_overdue_days.columns = ["account_id", "avg_overdue_days"]

# 是否存在 30+ 天逾期（坏账标签）
is_default = repay.groupby("account_id")["is_default_30d"].max().reset_index()
is_default.columns = ["account_id", "has_30d_default"]

# -----------------------------------------------------------
# 2. 将账户级 → 用户级（一个用户可能有多张卡）
# -----------------------------------------------------------
# 首先把账户对应到用户
account_user = credit[["account_id", "customer_id"]]

# 合并所有风险特征
risk_df = account_user.merge(recent_overdue_count, on="account_id", how="left")
risk_df = risk_df.merge(max_overdue_days, on="account_id", how="left")
risk_df = risk_df.merge(avg_overdue_days, on="account_id", how="left")
risk_df = risk_df.merge(is_default, on="account_id", how="left")

# 对于无逾期记录的地方填 0
risk_df = risk_df.fillna(0)

# 用户级别聚合
risk_user_df = risk_df.groupby("customer_id").agg({
    "recent_3m_overdue_cnt": "sum",
    "max_overdue_days": "max",
    "avg_overdue_days": "mean",
    "has_30d_default": "max"   # 只要有一张卡违约 → 就算坏用户
}).reset_index()

# -----------------------------------------------------------
# 3. 保存文件
# -----------------------------------------------------------
risk_user_df.to_csv("risk_features_step3.csv", index=False, encoding="utf-8-sig")

print("🎉 风险特征工程完成！")
print("➡ 已生成：risk_features_step3.csv")
print(risk_user_df.head())

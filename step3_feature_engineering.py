import pandas as pd
from datetime import datetime

# 1. 读取数据
customers = pd.read_csv("customers.csv", parse_dates=["register_date"])
credit = pd.read_csv("credit_accounts.csv", parse_dates=["open_date"])
txn = pd.read_csv("transactions.csv", parse_dates=["txn_date"])
repay = pd.read_csv("repayment.csv", parse_dates=["due_date", "repay_date"])

# ===========================================================
# 【一】客户层特征工程（User-level Features）
# ===========================================================

print("===== 开始构建用户层特征 =====")

# -----------------------------------------------------------
# 1. 计算“持卡时长（月份）”
# -----------------------------------------------------------
current_date = datetime(2024, 7, 1)  # 假设分析日期为 2024-07-01

credit["open_months"] = ((current_date - credit["open_date"]).dt.days // 30)

# 每个客户可能有多张卡 → 取最早开卡日
customer_open_months = credit.groupby("customer_id")["open_months"].max().reset_index()
customer_open_months.columns = ["customer_id", "max_open_months"]

# -----------------------------------------------------------
# 2. 计算总授信额度（一个客户可能多张卡）
# -----------------------------------------------------------
customer_credit_limit = credit.groupby("customer_id")["credit_limit"].sum().reset_index()
customer_credit_limit.columns = ["customer_id", "total_credit_limit"]

# -----------------------------------------------------------
# 3. 计算 近3个月（2024-04~2024-06）的消费金额
# -----------------------------------------------------------
recent_txn = txn[txn["txn_date"] >= "2024-04-01"]

recent_spending = recent_txn.groupby("account_id")["amount"].sum().reset_index()
recent_spending.columns = ["account_id", "recent_3m_amount"]

# 将消费金额从 account_id → customer_id
recent_spending = recent_spending.merge(
    credit[["account_id", "customer_id"]],
    on="account_id",
    how="left"
)

customer_recent_3m = recent_spending.groupby("customer_id")["recent_3m_amount"].sum().reset_index()
customer_recent_3m.columns = ["customer_id", "recent_3m_amount"]

# 对没有消费的填 0
customer_recent_3m["recent_3m_amount"] = customer_recent_3m["recent_3m_amount"].fillna(0)

# -----------------------------------------------------------
# 4. 授信额度使用率（消费 / 授信额度）
# -----------------------------------------------------------
customer_feature_df = customers.merge(customer_open_months, on="customer_id", how="left")
customer_feature_df = customer_feature_df.merge(customer_credit_limit, on="customer_id", how="left")
customer_feature_df = customer_feature_df.merge(customer_recent_3m, on="customer_id", how="left")

customer_feature_df["credit_usage_rate"] = (
    customer_feature_df["recent_3m_amount"] / customer_feature_df["total_credit_limit"]
).fillna(0)

# -----------------------------------------------------------
# 5. 输出初步特征文件
# -----------------------------------------------------------
customer_feature_df.to_csv("customer_features_step3.csv", index=False, encoding="utf-8-sig")

print("🎉 用户层特征工程完成！")
print("➡ 已生成：customer_features_step3.csv")
print(customer_feature_df.head())

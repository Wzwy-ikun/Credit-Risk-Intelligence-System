import pandas as pd

print("===== Step 4（修正版）：开始合并最终建模数据 =====")

# ❶ 读取 Step3 Part1 生成的用户特征表（已经包含了 age、gender 等基础信息）
customer_features = pd.read_csv("customer_features_step3.csv")

# ❷ 读取 Step3 Part2 生成的风险特征表
risk_features = pd.read_csv("risk_features_step3.csv")

# ===========================================================
# 【一】按 customer_id 合并全部特征
# ===========================================================
df = customer_features.merge(risk_features, on="customer_id", how="left")

# ===========================================================
# 【二】简单处理缺失值（风控行业常规做法）
# ===========================================================
df = df.fillna({
    "recent_3m_amount": 0,
    "credit_usage_rate": 0,
    "recent_3m_overdue_cnt": 0,
    "max_overdue_days": 0,
    "avg_overdue_days": 0,
    "has_30d_default": 0
})

# 将 has_30d_default 作为模型标签（目标变量）
df["label_default"] = df["has_30d_default"]

print("当前字段列表：")
print(df.columns.tolist())

# ===========================================================
# 【三】输出最终模型数据集（覆盖旧文件）
# ===========================================================
df.to_csv("model_dataset.csv", index=False, encoding="utf-8-sig")

print("🎉 修正版建模数据已生成！")
print("➡ 文件名：model_dataset.csv")
print(df.head())
print("\n数据集形状：", df.shape)

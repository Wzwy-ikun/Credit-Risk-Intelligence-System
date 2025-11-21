import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, recall_score, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

print("===== Step 5：违约预测模型训练 =====")

# 1. 读取最终数据集
df = pd.read_csv("model_dataset.csv")

# -------------------------------------------------------------
# 2. 选择用于建模的特征（风控中常用的关键特征）
feature_cols = [
    "age", "max_open_months", "total_credit_limit",
    "recent_3m_amount", "credit_usage_rate",
    "recent_3m_overdue_cnt", "max_overdue_days",
    "avg_overdue_days"
]

X = df[feature_cols]
y = df["label_default"]  # 目标变量（是否违约）

# 🔥 关键步骤：把特征里的 NaN 统一填成 0，避免模型报错
X = X.fillna(0)

# 可选：打印一下每一列还有没有 NaN（正常情况应该都是 0）
print("每个特征里 NaN 的数量：")
print(X.isna().sum())


# -------------------------------------------------------------
# 3. 划分训练集 / 测试集
# -------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# -------------------------------------------------------------
# 4. 建立逻辑回归模型（风控最常用）
# -------------------------------------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

logit = LogisticRegression(max_iter=500)
logit.fit(X_train_scaled, y_train)

y_pred_logit = logit.predict(X_test_scaled)
y_prob_logit = logit.predict_proba(X_test_scaled)[:, 1]

# -------------------------------------------------------------
# 5. 建立随机森林模型（表现更好）
# -------------------------------------------------------------
rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=6,
    random_state=42
)
rf.fit(X_train, y_train)

y_pred_rf = rf.predict(X_test)
y_prob_rf = rf.predict_proba(X_test)[:, 1]

# -------------------------------------------------------------
# 6. 输出模型评估结果（风控最关注 Recall/AUC）
# -------------------------------------------------------------
print("\n===== 逻辑回归模型表现 =====")
print("Accuracy:", accuracy_score(y_test, y_pred_logit))
print("Recall:", recall_score(y_test, y_pred_logit))
print("F1 Score:", f1_score(y_test, y_pred_logit))
print("AUC:", roc_auc_score(y_test, y_prob_logit))

print("\n===== 随机森林模型表现 =====")
print("Accuracy:", accuracy_score(y_test, y_pred_rf))
print("Recall:", recall_score(y_test, y_pred_rf))
print("F1 Score:", f1_score(y_test, y_pred_rf))
print("AUC:", roc_auc_score(y_test, y_prob_rf))

# -------------------------------------------------------------
# 7. 打印随机森林模型的特征重要性
# -------------------------------------------------------------
importance = pd.DataFrame({
    "feature": feature_cols,
    "importance": rf.feature_importances_
}).sort_values(by="importance", ascending=False)

print("\n===== 随机森林特征重要性（从高到低）=====")
print(importance)

# 保存特征重要性到文件
importance.to_csv("model_feature_importance.csv", index=False, encoding="utf-8-sig")

print("\n🎉 Step 5 完成！")
print("➡ 已生成模型特征重要性：model_feature_importance.csv")

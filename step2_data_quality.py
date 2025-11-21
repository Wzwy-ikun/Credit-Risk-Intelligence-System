import pandas as pd

# 读取 csv
customers = pd.read_csv("customers.csv", parse_dates=["register_date"])
credit = pd.read_csv("credit_accounts.csv", parse_dates=["open_date"])
txn = pd.read_csv("transactions.csv", parse_dates=["txn_date"])
repay = pd.read_csv("repayment.csv", parse_dates=["due_date", "repay_date"])

print("==========【1. 查看各表数据类型】==========")
print(customers.dtypes)
print(credit.dtypes)
print(txn.dtypes)
print(repay.dtypes)

print("\n==========【2. 检查缺失值情况】==========")
print("customers 缺失值：\n", customers.isnull().sum())
print("credit_accounts 缺失值：\n", credit.isnull().sum())
print("transactions 缺失值：\n", txn.isnull().sum())
print("repayment 缺失值：\n", repay.isnull().sum())

print("\n==========【3. 检查金额/额度异常值】==========")
# 检查是否有负数
print("交易金额是否存在负数：", (txn["amount"] < 0).sum())
print("授信额度是否存在负数：", (credit["credit_limit"] < 0).sum())
print("账单金额是否存在负数：", (repay["statement_amount"] < 0).sum())
print("还款金额是否存在负数：", (repay["repay_amount"] < 0).sum())

print("\n==========【4. 检查逾期天数是否为异常值（负数）】==========")
print("逾期天数为负数的条数：", (repay["overdue_days"] < 0).sum())

print("\n==========【5. 检查日期字段的最大最小范围】==========")
print("交易日期范围：", txn["txn_date"].min(), "~", txn["txn_date"].max())
print("开户日期范围：", credit["open_date"].min(), "~", credit["open_date"].max())
print("注册日期范围：", customers["register_date"].min(), "~", customers["register_date"].max())
print("还款日期范围：", repay["repay_date"].min(), "~", repay["repay_date"].max())

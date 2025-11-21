import pandas as pd

# 1. 读取 4 个 csv 文件，并把日期字段解析为日期类型
customers = pd.read_csv("customers.csv", parse_dates=["register_date"])
credit_accounts = pd.read_csv("credit_accounts.csv", parse_dates=["open_date"])
transactions = pd.read_csv("transactions.csv", parse_dates=["txn_date"])
repayment = pd.read_csv("repayment.csv", parse_dates=["due_date", "repay_date"])

# 2. 简单查看每张表的前 5 行，确认结构是否正常
print("==== customers（客户表）前 5 行 ====")
print(customers.head())
print()

print("==== credit_accounts（信用卡账户表）前 5 行 ====")
print(credit_accounts.head())
print()

print("==== transactions（交易表）前 5 行 ====")
print(transactions.head())
print()

print("==== repayment（还款表）前 5 行 ====")
print(repayment.head())
print()

# 3. 查看每张表的行数和列数
print("customers 形状：", customers.shape)
print("credit_accounts 形状：", credit_accounts.shape)
print("transactions 形状：", transactions.shape)
print("repayment 形状：", repayment.shape)

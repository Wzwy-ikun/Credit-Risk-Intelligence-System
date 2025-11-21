import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_customers(num_customers: int = 50) -> pd.DataFrame:
    random.seed(42)
    np.random.seed(42)

    customer_ids = [f"C{str(i).zfill(4)}" for i in range(1, num_customers + 1)]
    genders = np.random.choice(["male", "female"], num_customers)
    ages = np.random.randint(20, 55, num_customers)
    edu_levels = np.random.choice(["高中", "本科", "研究生"], num_customers)
    income_levels = np.random.choice(["0-5k", "5k-10k", "10k-20k", "20k+"], num_customers)
    cities = np.random.choice(["杭州", "上海", "深圳", "成都", "北京"], num_customers)
    register_dates = [
        datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1500))
        for _ in range(num_customers)
    ]
    channels = np.random.choice(["online", "branch", "promotion"], num_customers)

    customers_df = pd.DataFrame({
        "customer_id": customer_ids,
        "gender": genders,
        "age": ages,
        "edu_level": edu_levels,
        "income_level": income_levels,
        "city": cities,
        "register_date": register_dates,
        "channel": channels
    })

    return customers_df


def generate_credit_accounts(customers_df: pd.DataFrame, num_accounts: int = 80) -> pd.DataFrame:
    customer_ids = customers_df["customer_id"].tolist()

    account_ids = [f"A{str(i).zfill(4)}" for i in range(1, num_accounts + 1)]
    account_customers = np.random.choice(customer_ids, num_accounts)
    open_dates = [
        datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1500))
        for _ in range(num_accounts)
    ]
    credit_limits = np.random.choice([10000, 15000, 20000, 30000, 50000, 80000], num_accounts)
    card_types = np.random.choice(["标准卡", "金卡", "白金卡"], num_accounts)
    annual_fees = [200 if t == "标准卡" else 400 if t == "金卡" else 600 for t in card_types]
    statuses = np.random.choice(["正常", "冻结", "注销"], num_accounts, p=[0.85, 0.1, 0.05])

    credit_df = pd.DataFrame({
        "account_id": account_ids,
        "customer_id": account_customers,
        "open_date": open_dates,
        "credit_limit": credit_limits,
        "card_type": card_types,
        "annual_fee": annual_fees,
        "status": statuses
    })

    return credit_df


def generate_transactions(credit_df: pd.DataFrame, num_txn: int = 300) -> pd.DataFrame:
    account_ids = credit_df["account_id"].tolist()

    txn_ids = [f"T{str(i).zfill(5)}" for i in range(1, num_txn + 1)]
    txn_accounts = np.random.choice(account_ids, num_txn)
    txn_dates = [
        datetime(2023, 1, 1) + timedelta(days=random.randint(0, 400))
        for _ in range(num_txn)
    ]
    amounts = np.random.randint(50, 20000, num_txn)
    merchant_categories = np.random.choice(
        ["餐饮", "电商", "线下零售", "家电", "旅游", "奢侈品"],
        num_txn
    )
    is_online = np.random.choice([0, 1], num_txn)
    txn_cities = np.random.choice(["杭州", "上海", "深圳", "成都", "北京"], num_txn)

    txn_df = pd.DataFrame({
        "txn_id": txn_ids,
        "account_id": txn_accounts,
        "txn_date": txn_dates,
        "amount": amounts,
        "merchant_category": merchant_categories,
        "is_online": is_online,
        "city": txn_cities
    })

    return txn_df


def generate_repayment(credit_df: pd.DataFrame, num_bills: int = 150) -> pd.DataFrame:
    account_ids = credit_df["account_id"].tolist()

    repay_accounts = np.random.choice(account_ids, num_bills)
    bill_months = np.random.choice(["2024-03", "2024-04", "2024-05", "2024-06"], num_bills)
    statement_amounts = np.random.randint(500, 30000, num_bills)

    repay_amounts = []
    due_dates = []
    repay_dates = []
    overdue_days_list = []
    is_default_list = []

    for i in range(num_bills):
        # 到期日
        due = datetime(2024, random.randint(4, 6), random.randint(1, 28))
        due_dates.append(due)

        # 模拟实际还款日期（可能提前、按时、或逾期）
        delay = random.randint(-3, 50)  # 负数=提前，还可以大幅逾期
        repay = due + timedelta(days=delay)
        repay_dates.append(repay)

        overdue = max(0, delay)
        overdue_days_list.append(overdue)

        # 30 天以上逾期视为违约
        is_default_list.append(1 if overdue >= 30 else 0)

        # 逾期越严重，还款金额越可能偏少
        if overdue >= 30:
            repay_amounts.append(statement_amounts[i] * random.uniform(0.1, 0.7))
        else:
            repay_amounts.append(statement_amounts[i] * random.uniform(0.7, 1.1))

    repay_df = pd.DataFrame({
        "account_id": repay_accounts,
        "bill_month": bill_months,
        "statement_amount": statement_amounts,
        "repay_amount": np.round(repay_amounts, 2),
        "due_date": due_dates,
        "repay_date": repay_dates,
        "overdue_days": overdue_days_list,
        "is_default_30d": is_default_list
    })

    return repay_df


def main():
    # 1. 生成 customers 表
    customers_df = generate_customers(num_customers=50)
    customers_df.to_csv("customers.csv", index=False, encoding="utf-8-sig")

    # 2. 生成 credit_accounts 表
    credit_df = generate_credit_accounts(customers_df, num_accounts=80)
    credit_df.to_csv("credit_accounts.csv", index=False, encoding="utf-8-sig")

    # 3. 生成 transactions 表
    txn_df = generate_transactions(credit_df, num_txn=300)
    txn_df.to_csv("transactions.csv", index=False, encoding="utf-8-sig")

    # 4. 生成 repayment 表
    repay_df = generate_repayment(credit_df, num_bills=150)
    repay_df.to_csv("repayment.csv", index=False, encoding="utf-8-sig")

    print("✅ 数据文件已生成：customers.csv, credit_accounts.csv, transactions.csv, repayment.csv")


if __name__ == "__main__":
    main()

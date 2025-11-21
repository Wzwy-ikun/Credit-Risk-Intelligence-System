# Credit-Risk-Intelligence-System
**Python + MySQL + Excel + Tableau 
# 📊 智能风控分析系统（Credit Risk Intelligence System）
> **Python + MySQL + Excel + Tableau 全流程项目｜金融科技方向最强作品集之一**  
> 真实模拟银行/消费金融风控团队的业务场景：从数据生成、清洗、入库、分析、评分卡模型构建，到最终的风控可视化仪表盘。

---

# 🧭 项目简介（Overview）

本项目完整复刻了金融科技公司/银行风控部门的一条业务链路，围绕 **“用户信用风险评估”** 构建。  
你可以将项目理解成一个迷你但真实的 **“智能风控中台”**：

- 使用 **Python** 生成真实结构的数据、完成清洗与特征工程  
- 使用 **MySQL** 搭建业务数据库并进行风控 SQL 分析  
- 使用 **Excel** 进行人工检查、数据字典整理  
- 使用 **Tableau** 构建可对管理层展示的风控可视化仪表盘（Dashboard）  
- 构建了一个简单但专业的 **评分卡模型（Scorecard）** 用于客户风险评级  
- 最终形成可以在面试、作品集、求职中展示的完整解决方案  

本项目具有高度的展示价值，完全达到企业级 BI / 风控分析水平。

---

# 📂 项目结构（Project Structure）
```
├── data/
│ ├── customers.csv
│ ├── credit_accounts.csv
│ ├── transactions.csv
│ ├── repayment.csv
│ ├── risk_scorecard_data.csv
│ └── （所有数据均由 Python 自动生成）
│
├── python/
│ ├── step1_generate_data.py # 生成客户、授信、交易、还款数据
│ ├── step2_clean_data.py # 数据清洗 + 缺失值检查
│ ├── step3_feature_engineering.py # 基础特征工程
│ ├── step5_model_training.py # 模拟评分卡模型训练
│ └── utils/ # 业务规则、数据生成函数
│
├── mysql/
│ ├── create_tables.sql # 创建数据库与四张业务表
│ ├── load_data.sql # LOAD DATA 导入 CSV
│ ├── risk_sql_analysis.sql # 11 条风控分析 SQL
│ └── feature_sql.sql # 合成评分卡训练数据的 SQL
│
├── tableau/
│ ├── dashboard.twbx # 风控终极仪表盘（截图可见下文）
│ └── charts/ # 单张图表文件（象限图、双轴图等）
│
└── README.md # 当前文件
```

---

# 🛠 使用技术栈（Tech Stack）

| 技术 | 用途 |
|------|------|
| **Python** | 数据生成、数据清洗、特征工程、模型训练 |
| **MySQL** | 风控数据落库、风控 SQL 分析、业务指标提取 |
| **Excel** | 数据字典、字段验证、格式检查 |
| **Tableau** | 风控仪表盘、可视化图表、管理层展示 |

此项目覆盖数据分析师/金融科技岗位在工业级环境下最常用的工具组合。

---

# 🧪 数据生成（Python）

项目使用 Python 生成了 4 类业务数据：

| 文件 | 数据量 | 描述 |
|------|--------|------|
| `customers.csv` | N 行 | 客户基础信息（年龄、收入层、城市） |
| `credit_accounts.csv` | N 行 | 授信额度、授信深度、账户 ID |
| `transactions.csv` | M 行 | 消费行为数据（交易金额、交易日期） |
| `repayment.csv` | M 行 | 还款表现、逾期标签（is_default_30d） |

### 生成逻辑（示例）：

```python
income = random.choice(["0-5k", "5k-10k", "10k-20k", "20k+"])
limit = random.randint(2000, 50000)
is_default = 1 if random.random() < default_probability else 0
```
数据真实模拟银行客户行为特征，可直接用于风控分析。

🗄 数据落地 MySQL（Database Modeling）

数据库：

credit_risk_db

业务表：

customers

credit_accounts

repayment

transactions

创建表结构
```
CREATE TABLE customers (
    customer_id VARCHAR(20),
    age INT,
    income_level VARCHAR(20),
    city VARCHAR(20)
);

```
导入数据（LOAD DATA）
```
LOAD DATA INFILE '/xxx/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
IGNORE 1 ROWS;
```
📈 风控分析 SQL（核心业务分析）

项目包含 11 条企业级风控分析 SQL，部分如下：

① 城市维度违约率
```
SELECT city, AVG(is_default_30d) AS default_rate
FROM repayment r
JOIN credit_accounts ca ON r.account_id = ca.account_id
GROUP BY city;

```
② 收入层级 × 风险分析
③ 授信额度结构分析
④ 用户画像分析（Age × Income × Credit）
⑤ 交易行为风险检测
⑥ 客群分层 SQL
⑦ 账单周期风险监控

所有 SQL 分析最终形成可视化输入。

🤖 风控评分卡模型（Scorecard Model）

评分卡由三类特征组成：

income_score（收入）

credit_score（授信）

spend_score（消费行为）

评分公式（Tableau 计算字段）：
```
(
    [income_score] * 0.3 +
    [credit_score] * 0.3 +
    [spend_score] * 0.4
) * 25
```
风险等级：
```
IF [risk_score] < 40 THEN "低风险"
ELSEIF [risk_score] < 70 THEN "中风险"
ELSE "高风险"
END
```
📊 Tableau 可视化成果（Charts）
项目包含多个核心图表，各图可在 dashboard.twbx 中查看。

📌 图表 A：整体违约率 KPI（核心指标）



📌 图表 B：风险等级分布（低 / 中 / 高）



📌 图表 C：授信策略象限图（额度 × 风险）｜风控最经典图

用途：

优质客户（高额度 × 低风险）

需提额客户

高风险客户

授信过度提醒

（插入象限图截图）

📌 图表 D：收入 × 风险分析



📌 图表 E：城市违约率（City Risk）



📌 图表 F：最终双轴图（Risk Segmentation + Default Rate）

蓝柱 → 客户数量

红线 → 违约率



📊 总览仪表盘（Dashboard Overview）

仪表盘包含：

KPI 风控指标

风险分层柱状图

授信策略象限图

城市风险

收入分层风险

最终双轴风险表现图





🌟 项目亮点（你的简历可以写这些）

✔ 完整复刻企业级风控分析流程（从 Python 到 Tableau）

✔ 掌握金融科技业务理解（授信、违约、账单周期、消费行为）

✔ 构建专业评分卡模型（Scorecard）

✔ 制作高质量可视化仪表盘

✔ SQL 分析深度匹配银行风控岗要求
🚀 如何运行项目
git clone
 https://github.com/Wzwy-ikun
cd 项目目录
pip install -r requirements.txt
运行 Python 文件生成 CSV

导入到 MySQL

执行 SQL 生成分析结果

打开 Tableau 查看 dashboard










































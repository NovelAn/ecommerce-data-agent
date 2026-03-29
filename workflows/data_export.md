# 数据导出 (Data Export Workflow)

## 触发场景

- 数据明细导出
- 临时数据查询
- 二次分析需求
- 数据备份

## 流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                        数据导出流程                              │
└─────────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│ Step 1: 需求确认 (需求分析师)                                   │
│   • 需要哪些数据？                                              │
│   • 时间范围？                                                  │
│   • 筛选条件？                                                  │
│   • 输出格式？                                                  │
└───────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│ Step 2: 数据抽取 (ETL 工程师)                                   │
│   • 编写 SQL                                                    │
│   • 执行查询                                                    │
│   • 数据校验                                                    │
└───────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│ Step 3: Excel 生成 (报告设计师)                                 │
│   • 格式化                                                      │
│   • 添加说明                                                    │
│   • 生成文件                                                    │
└───────────────────────────────────────────────────────────────┘
```

## Excel 工作簿结构

### 标准导出模板

```
工作簿名称: {数据类型}_{时间范围}_{导出日期}.xlsx

├── Sheet 1: 概览
│   ├── 数据说明
│   ├── 时间范围
│   ├── 筛选条件
│   ├── 记录数量
│   └── 导出时间
│
├── Sheet 2: 明细数据
│   ├── 表头（加粗、背景色）
│   ├── 数据行
│   └── 自动筛选
│
├── Sheet 3: 汇总统计
│   ├── 按维度汇总
│   ├── 合计行
│   └── 占比计算
│
└── Sheet 4: 字段说明
    ├── 字段名称
    ├── 字段含义
    ├── 数据类型
    └── 取值范围
```

### 格式规范

```python
# Excel 格式化规则
formatting = {
    'header': {
        'bold': True,
        'bg_color': '#4472C4',
        'font_color': 'white',
        'border': 1
    },
    'number': {
        'num_format': '#,##0'
    },
    'currency': {
        'num_format': '¥#,##0.00'
    },
    'percent': {
        'num_format': '0.00%'
    },
    'date': {
        'num_format': 'yyyy-mm-dd'
    }
}
```

## 常见导出场景

### 场景 1: 订单明细导出
```sql
-- 订单明细导出 SQL
SELECT
    order_id,
    user_id,
    order_time,
    pay_time,
    channel,
    province,
    city,
    product_count,
    order_amount,
    discount_amount,
    pay_amount,
    coupon_code,
    status
FROM orders
WHERE created_at BETWEEN '{start_date}' AND '{end_date}'
ORDER BY created_at DESC;
```

### 场景 2: 用户行为导出
```sql
-- 用户行为导出 SQL
SELECT
    user_id,
    event_date,
    event_type,
    page_name,
    session_id,
    device_type,
    traffic_source,
    stay_duration
FROM user_events
WHERE DATE(timestamp) BETWEEN '{start_date}' AND '{end_date}'
ORDER BY user_id, timestamp;
```

### 场景 3: 商品销售汇总
```sql
-- 商品销售汇总导出 SQL
SELECT
    sku_id,
    sku_name,
    category_l1,
    category_l2,
    brand,
    SUM(quantity) as total_qty,
    SUM(amount) as total_amount,
    COUNT(DISTINCT order_id) as order_count,
    COUNT(DISTINCT user_id) as buyer_count
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'paid'
    AND o.created_at BETWEEN '{start_date}' AND '{end_date}'
GROUP BY sku_id, sku_name, category_l1, category_l2, brand
ORDER BY total_amount DESC;
```

## 输出模板

### 概览 Sheet
```
===========================================
              数据导出说明
===========================================

数据类型：{数据类型}
时间范围：{start_date} 至 {end_date}
筛选条件：{filters}
记录数量：{record_count} 条
导出时间：{export_time}
导出人  ：{exporter}

注意事项：
1. 数据仅供内部使用
2. 请勿外传
3. 如有疑问请联系数据分析团队

===========================================
```

### 字段说明 Sheet
```
| 字段名称 | 字段含义 | 数据类型 | 示例值 |
|----------|----------|----------|--------|
| order_id | 订单编号 | String | ORD20240101001 |
| user_id | 用户ID | String | U123456 |
| pay_amount | 实付金额 | Decimal | 99.00 |
| status | 订单状态 | String | paid/cancelled |
```

## 大数据量处理

### 分片导出
```python
# 超过 10 万条记录时分片导出
def export_large_data(query, chunk_size=100000):
    sheets = []
    for i, chunk in enumerate(query_results_in_chunks(query, chunk_size)):
        sheet_name = f"数据_{i+1}"
        sheets.append((sheet_name, chunk))
    return sheets
```

### 压缩处理
```python
# 超过 50MB 时压缩
def export_with_compression(data, filename):
    if get_size(data) > 50 * 1024 * 1024:
        return create_zip(data, filename)
    return create_excel(data, filename)
```

## 示例调用

```
导出上个月所有订单明细到 Excel
```

```
导出最近 7 天的用户行为数据，包括页面浏览、加购、下单
```

```
导出 Q1 的商品销售汇总表，按品类分组
```

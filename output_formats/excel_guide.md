# Excel 输出格式指南

## 适用场景

| 场景 | 推荐程度 | 说明 |
|------|----------|------|
| 数据明细导出 | ⭐⭐⭐⭐⭐ | 最佳选择 |
| 二次分析需求 | ⭐⭐⭐⭐⭐ | 最佳选择 |
| 数据备份 | ⭐⭐⭐⭐⭐ | 最佳选择 |
| 周报/月报 | ⭐⭐⭐⭐ | 配合 HTML/PPT |
| 高管汇报 | ⭐⭐ | 作为补充材料 |

## 工作簿结构

### 标准 4 Sheet 结构

```
📁 report_YYYYMMDD.xlsx
├── 📄 1. 概览 (Overview)
│   ├── 数据说明
│   ├── 时间范围
│   ├── 筛选条件
│   └── 汇总指标
│
├── 📄 2. 明细数据 (Data)
│   ├── 表头（格式化）
│   ├── 数据行
│   └── 自动筛选
│
├── 📄 3. 汇总分析 (Summary)
│   ├── 维度汇总
│   ├── 趋势数据
│   └── 对比分析
│
└── 📄 4. 字段说明 (Fields)
    ├── 字段名称
    ├── 含义
    ├── 类型
    └── 示例
```

## 格式规范

### 表头样式
```python
header_format = {
    'bold': True,
    'bg_color': '#4472C4',
    'font_color': 'white',
    'border': 1,
    'alignment': 'center'
}
```

### 数据类型格式
```python
formats = {
    'number': '#,##0',           # 1,234,567
    'currency': '¥#,##0.00',     # ¥1,234.56
    'percent': '0.00%',          # 12.34%
    'date': 'yyyy-mm-dd',        # 2024-01-15
    'datetime': 'yyyy-mm-dd hh:mm:ss'
}
```

### 条件格式
```python
# 正负值颜色
conditional_format = {
    'type': 'cell',
    'criteria': '>',
    'value': 0,
    'format': {'font_color': 'green'}
}

# 数据条
data_bar = {
    'type': 'data_bar',
    'bar_color': '#63C384'
}
```

## Sheet 模板

### 概览 Sheet
```
╔══════════════════════════════════════════════════════════════╗
║                      数据导出说明                              ║
╠══════════════════════════════════════════════════════════════╣
║ 数据类型：订单明细                                             ║
║ 时间范围：2024-01-01 至 2024-01-31                            ║
║ 筛选条件：状态=已支付, 金额>0                                  ║
║ 记录数量：125,678 条                                           ║
║ 导出时间：2024-02-01 10:30:00                                  ║
║ 导出人  ：数据分析团队                                         ║
╠══════════════════════════════════════════════════════════════╣
║                      核心指标汇总                              ║
╠══════════════════════════════════════════════════════════════╣
║ GMV：     ¥ 12,345,678.90                                      ║
║ 订单量：  125,678 单                                           ║
║ 客单价：  ¥ 98.25                                              ║
║ 退款率：  2.34%                                                ║
╚══════════════════════════════════════════════════════════════╝

注意事项：
1. 数据仅供内部使用，请勿外传
2. 如有疑问请联系数据分析团队
3. 数据截止时间为导出时间
```

### 字段说明 Sheet
| 字段名称 | 字段含义 | 数据类型 | 示例值 | 备注 |
|----------|----------|----------|--------|------|
| order_id | 订单编号 | String | ORD20240101001 | 唯一标识 |
| user_id | 用户ID | String | U123456 | 关联用户表 |
| pay_amount | 实付金额 | Decimal | 99.00 | 单位：元 |
| status | 订单状态 | String | paid | paid/cancelled/refunded |
| created_at | 创建时间 | DateTime | 2024-01-01 10:30:00 | 北京时间 |

## 常见导出场景

### 订单明细
```
字段：order_id, user_id, channel, province, city,
      product_count, order_amount, discount_amount,
      pay_amount, coupon_code, status, created_at, paid_at
```

### 用户行为
```
字段：user_id, event_date, event_type, page_name,
      session_id, device_type, traffic_source, stay_duration
```

### 商品销售
```
字段：sku_id, sku_name, category_l1, category_l2, brand,
      total_qty, total_amount, order_count, buyer_count
```

## 大数据量处理

### 分片策略
| 数据量 | 处理方式 |
|--------|----------|
| < 10万 | 单文件 |
| 10-50万 | 多 Sheet |
| > 50万 | 分文件 + ZIP 压缩 |

### 列数限制
- Excel 2007+: 16,384 列
- Excel 2003: 256 列

### 行数限制
- Excel 2007+: 1,048,576 行
- Excel 2003: 65,536 行

## 使用 document-skills:xlsx

调用现有 skill 生成 Excel：

```
使用 xlsx skill 创建一个 Excel 文件：
- Sheet 1: 概览页，包含数据说明和汇总指标
- Sheet 2: 订单明细数据，共 {count} 条记录
- 表头加粗、背景色 #4472C4
- 数字格式化为千分位
- 金额格式化为货币格式
```

## 文件命名规范

```
{类型}_{时间范围}_{日期}.xlsx

示例：
- orders_202401_20240201.xlsx
- user_behavior_7d_20240115.xlsx
- product_sales_q4_202401.xlsx
- daily_report_20240115.xlsx
```

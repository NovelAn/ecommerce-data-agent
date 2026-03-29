# 快速 Recap (Quick Recap Workflow)

## 触发场景

- 日常数据复盘
- 周报/日报
- 快速数据检查
- 会议前准备

## 流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                        快速 Recap 流程                           │
│                    (目标: 10-30 分钟完成)                        │
└─────────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│ Step 1: 数据快取 (ETL 工程师)                                  │
│   • 使用预定义 SQL 模板                                        │
│   • 抽取核心指标                                               │
│   • 自动质量检查                                               │
└───────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│ Step 2: 快速分析 (商业分析师)                                  │
│   • 计算环比/同比                                              │
│   • 识别显著变化                                               │
│   • 标注异常点                                                 │
└───────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│ Step 3: 生成 HTML Recap (报告设计师)                           │
│   • 使用标准模板                                               │
│   • 自动填充数据                                               │
│   • 生成可交互报告                                             │
└───────────────────────────────────────────────────────────────┘
```

## 标准指标集

### 交易指标
```sql
-- 标准 Recap 指标
SELECT
    'GMV' as metric,
    SUM(pay_amount) as value
FROM orders
WHERE status = 'paid'
    AND created_at >= {start_date}

UNION ALL

SELECT
    '订单量' as metric,
    COUNT(*) as value
FROM orders
WHERE status = 'paid'
    AND created_at >= {start_date}

UNION ALL

SELECT
    '客单价' as metric,
    AVG(pay_amount) as value
FROM orders
WHERE status = 'paid'
    AND created_at >= {start_date}
```

### 用户指标
```sql
-- 用户相关指标
SELECT
    'DAU' as metric,
    COUNT(DISTINCT user_id) as value
FROM user_events
WHERE DATE(timestamp) = {date}

UNION ALL

SELECT
    '新客数' as metric,
    COUNT(DISTINCT user_id) as value
FROM orders
WHERE is_first_order = 1
    AND DATE(created_at) = {date}
```

## HTML Recap 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数据 Recap - {date}</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1000px; margin: 0 auto; }

        .header {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .header h1 {
            font-size: 20px;
            color: #333;
            margin-bottom: 8px;
        }
        .header .date {
            font-size: 14px;
            color: #666;
        }

        .metrics-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-bottom: 20px;
        }
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .metric-card .label {
            font-size: 13px;
            color: #666;
            margin-bottom: 8px;
        }
        .metric-card .value {
            font-size: 26px;
            font-weight: 600;
            color: #333;
        }
        .metric-card .change {
            font-size: 12px;
            margin-top: 8px;
            padding: 4px 8px;
            border-radius: 4px;
            display: inline-block;
        }
        .metric-card .change.up {
            background: #dcfce7;
            color: #16a34a;
        }
        .metric-card .change.down {
            background: #fee2e2;
            color: #dc2626;
        }

        .chart-section {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .chart-section h3 {
            font-size: 16px;
            margin-bottom: 16px;
            color: #333;
        }
        .chart-container {
            height: 300px;
        }

        .insights {
            background: #fffbeb;
            border-left: 4px solid #f59e0b;
            border-radius: 0 12px 12px 0;
            padding: 16px 20px;
            margin-bottom: 20px;
        }
        .insights h3 {
            font-size: 14px;
            color: #92400e;
            margin-bottom: 12px;
        }
        .insights ul {
            list-style: none;
        }
        .insights li {
            font-size: 14px;
            color: #333;
            padding: 6px 0;
            padding-left: 20px;
            position: relative;
        }
        .insights li::before {
            content: '•';
            position: absolute;
            left: 0;
            color: #f59e0b;
        }

        .actions {
            background: #f0fdf4;
            border-left: 4px solid #22c55e;
            border-radius: 0 12px 12px 0;
            padding: 16px 20px;
        }
        .actions h3 {
            font-size: 14px;
            color: #166534;
            margin-bottom: 12px;
        }
        .actions ul {
            list-style: none;
        }
        .actions li {
            font-size: 14px;
            color: #333;
            padding: 6px 0;
            padding-left: 20px;
            position: relative;
        }
        .actions li::before {
            content: '✓';
            position: absolute;
            left: 0;
            color: #22c55e;
        }

        .footer {
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 每日数据 Recap</h1>
            <div class="date">数据日期：{date} | 生成时间：{generated_at}</div>
        </div>

        <div class="metrics-row">
            <div class="metric-card">
                <div class="label">GMV</div>
                <div class="value">¥{gmv}</div>
                <div class="change {gmv_trend}">{gmv_change}% 环比</div>
            </div>
            <div class="metric-card">
                <div class="label">订单量</div>
                <div class="value">{orders}</div>
                <div class="change {orders_trend}">{orders_change}% 环比</div>
            </div>
            <div class="metric-card">
                <div class="label">客单价</div>
                <div class="value">¥{aov}</div>
                <div class="change {aov_trend}">{aov_change}% 环比</div>
            </div>
            <div class="metric-card">
                <div class="label">DAU</div>
                <div class="value">{dau}</div>
                <div class="change {dau_trend}">{dau_change}% 环比</div>
            </div>
        </div>

        <div class="chart-section">
            <h3>GMV 趋势（近7天）</h3>
            <div id="trend-chart" class="chart-container"></div>
        </div>

        <div class="insights">
            <h3>💡 今日发现</h3>
            <ul>
                <li>{insight_1}</li>
                <li>{insight_2}</li>
                <li>{insight_3}</li>
            </ul>
        </div>

        <div class="actions">
            <h3>✅ 建议行动</h3>
            <ul>
                <li>{action_1}</li>
                <li>{action_2}</li>
            </ul>
        </div>

        <div class="footer">
            数据来源：{data_source} | 如有疑问请联系数据分析团队
        </div>
    </div>

    <script>
        // 趋势图
        const trendChart = echarts.init(document.getElementById('trend-chart'));
        trendChart.setOption({
            tooltip: { trigger: 'axis' },
            grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
            xAxis: {
                type: 'category',
                data: {dates}
            },
            yAxis: {
                type: 'value',
                axisLabel: { formatter: '¥{value}' }
            },
            series: [{
                type: 'line',
                data: {gmv_values},
                smooth: true,
                areaStyle: { opacity: 0.1 },
                itemStyle: { color: '#667eea' }
            }]
        });
    </script>
</body>
</html>
```

## 时间目标

| 复杂度 | 目标时间 | 指标数量 | 图表数量 |
|--------|----------|----------|----------|
| 简单 | 10 分钟 | 4 个 | 1 个 |
| 标准 | 20 分钟 | 8 个 | 2 个 |
| 详细 | 30 分钟 | 12 个 | 3 个 |

## 示例调用

```
生成昨日 GMV Recap，输出 HTML 格式
```

```
做一份上周数据的快速复盘，包括 GMV、订单量、用户数
```

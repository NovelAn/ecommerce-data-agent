# Ecommerce Data Agent - 电商数据分析智能体团队

一套专为电商数据分析设计的多智能体协作系统，支持需求分析、ETL、商业分析、可视化、报告生成全流程。

## 🎯 适用场景

- 电商数据分析（GMV、转化率、用户行为等）
- 数据 ETL 全流程
- 多格式报告输出（HTML/Excel/PPT）
- 交互式数据看板
- 商业洞察与策略建议

## 🤖 智能体团队

| Agent | 职责 | 输出 |
|-------|------|------|
| **需求分析师** | 梳理分析需求、产出分析文档 | 需求文档、分析计划 |
| **ETL 工程师** | 数据抽取、清洗、转换 | SQL、数据质量报告 |
| **商业分析师** | 指标计算、趋势分析、异常检测 | 分析结论、数据洞察 |
| **可视化工程师** | 图表配置、BI 对接、编码式可视化 | ECharts 配置、BI 看板 |
| **报告设计师** | 多格式报告输出（HTML/Excel/PPT） | 完整报告文件 |
| **策略顾问** | 业务建议、行动计划、风险评估 | 策略建议文档 |

## 📊 输出格式选择

| 场景 | 推荐格式 | 命令示例 |
|------|----------|----------|
| 日常数据 Recap | 交互式 HTML | `生成上周 GMV 的 HTML recap` |
| 周报/月报 | PPT + HTML | `做一份周报 PPT` |
| 数据明细表 | Excel | `导出订单数据到 Excel` |
| 高管汇报 | PPT | `给老板做季度汇报 PPT` |
| 深度分析 | HTML + Excel | `深度分析用户流失，输出 HTML 报告和 Excel 数据` |

## 🚀 快速开始

### 基础用法

```
分析上周的 GMV 趋势，生成一份可交互的 HTML recap
```

### 指定输出格式

```
分析 Q3 用户增长数据，输出 PPT 格式的汇报材料
```

### 完整分析流程

```
对上月销售数据进行全流程分析：
1. 需求梳理
2. 数据提取
3. 指标分析
4. 生成 Excel 数据表 + HTML 交互报告
5. 输出业务建议
```

## 🔄 程序化编排 (Programmatic Orchestration)

本技能现已支持**真正的多智能体程序化编排**，使用 **Hierarchical Orchestration** 模式。

### 架构图

```
用户请求
    ↓
┌─────────────────────────────────────────────────┐
│           Orchestrator (协调者)                  │
│  • 分析请求 → 确定工作流类型                      │
│  • 创建执行计划 → 分配任务                        │
│  • 协调 Agent 之间的上下文传递                    │
└─────────────────────────────────────────────────┘
    │
    ├→ 需求分析师  → 需求文档
    ├→ ETL工程师   → 清洗数据
    ├→ 业务分析师  → 分析结论
    ├→ 可视化工程师 → 图表配置
    ├→ 报告设计师  → 最终报告
    └→ 策略顾问    → 策略建议
```

### 工作流类型

| 类型 | Agent序列 | 预计时间 | 输出格式 |
|------|----------|---------|---------|
| **快速回顾** | 需求→ETL→分析→可视化 | 10-30分钟 | HTML |
| **完整分析** | 全部6个Agent | 1-2小时 | HTML/Excel |
| **高管汇报** | 需求→ETL→分析→策略→报告 | 30-60分钟 | PPT |
| **数据导出** | 需求→ETL→报告 | 15-30分钟 | Excel |

### Python SDK 使用示例

```python
from orchestration import EcommerceDataOrchestrator

# 创建编排器
orchestrator = EcommerceDataOrchestrator()

# 运行分析
result = await orchestrator.run_workflow(
    "分析最近30天的GMV趋势，找出增长点并给出建议"
)

# 查看结果
print(result["workflow_type"])  # "full_analysis"
print(result["output_format"])  # "html"
print(result["success"])        # True
```

### Claude Agent SDK 集成

```python
from claude_agent_sdk import query, ClaudeAgentOptions
from orchestration.agents import (
    REQUIREMENT_ANALYST,
    ETL_ENGINEER,
    BUSINESS_ANALYST,
    # ...
)

# 定义 subagents
agents = {
    "requirement_analyst": {
        "description": REQUIREMENT_ANALYST.goal,
        "prompt": REQUIREMENT_ANALYST.system_prompt,
        "tools": REQUIREMENT_ANALYST.tools
    },
    "etl_engineer": {
        "description": ETL_ENGINEER.goal,
        "prompt": ETL_ENGINEER.system_prompt,
        "tools": ETL_ENGINEER.tools
    },
    # ... 其他 agents
}

# 运行编排
async for message in query(
    prompt="分析Q3用户增长数据",
    options=ClaudeAgentOptions(
        allowed_tools=["Agent"],
        agents=agents
    )
):
    if "result" in message:
        print(message["result"])
```

### 智能路由

Orchestrator 会自动分析请求并选择最佳工作流：

| 请求关键词 | 自动选择工作流 |
|-----------|--------------|
| "快速"、"概览"、"日报" | quick_recap |
| "高管"、"汇报"、"PPT" | executive_report |
| "导出"、"明细"、"Excel" | data_export |
| 其他 | full_analysis |

## 📁 目录结构

```
ecommerce-data-agent/
├── SKILL.md                    # 本文件
├── agents/                     # 智能体定义 (文档型)
│   ├── requirement_analyst.md
│   ├── etl_engineer.md
│   ├── business_analyst.md
│   ├── visualization_engineer.md
│   ├── report_designer.md
│   └── strategy_advisor.md
├── orchestration/              # 🆕 程序化编排模块
│   ├── __init__.py
│   ├── orchestrator.py         # 主编排器
│   └── agents.py               # Agent 定义 (程序化)
├── workflows/                  # 工作流程
│   ├── full_analysis.md
│   ├── quick_recap.md
│   ├── executive_report.md
│   └── data_export.md
├── templates/                  # 模板文件
│   └── html/
│       └── report_base.html
├── output_formats/             # 输出格式指南
│   ├── html_guide.md
│   ├── excel_guide.md
│   └── ppt_guide.md
└── examples/                   # 示例文件
    ├── html/
    ├── excel/
    └── ppt/
```

## 🔗 依赖 Skills

本 Skill 可调用以下已安装的 skills：

- `document-skills:xlsx` - Excel 文件处理
- `document-skills:pptx` - PPT 文件处理
- `document-skills:frontend-design` - HTML/前端设计
- `multi-agent-orchestration` - 编排模式参考

## 📝 常用电商指标

### 核心交易指标
- GMV (Gross Merchandise Volume)
- 实付金额
- 订单量 / 成交订单数
- 客单价 (AOV)

### 用户指标
- DAU / MAU
- 新增用户数
- 留存率 (次日/7日/30日)
- 用户生命周期价值 (LTV)

### 转化指标
- 转化率 (CVR)
- 加购率
- 收藏率
- 跳失率

### 商品指标
- 动销率
- 售罄率
- 库存周转天数
- 商品退货率

## 💡 最佳实践

1. **明确输出格式** - 在需求中说明期望的报告格式
2. **提供时间范围** - 明确分析的时间维度
3. **说明受众** - 不同受众选择不同报告风格
4. **迭代优化** - 先快速生成初版，再迭代优化

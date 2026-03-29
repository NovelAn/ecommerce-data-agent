# Ecommerce Data Orchestrator - Main Orchestrator
# 电商数据分析编排器 - 层级编排模式

import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from datetime import datetime
import json

from .agents import (
    AgentDefinition,
    AgentRole,
    REQUIREMENT_ANALYST,
    ETL_ENGINEER,
    BUSINESS_ANALYST,
    VISUALIZATION_ENGINEER,
    REPORT_DESIGNER,
    STRATEGY_ADVISOR
)


class WorkflowType(Enum):
    """工作流类型"""
    QUICK_RECAP = "quick_recap"          # 快速回顾 (10-30分钟)
    FULL_ANALYSIS = "full_analysis"      # 完整分析 (1-2小时)
    EXECUTIVE_REPORT = "executive_report" # 高管汇报
    DATA_EXPORT = "data_export"          # 数据导出


class OutputFormat(Enum):
    """输出格式"""
    HTML = "html"
    EXCEL = "excel"
    PPT = "ppt"
    ALL = "all"


@dataclass
class TaskContext:
    """任务上下文 - 在Agent之间传递的共享状态"""
    request: str                              # 原始请求
    workflow_type: WorkflowType              # 工作流类型
    output_format: OutputFormat              # 输出格式

    # 阶段产出
    requirement_doc: Optional[str] = None    # 需求文档
    raw_data: Optional[Dict] = None          # 原始数据
    analysis_result: Optional[Dict] = None   # 分析结果
    visualizations: Optional[List] = None    # 可视化配置
    report: Optional[str] = None             # 报告内容
    strategies: Optional[List] = None        # 策略建议

    # 元数据
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    current_stage: str = "init"
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "request": self.request,
            "workflow_type": self.workflow_type.value,
            "output_format": self.output_format.value,
            "current_stage": self.current_stage,
            "errors": self.errors
        }


@dataclass
class AgentResult:
    """Agent执行结果"""
    agent_role: AgentRole
    success: bool
    output: Any
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict = field(default_factory=dict)


class EcommerceDataOrchestrator:
    """
    电商数据分析编排器

    使用层级编排模式(Hierarchical Orchestration):
    - Orchestrator 作为协调者，管理整体工作流
    - 6个专业Agent各司其职
    - 根据工作流类型决定调用哪些Agent
    """

    def __init__(self, model: str = "claude-opus-4-6"):
        self.model = model
        self.agents = {
            AgentRole.REQUIREMENT_ANALYST: REQUIREMENT_ANALYST,
            AgentRole.ETL_ENGINEER: ETL_ENGINEER,
            AgentRole.BUSINESS_ANALYST: BUSINESS_ANALYST,
            AgentRole.VISUALIZATION_ENGINEER: VISUALIZATION_ENGINEER,
            AgentRole.REPORT_DESIGNER: REPORT_DESIGNER,
            AgentRole.STRATEGY_ADVISOR: STRATEGY_ADVISOR,
        }

        # 工作流定义
        self.workflows = {
            WorkflowType.QUICK_RECAP: [
                AgentRole.REQUIREMENT_ANALYST,
                AgentRole.ETL_ENGINEER,
                AgentRole.BUSINESS_ANALYST,
                AgentRole.VISUALIZATION_ENGINEER,
            ],
            WorkflowType.FULL_ANALYSIS: [
                AgentRole.REQUIREMENT_ANALYST,
                AgentRole.ETL_ENGINEER,
                AgentRole.BUSINESS_ANALYST,
                AgentRole.VISUALIZATION_ENGINEER,
                AgentRole.REPORT_DESIGNER,
                AgentRole.STRATEGY_ADVISOR,
            ],
            WorkflowType.EXECUTIVE_REPORT: [
                AgentRole.REQUIREMENT_ANALYST,
                AgentRole.ETL_ENGINEER,
                AgentRole.BUSINESS_ANALYST,
                AgentRole.STRATEGY_ADVISOR,
                AgentRole.REPORT_DESIGNER,  # PPT输出
            ],
            WorkflowType.DATA_EXPORT: [
                AgentRole.REQUIREMENT_ANALYST,
                AgentRole.ETL_ENGINEER,
                AgentRole.REPORT_DESIGNER,  # Excel输出
            ],
        }

    def analyze_request(self, request: str) -> tuple[WorkflowType, OutputFormat]:
        """
        分析请求，确定工作流类型和输出格式

        这是Orchestrator的智能路由功能
        """
        request_lower = request.lower()

        # 确定工作流类型
        if any(kw in request_lower for kw in ["快速", "概览", "recap", "日报", "daily"]):
            workflow = WorkflowType.QUICK_RECAP
        elif any(kw in request_lower for kw in ["高管", "汇报", "ppt", "演示", "executive", "汇报"]):
            workflow = WorkflowType.EXECUTIVE_REPORT
        elif any(kw in request_lower for kw in ["导出", "明细", "export", "excel", "下载"]):
            workflow = WorkflowType.DATA_EXPORT
        else:
            workflow = WorkflowType.FULL_ANALYSIS

        # 确定输出格式
        if "html" in request_lower or "交互" in request_lower:
            output_format = OutputFormat.HTML
        elif "excel" in request_lower or "表格" in request_lower:
            output_format = OutputFormat.EXCEL
        elif "ppt" in request_lower or "演示" in request_lower:
            output_format = OutputFormat.PPT
        else:
            # 根据工作流类型选择默认格式
            default_formats = {
                WorkflowType.QUICK_RECAP: OutputFormat.HTML,
                WorkflowType.FULL_ANALYSIS: OutputFormat.HTML,
                WorkflowType.EXECUTIVE_REPORT: OutputFormat.PPT,
                WorkflowType.DATA_EXPORT: OutputFormat.EXCEL,
            }
            output_format = default_formats[workflow]

        return workflow, output_format

    def create_execution_plan(self, context: TaskContext) -> List[Dict]:
        """
        创建执行计划

        返回每个阶段需要执行的Agent和任务
        """
        workflow_agents = self.workflows[context.workflow_type]

        plan = []
        for i, role in enumerate(workflow_agents):
            agent = self.agents[role]
            plan.append({
                "stage": i + 1,
                "agent_role": role,
                "agent_name": agent.name,
                "goal": agent.goal,
                "tools": agent.tools,
                "dependencies": [workflow_agents[j] for j in range(i)] if i > 0 else []
            })

        return plan

    async def execute_agent(
        self,
        agent: AgentDefinition,
        context: TaskContext,
        input_data: Any = None
    ) -> AgentResult:
        """
        执行单个Agent

        这是实际调用Agent的地方
        在Claude Agent SDK中，这会通过subagents实现
        """
        start_time = datetime.now()

        try:
            # 这里是Agent执行的占位符
            # 在实际使用Claude Agent SDK时，会调用subagent
            print(f"\n{'='*60}")
            print(f"🤖 执行 Agent: {agent.name}")
            print(f"📋 目标: {agent.goal}")
            print(f"🔧 工具: {', '.join(agent.tools)}")
            print(f"{'='*60}\n")

            # 模拟Agent处理
            # 实际实现中，这里会调用Claude Agent SDK的subagent
            output = {
                "agent": agent.name,
                "role": agent.role,
                "input": input_data,
                "context": context.to_dict(),
                "status": "ready_for_execution"
            }

            execution_time = (datetime.now() - start_time).total_seconds()

            return AgentResult(
                agent_role=AgentRole(agent.role),
                success=True,
                output=output,
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return AgentResult(
                agent_role=AgentRole(agent.role),
                success=False,
                output=None,
                error=str(e),
                execution_time=execution_time
            )

    async def run_workflow(self, request: str) -> Dict:
        """
        运行完整工作流

        这是编排器的核心方法
        """
        # 1. 分析请求
        workflow_type, output_format = self.analyze_request(request)

        # 2. 创建上下文
        context = TaskContext(
            request=request,
            workflow_type=workflow_type,
            output_format=output_format
        )

        # 3. 创建执行计划
        plan = self.create_execution_plan(context)

        print(f"\n🎯 工作流类型: {workflow_type.value}")
        print(f"📄 输出格式: {output_format.value}")
        print(f"📊 执行阶段: {len(plan)} 个\n")

        # 4. 执行每个阶段
        results = []
        for stage in plan:
            context.current_stage = f"stage_{stage['stage']}"

            agent = self.agents[stage["agent_role"]]

            # 获取上一阶段的输出作为输入
            input_data = results[-1].output if results else {"request": request}

            # 执行Agent
            result = await self.execute_agent(agent, context, input_data)
            results.append(result)

            # 更新上下文
            if not result.success:
                context.errors.append(f"Stage {stage['stage']} failed: {result.error}")

            print(f"✅ Stage {stage['stage']}: {agent.name} - {'成功' if result.success else '失败'}")

        # 5. 完成上下文
        context.completed_at = datetime.now()
        context.current_stage = "completed"

        # 6. 返回结果
        return {
            "success": all(r.success for r in results),
            "workflow_type": workflow_type.value,
            "output_format": output_format.value,
            "context": context.to_dict(),
            "results": [
                {
                    "agent": r.agent_role.value,
                    "success": r.success,
                    "execution_time": r.execution_time,
                    "error": r.error
                }
                for r in results
            ],
            "total_execution_time": sum(r.execution_time for r in results),
            "execution_plan": plan
        }

    def get_agent_for_role(self, role: AgentRole) -> AgentDefinition:
        """获取指定角色的Agent定义"""
        return self.agents.get(role)

    def list_agents(self) -> List[Dict]:
        """列出所有可用的Agent"""
        return [
            {
                "role": role.value,
                "name": agent.name,
                "goal": agent.goal,
                "expertise": agent.expertise,
                "tools": agent.tools,
                "priority": agent.priority
            }
            for role, agent in self.agents.items()
        ]

    def get_workflow_info(self, workflow_type: WorkflowType) -> Dict:
        """获取工作流信息"""
        agents = self.workflows[workflow_type]
        return {
            "type": workflow_type.value,
            "stages": len(agents),
            "agents": [self.agents[role].name for role in agents],
            "estimated_time": {
                WorkflowType.QUICK_RECAP: "10-30分钟",
                WorkflowType.FULL_ANALYSIS: "1-2小时",
                WorkflowType.EXECUTIVE_REPORT: "30-60分钟",
                WorkflowType.DATA_EXPORT: "15-30分钟",
            }.get(workflow_type, "未知")
        }


# ============================================================
# Claude Agent SDK 集成示例
# ============================================================

"""
使用 Claude Agent SDK 的完整实现示例:

```python
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition, ResultMessage

async def run_ecommerce_analysis(user_request: str):
    # 定义6个专业subagent
    agents = {
        "requirement_analyst": AgentDefinition(
            description="需求分析师 - 理解和梳理业务需求",
            prompt=REQUIREMENT_ANALYST.system_prompt,
            tools=REQUIREMENT_ANALYST.tools
        ),
        "etl_engineer": AgentDefinition(
            description="ETL工程师 - 数据提取、清洗、转换",
            prompt=ETL_ENGINEER.system_prompt,
            tools=ETL_ENGINEER.tools
        ),
        "business_analyst": AgentDefinition(
            description="业务分析师 - 深入分析业务数据",
            prompt=BUSINESS_ANALYST.system_prompt,
            tools=BUSINESS_ANALYST.tools
        ),
        "visualization_engineer": AgentDefinition(
            description="可视化工程师 - 数据可视化呈现",
            prompt=VISUALIZATION_ENGINEER.system_prompt,
            tools=VISUALIZATION_ENGINEER.tools
        ),
        "report_designer": AgentDefinition(
            description="报告设计师 - 设计专业报告",
            prompt=REPORT_DESIGNER.system_prompt,
            tools=REPORT_DESIGNER.tools
        ),
        "strategy_advisor": AgentDefinition(
            description="策略顾问 - 提供策略建议",
            prompt=STRATEGY_ADVISOR.system_prompt,
            tools=STRATEGY_ADVISOR.tools
        ),
    }

    # Orchestrator system prompt
    orchestrator_prompt = '''
你是一个电商数据分析团队的协调者(Orchestrator)。

你的职责:
1. 分析用户的请求，确定需要哪些专业Agent参与
2. 按正确的顺序调用Agent
3. 在Agent之间传递上下文
4. 汇总最终结果

可用的专业Agent:
- requirement_analyst: 需求分析
- etl_engineer: 数据ETL
- business_analyst: 业务分析
- visualization_engineer: 可视化
- report_designer: 报告设计
- strategy_advisor: 策略建议

工作流选择:
- 快速回顾: requirement → etl → analyst → viz
- 完整分析: requirement → etl → analyst → viz → report → strategy
- 高管汇报: requirement → etl → analyst → strategy → report(ppt)
- 数据导出: requirement → etl → report(excel)
'''

    # 运行orchestrator
    async for message in query(
        prompt=f'''
用户请求: {user_request}

请协调团队完成这个分析任务:
1. 首先分析需求
2. 确定工作流类型
3. 按顺序调用相关专业Agent
4. 汇总输出最终结果
''',
        options=ClaudeAgentOptions(
            allowed_tools=["Agent"],  # 允许调用subagents
            agents=agents,
            system_prompt=orchestrator_prompt
        )
    ):
        if isinstance(message, ResultMessage):
            print(message.result)

# 使用
anyio.run(run_ecommerce_analysis, "分析最近30天的GMV趋势，给出增长建议")
```
"""


# ============================================================
# 命令行入口
# ============================================================

def main():
    """命令行入口"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m orchestration.orchestrator <request>")
        print("Example: python -m orchestration.orchestrator '分析最近30天GMV趋势'")
        sys.exit(1)

    request = " ".join(sys.argv[1:])

    orchestrator = EcommerceDataOrchestrator()

    # 同步运行异步方法
    result = asyncio.run(orchestrator.run_workflow(request))

    print("\n" + "="*60)
    print("📊 执行结果")
    print("="*60)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Ecommerce Data Agent - 使用示例

演示如何使用程序化编排系统
"""

import asyncio
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestration import EcommerceDataOrchestrator
from orchestration.agents import (
    AgentRole,
    get_agent,
    get_all_agents,
    REQUIREMENT_ANALYST,
    ETL_ENGINEER,
    BUSINESS_ANALYST
)


async def demo_orchestrator():
    """演示编排器的基本使用"""

    print("=" * 60)
    print("🚀 电商数据分析编排器演示")
    print("=" * 60)

    # 创建编排器
    orchestrator = EcommerceDataOrchestrator()

    # 示例请求列表
    requests = [
        "分析最近30天的GMV趋势",
        "快速回顾昨天的销售数据",
        "给老板做Q3季度汇报PPT",
        "导出上个月的订单明细到Excel"
    ]

    for request in requests:
        print(f"\n📝 请求: {request}")

        # 分析请求
        workflow_type, output_format = orchestrator.analyze_request(request)
        print(f"   工作流类型: {workflow_type.value}")
        print(f"   输出格式: {output_format.value}")

        # 获取工作流信息
        workflow_info = orchestrator.get_workflow_info(workflow_type)
        print(f"   预计时间: {workflow_info['estimated_time']}")
        print(f"   涉及Agent: {', '.join(workflow_info['agents'])}")


async def demo_agent_info():
    """演示如何获取Agent信息"""

    print("\n" + "=" * 60)
    print("🤖 Agent 信息")
    print("=" * 60)

    orchestrator = EcommerceDataOrchestrator()
    agents = orchestrator.list_agents()

    for agent in agents:
        print(f"\n📋 {agent['name']}")
        print(f"   角色: {agent['role']}")
        print(f"   目标: {agent['goal']}")
        print(f"   工具: {', '.join(agent['tools'])}")


async def demo_full_workflow():
    """演示完整工作流执行"""

    print("\n" + "=" * 60)
    print("🔄 完整工作流执行演示")
    print("=" * 60)

    orchestrator = EcommerceDataOrchestrator()

    request = "分析最近7天的GMV趋势，找出增长点"

    print(f"\n📝 请求: {request}")
    print("\n开始执行工作流...\n")

    result = await orchestrator.run_workflow(request)

    print("\n" + "=" * 60)
    print("📊 执行结果")
    print("=" * 60)
    print(f"成功: {result['success']}")
    print(f"工作流类型: {result['workflow_type']}")
    print(f"输出格式: {result['output_format']}")
    print(f"总执行时间: {result['total_execution_time']:.2f}s")

    print("\n执行阶段:")
    for r in result['results']:
        status = "✅" if r['success'] else "❌"
        print(f"  {status} {r['agent']} - {r['execution_time']:.2f}s")


def print_usage():
    """打印使用说明"""
    print("""
使用方式:

1. 直接运行演示:
   python example_usage.py

2. 作为模块导入:
   from orchestration import EcommerceDataOrchestrator

   orchestrator = EcommerceDataOrchestrator()
   result = await orchestrator.run_workflow("你的分析请求")

3. 查看特定Agent:
   from orchestration.agents import get_agent, AgentRole

   agent = get_agent(AgentRole.BUSINESS_ANALYST)
   print(agent.system_prompt)

4. 命令行使用:
   python -m orchestration.orchestrator "分析最近30天GMV趋势"
""")


async def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_usage()
        return

    # 运行演示
    await demo_orchestrator()
    await demo_agent_info()

    # 如果需要完整工作流演示，取消下面的注释
    # await demo_full_workflow()


if __name__ == "__main__":
    asyncio.run(main())

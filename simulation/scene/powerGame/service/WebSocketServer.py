import copy
import json
import math
import time
import uuid
from pprint import pprint
import websockets
import asyncio
import os
import glob

from simulation.models.agents.RA.RAAgent import RequirementAnalysisAgent
from simulation.models.agents.RA.RAObserver import RequirementAnalysisObserver

connected = set()


MODEL_LIST = ['deepseek-r1:32b', 'deepseek-r1:32b-qwen-distill-q8_0', 'gpt-4o']
REQUIREMENT_LIST = [
    '我想要复现古巴导弹危机中美国和古巴在各个时间段的行为，分析什么因素对战争的走势影响最大',
    '我想要分析一个由业务员组成的数字政务系统中，对业务员工作效率影响的最大因素。在此系统中，业务员需要不断处理来自客户的订单，每一份订单的难度有不同的水平，员工的薪资可能也不相同',
    '我想探究在古巴导弹危机中，若美国一直采用强硬的态度，最终战争的走向'
]


# 数据发送到前端
async def send_data(websocket, data, agent_state, info):
    res = {
        'type': 'success',
        'data': data,
        'agent_state': agent_state,
        'info': info
    }
    await asyncio.sleep(2)
    await websocket.send(json.dumps(res))


# 需求解析
async def req_analysis(websocket):
    # 使用的模型
    MODEL_NAME = MODEL_LIST[1]
    # 当前需求
    req = REQUIREMENT_LIST[2]
    # 需求解析后的参数字典
    exp_param = {
        'goal': None,
        'influence_factor': None,
        'response_var': None,
        'formula': None,
        'exp_params': None
    }
    # 各agent状态
    # index：{ 0: 需求解析 1: 需求格式检查 2: 变量检查 3: 实验方案检查 4: Agent设计}
    # value：{ 0: 等待中 1: 正在工作 2: 工作完成且通过 3: 不通过 }
    agent_state = [0] * 5

    # 需求分析
    raAgent = RequirementAnalysisAgent(llm_model=MODEL_NAME)
    raObserver = RequirementAnalysisObserver(llm_model=MODEL_NAME)
    analysis_num = 0
    while True:
        agent_state[0] = 1
        await send_data(websocket, None, agent_state, None)
        ra_res = raAgent.requirement_analysis(req)
        agent_state[0] = 2
        await send_data(websocket, ra_res, agent_state, None)
        print(ra_res)
        # log_with_tag(message=json.dumps(ra_res), tag='RA Result', level='info')
        # 检查需求分析结果格式是否正确
        agent_state[1] = 1
        await send_data(websocket, None, agent_state, '需求解析结果格式检查中')
        is_analysis_format_true = raObserver.requirement_format_judge(ra_res)
        if is_analysis_format_true:
            agent_state[1] = 2
            await send_data(websocket, ra_res, agent_state, '需求解析完成')
            # log_with_tag(message='需求解析成功', tag='RA Success', level='warning')
            print(f'\033[31m------需求解析成功------\033[0m')
            exp_param['goal'] = ra_res['goal']
            exp_param['influence_factor'] = ra_res['influence_factor']
            exp_param['response_var'] = ra_res['response_var']
            exp_param['formula'] = ra_res['formula']
            exp_param['exp_params'] = ra_res['exp_params']
            break
        else:
            agent_state[1] = 3
            await send_data(websocket, ra_res, agent_state, '需求解析格式错误')
            # log_with_tag(message='需求解析失败', tag='RA Fail', level='error')
            print(f'\033[31m------需求解析错误({++analysis_num})------\033[0m')
            agent_state[1] = 0


async def handle_message(websocket, message):
    print(message)
    if message == "begin":
        print('Game Start')
        connected.add(websocket)
        await asyncio.create_task(req_analysis(websocket))
    else:
        print('else')
        await websocket.send("get message: " + message + '但并非系统制定指令')


async def server(websocket):
    try:
        async for message in websocket:
            await handle_message(websocket, message)
    finally:
        connected.remove(websocket)


async def main():
    print("WebSocket服务器启动成功，端口号为8765")
    async with websockets.serve(server, "localhost", 8765):
        await asyncio.Future()  # 保持运行


if __name__ == "__main__":
    asyncio.run(main())
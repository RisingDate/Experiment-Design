import copy
import json
import math
import time
import uuid
from datetime import datetime
from pprint import pprint
import websockets
import asyncio
import os
import glob

from simulation.models.agents.AD.ADAgent import AgentDesignAgent
from simulation.models.agents.ED.VCAgent import VariableControlAgent
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
        'exp_params': None,
        'agent_design_res': None
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
        await send_data(websocket, None, agent_state,
                        {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 0, 'data': '我正在解析用户需求'})
        ra_res = raAgent.requirement_analysis(req)
        agent_state[0] = 2
        await send_data(websocket, ra_res, agent_state,
                        {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 0, 'data': '用户需求解析完成'})
        print(ra_res)
        # 检查需求分析结果格式是否正确
        agent_state[1] = 1
        await send_data(websocket, None, agent_state,
                        {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 1, 'data': '我正在检查生成的需求格式是否正确'})
        is_analysis_format_true = raObserver.requirement_format_judge(ra_res)
        if is_analysis_format_true:
            agent_state[1] = 2
            await send_data(websocket, ra_res, agent_state,
                            {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 1, 'data': '我认为格式是正确的'})
            print(f'\033[31m------需求解析成功------\033[0m')
            exp_param['goal'] = ra_res['goal']
            exp_param['influence_factor'] = ra_res['influence_factor']
            exp_param['response_var'] = ra_res['response_var']
            exp_param['formula'] = ra_res['formula']
            exp_param['exp_params'] = ra_res['exp_params']
            break
        else:
            agent_state[1] = 3
            await send_data(websocket, ra_res, agent_state,
                            {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 1, 'data': '解析结果的格式是错误的，接下来将由RAAgent重新解析需求'})
            await asyncio.sleep(3)
            print(f'\033[31m------需求解析错误({analysis_num})------\033[0m')
            analysis_num += 1
            agent_state[1] = 0
            await asyncio.sleep(3)

    # 影响因素和响应变量内容检查
    vcAgent = VariableControlAgent(llm_model=MODEL_NAME)
    agent_state[2] = 1
    await send_data(websocket, exp_param, agent_state,
                    {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 2, 'data': '我正在检查生成的变量是否合理'})
    vc_res = vcAgent.VCAnalysis(req=req,
                                influence_factor=ra_res['influence_factor'],
                                response_var=ra_res['response_var'],
                                formula=ra_res['formula'])
    print('VC Response: ', vc_res)
    if vc_res['is_reasonable'] == 1:
        agent_state[2] = 2
        await send_data(websocket, exp_param, agent_state,
                        {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 2, 'data': '我认为生成的变量是合理的'})
        print('\033[31m------变量生成正确------\033[0m')
    else:
        # -------变量解析结果不合理------------
        agent_state[2] = 3
        await send_data(websocket, exp_param, agent_state,
                        {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 2, 'data': '我认为生成的变量不合理，理由为：' + vc_res['reason']})
        await asyncio.sleep(3)

        agent_state[2] = 1
        await send_data(websocket, exp_param, agent_state,
                        {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 2, 'data': '我正在重新思考变量内容'})
        await asyncio.sleep(3)

        print('\033[31m------变量生成不合理------\033[0m')
        exp_param['influence_factor'] = vc_res['influence_factor']
        exp_param['response_var'] = vc_res['response_var']
        exp_param['formula'] = vc_res['formula']
        agent_state[2] = 2
        await send_data(websocket, exp_param, agent_state,
                        {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 2, 'data': '我已重新生成变量'})

    # 实验方案检查
    agent_state[3] = 1
    await send_data(websocket, exp_param, agent_state,
                    {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 3, 'data': '开始检查生成的实验方案是否合理'})

    vc_exp_param_res = vcAgent.VCExpParamAnalysis(req=req,
                                                  influence_factor=exp_param['influence_factor'],
                                                  response_var=exp_param['response_var'],
                                                  formula=exp_param['formula'],
                                                  exp_params=exp_param['exp_params'])
    if vc_exp_param_res['is_reasonable'] == 1:
        agent_state[3] = 2
        await send_data(websocket, exp_param, agent_state,
                        {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 3, 'data': '我认为实验方案是合理的'})
        print('\033[31m------实验参数设置合理------\033[0m')
    else:
        agent_state[3] = 3
        await send_data(websocket, exp_param, agent_state,
                        {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 3, 'data': '我认为实验方案不合理，理由如下：' + vc_exp_param_res['reason']})
        await asyncio.sleep(3)

        agent_state[3] = 1
        await send_data(websocket, exp_param, agent_state,
                        {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 3, 'data': '我开始重新思考实验方案'})
        await asyncio.sleep(3)

        print('\033[31m------实验参数设置不合理------\033[0m')
        exp_param['exp_params'] = vc_exp_param_res['exp_params']
        agent_state[3] = 2
        await send_data(websocket, exp_param, agent_state,
                        {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 3, 'data': '已重新生成实验方案'})

    # 智能体设计
    adAgent = AgentDesignAgent(llm_model=MODEL_NAME)
    agent_design_format_flag = False
    while not agent_design_format_flag:
        agent_state[4] = 1
        await send_data(websocket, exp_param, agent_state,
                        {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 4, 'data': '我正在设计实验需要的Agent'})
        agent_design_res = adAgent.agent_design(req, exp_param)

        exp_param['agent_design_res'] = agent_design_res
        agent_state[4] = 0
        await send_data(websocket, exp_param, agent_state,
                        {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 4, 'data': 'Agent设计完成，等待检测...'})
        await asyncio.sleep(3)
        print('智能体设计结果: ', agent_design_res)

        agent_design_format_flag, ad_format_check_info = adAgent.format_check(agent_design_res)
        if not agent_design_format_flag:
            print('\033[31m------智能体设计方案不合理------\033[0m')
            print('错误原因为： ', ad_format_check_info)
            agent_state[4] = 3
            await send_data(websocket, exp_param, agent_state,
                            {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 4, 'data': 'Agent设计存在问题：' + ad_format_check_info})
            await asyncio.sleep(3)

        else:
            print('\033[32m------智能体设计方案合理------\033[0m')
            agent_state[4] = 2
            await send_data(websocket, exp_param, agent_state,
                            {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent_index': 4, 'data': 'Agent设计完成内容通过检测'})


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
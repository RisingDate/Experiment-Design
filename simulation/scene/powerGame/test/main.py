from simulation.models.agents.RA.RAAgent import RequirementAnalysisAgent
from simulation.models.agents.RA.RAObserver import RequirementAnalysisObserver
from simulation.models.agents.ED.VCAgent import VariableControlAgent
from simulation.models.agents.AD.ADAgent import AgentDesignAgent
import logging
import json
from typing import Literal

MODEL_LIST = ['deepseek-r1:32b', '', 'deepseek-r1:32b-qwen-distill-q8_0', 'gpt-4o']
REQUIREMENT_LIST = [
    '我想要复现古巴导弹危机中美国和古巴在各个时间段的行为，分析什么因素对战争的走势影响最大',
    '我想要分析一个由业务员组成的数字政务系统中，对业务员工作效率影响的最大因素。在此系统中，业务员需要不断处理来自客户的订单，每一份订单的难度有不同的水平，员工的薪资可能也不相同',
    '我想探究在古巴导弹危机中，若美国一直采用强硬的态度，最终战争的走向'
]


# 定义日志模块
class TagFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, 'tag'):
            record.tag = 'GENERAL'  # 设置默认tag
        return f"[{record.tag}] {super().format(record)}"


logger = logging.getLogger("myLogger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("../log/running_log.log", encoding='utf-8')
formatter = TagFormatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


# 日志保存简易函数
def log_with_tag(message, tag='GENERAL', level: Literal['debug', 'info', 'warning', 'error', 'critical'] = 'info'):
    if level == 'info':
        logger.info(message, extra={'tag': tag})
    elif level == 'warning':
        logger.warning(message, extra={'tag': tag})
    elif level == 'error':
        logger.error(message, extra={'tag': tag})
    elif level == 'debug':
        logger.debug(message, extra={'tag': tag})
    elif level == 'critical':
        logger.critical(message, extra={'tag': tag})


if __name__ == '__main__':
    # 显示开始一次新的实验
    log_with_tag(message=' ', tag='---New Exp---', level='critical')
    exp_param = {
        'goal': None,
        'influence_factor': None,
        'response_var': None,
        'formula': None,
        'exp_params': None,
        'var_explain': None,
    }
    agent_design_res = {
        'attribute': [],
        'attribute_explain': [],
        'relationship_net': []
    }

    # 需求分析
    req = REQUIREMENT_LIST[0]

    raAgent = RequirementAnalysisAgent(llm_model=MODEL_LIST[2])
    raObserver = RequirementAnalysisObserver(llm_model=MODEL_LIST[2])
    analysis_num = 0
    while True:
        ra_res = raAgent.requirement_analysis(req)
        print(ra_res)
        log_with_tag(message=json.dumps(ra_res), tag='RA Result', level='info')
        # 检查需求分析结果格式是否正确
        is_analysis_format_true = raObserver.requirement_format_judge(ra_res)
        if is_analysis_format_true:
            log_with_tag(message='需求解析成功', tag='RA Success', level='warning')
            print(f'\033[31m------需求解析成功------\033[0m')
            exp_param['goal'] = ra_res['goal']
            exp_param['influence_factor'] = ra_res['influence_factor']
            exp_param['response_var'] = ra_res['response_var']
            exp_param['formula'] = ra_res['formula']
            exp_param['exp_params'] = ra_res['exp_params']
            break
        else:
            log_with_tag(message='需求解析失败', tag='RA Fail', level='error')
            print(f'\033[31m------需求解析错误({analysis_num})------\033[0m')
            analysis_num += 1

    # 影响因素和响应变量内容检查
    vcAgent = VariableControlAgent(llm_model=MODEL_LIST[2])
    vc_res = vcAgent.VCAnalysis(req=req,
                                influence_factor=ra_res['influence_factor'],
                                response_var=ra_res['response_var'],
                                formula=ra_res['formula'])
    print('VC Response: ', vc_res)
    if vc_res['is_reasonable'] == 1:
        print('\033[31m------变量生成正确------\033[0m')
        log_with_tag(message='变量生成正确', tag='VC Success', level='warning')
    else:
        print('\033[31m------变量生成不合理------\033[0m')
        log_with_tag(message='变量生成不合理，新变量如下', tag='VC Error', level='warning')
        exp_param['influence_factor'] = vc_res['influence_factor']
        exp_param['response_var'] = vc_res['response_var']
        exp_param['formula'] = vc_res['formula']
    exp_param['var_explain'] = vc_res['var_explain']
    log_with_tag(message=json.dumps(vc_res), tag='VC Result', level='info')

    # 实验参数检查
    vc_exp_param_res = vcAgent.VCExpParamAnalysis(req=req,
                                                  influence_factor=exp_param['influence_factor'],
                                                  response_var=exp_param['response_var'],
                                                  formula=exp_param['formula'],
                                                  exp_params=exp_param['exp_params'])
    if vc_exp_param_res['is_reasonable'] == 1:
        print('\033[31m------实验参数设置合理------\033[0m')
        log_with_tag(message='实验参数设置合理', tag='VC-Exp Param Right', level='warning')
        log_with_tag(message=vc_exp_param_res['reason'], tag='VC-Exp Param Right Reason', level='info')
    else:
        print('\033[31m------实验参数设置不合理------\033[0m')
        log_with_tag(message='实验参数设置不合理', tag='VC-Exp Param Error', level='warning')
        log_with_tag(message=vc_exp_param_res['reason'], tag='VC-Exp Param Error Reason', level='info')
        log_with_tag(message=json.dumps(vc_exp_param_res['exp_params']), tag='New Exp Params', level='info')
        exp_param['exp_params'] = vc_exp_param_res['exp_params']

    print(vc_exp_param_res)

    # 智能体设计
    adAgent = AgentDesignAgent(llm_model=MODEL_LIST[2])
    agent_design_format_flag = False
    while not agent_design_format_flag:
        agent_design_res = adAgent.agent_design(req, exp_param)
        log_with_tag(message=agent_design_res, tag='AD Result', level='info')
        print('智能体设计结果: ', agent_design_res)

        agent_design_format_flag, ad_format_check_info = adAgent.format_check(agent_design_res)
        if not agent_design_format_flag:
            print('\033[31m------智能体设计方案不合理------\033[0m')
            print('错误原因为： ', ad_format_check_info)
            log_with_tag(message=ad_format_check_info, tag='AD Error', level='error')
        else:
            print('\033[32m------智能体设计方案合理------\033[0m')
            log_with_tag(message='智能体设计方案格式正确', tag='AD Accept', level='info')
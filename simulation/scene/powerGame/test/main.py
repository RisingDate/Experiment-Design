from simulation.models.agents.RA.RAAgent import RequirementAnalysisAgent
from simulation.models.agents.RA.RAObserver import RequirementAnalysisObserver
from simulation.models.agents.ED.VCAgent import VariableControlAgent
import logging
import json
from typing import Literal


MODEL_LIST = ['deepseek-r1:32b', 'deepseek-r1:32b-qwen-distill-q8_0', 'gpt-4o']


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
    log_with_tag(message=' ', tag='New Exp', level='critical')
    exp_param = {
        'goal': None,
        'influence_factor': None,
        'response_var': None,
        'formula': None,
        'exp_params': None
    }

    # 需求分析
    req = '我想要复现古巴导弹危机中美国和古巴在各个时间段的行为，分析什么因素对战争的走势影响最大'

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
            print(f'------需求解析成功------')
            exp_param['goal'] = ra_res['goal']
            exp_param['influence_factor'] = ra_res['influence_factor']
            exp_param['response_var'] = ra_res['response_var']
            exp_param['formula'] = ra_res['formula']
            exp_param['exp_params'] = ra_res['exp_params']
            break
        else:
            log_with_tag(message='需求解析失败', tag='RA Fail', level='error')
            print(f'------需求解析错误({++analysis_num})------')

    # 影响因素和响应变量内容检查
    vcAgent = VariableControlAgent(llm_model=MODEL_LIST[2])
    vc_res = vcAgent.VCAnalysis(req=req,
                                influence_factor=ra_res['influence_factor'],
                                response_var=ra_res['response_var'],
                                formula=ra_res['formula'])
    print('VC Response: ', vc_res)
    if vc_res['is_reasonable'] == 1:
        log_with_tag(message='变量生成正确', tag='VC Success', level='warning')
    else:
        log_with_tag(message='变量生成错误，新变量如下', tag='VC Error', level='warning')
        exp_param['influence_factor'] = vc_res['influence_factor']
        exp_param['response_var'] = vc_res['response_var']
        exp_param['formula'] = vc_res['formula']
    log_with_tag(message=json.dumps(vc_res), tag='VC Result', level='info')

    # 实验参数检查
    if vc_res['is_reasonable'] == 0:
        vcAgent.VCExpParamAnalysis(req=req,
                                   influence_factor=exp_param['influence_factor'],
                                   response_var=exp_param['response_var'],
                                   formula=exp_param['formula'],
                                   exp_params=exp_param['exp_params'])


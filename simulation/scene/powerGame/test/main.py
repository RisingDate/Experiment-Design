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
    log_with_tag(message=' ', tag='New Exp', level='critical')
    raAgent = RequirementAnalysisAgent(llm_model=MODEL_LIST[2])
    raObserver = RequirementAnalysisObserver(llm_model=MODEL_LIST[2])
    req = '我想要复现古巴导弹危机中美国和古巴在各个时间段的行为，分析什么因素对战争的走势影响最大'
    analysis_num = 1
    while True:
        analysis_res = raAgent.requirement_analysis(req)
        print(analysis_res)
        log_with_tag(message=json.dumps(analysis_res), tag='RA Result', level='info')
        is_analysis_format_true = raObserver.requirement_format_judge(analysis_res)
        if is_analysis_format_true:
            log_with_tag(message='需求解析成功', tag='RA Success', level='warning')
            print(f'------需求解析成功------')
            break
        else:
            log_with_tag(message='需求解析失败', tag='RA Fail', level='error')
            print(f'------需求解析错误({analysis_num})------')

    vcAgent = VariableControlAgent(llm_model=MODEL_LIST[2])
    vc_res = vcAgent.VCAnalysis(req=req,
                                influence_factor=analysis_res['influence_factor'],
                                response_var=analysis_res['response_var'],
                                formula=analysis_res['formula'])
    print('VC Response: ', vc_res)
    if vc_res['is_reasonable'] == 1:
        log_with_tag(message='变量生成正确', tag='VC Success', level='warning')
    else:
        log_with_tag(message='变量生成错误，新变量如下', tag='VC Error', level='warning')

    log_with_tag(message=json.dumps(vc_res), tag='VC Result', level='info')

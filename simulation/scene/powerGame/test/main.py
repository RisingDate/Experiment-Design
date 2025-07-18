from simulation.models.agents.RA.RAAgent import RequirementAnalysisAgent
from simulation.models.agents.RA.RAObserver import RequirementAnalysisObserver
from simulation.models.agents.ED.VCAgent import VariableControlAgent

MODEL_LIST = ['deepseek-r1:32b', 'deepseek-r1:32b-qwen-distill-q8_0', 'gpt-4o']

if __name__ == '__main__':
    raAgent = RequirementAnalysisAgent(llm_model=MODEL_LIST[2])
    raObserver = RequirementAnalysisObserver(llm_model=MODEL_LIST[2])
    req = '我想要复现古巴导弹危机中美国和古巴在各个时间段的行为，分析什么因素对战争的走势影响最大'
    analysis_num = 1
    while True:
        analysis_res = raAgent.requirement_analysis(req)
        print(analysis_res)
        is_analysis_format_true = raObserver.requirement_format_judge(analysis_res)
        if is_analysis_format_true:
            print(f'------需求解析成功------')
            break
        print(f'------需求解析错误({analysis_num})------')

    vcAgent = VariableControlAgent(llm_model=MODEL_LIST[2])
    vc_res = vcAgent.VCAnalysis(req=req,
                                influence_factor=analysis_res['influence_factor'],
                                response_var=analysis_res['response_var'],
                                formula=analysis_res['formula'])
    print('VC Response: ', vc_res)

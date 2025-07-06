from simulation.models.agents.RA.RAAgent import RequirementAnalysisAgent
from simulation.models.agents.RA.RAObserver import RequirementAnalysisObserver

if __name__ == '__main__':
    ra = RequirementAnalysisAgent()
    raObserver = RequirementAnalysisObserver()
    req = '我想要复现古巴导弹危机中美国和古巴在各个时间段的行为，分析什么因素对战争的走势影响最大'
    analysis_num = 1
    while True:
        analysis_res = ra.requirement_analysis(req)
        print(analysis_res)
        is_analysis_format_true = raObserver.requirement_format_judge(analysis_res)
        if is_analysis_format_true:
            print(f'------需求解析完成------')
            break
        print(f'------需求解析错误({analysis_num})------')
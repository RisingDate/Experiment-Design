
from simulation.models.agents.RA.RAAgent import RequirementAnalysisAgent

if __name__ == '__main__':
    ra = RequirementAnalysisAgent()
    req = '我想要复现古巴导弹危机中美国和古巴在各个时间段的行为，分析什么因素对战争的走势影响最大'
    res = ra.requirement_analysis(req)
    print(res)

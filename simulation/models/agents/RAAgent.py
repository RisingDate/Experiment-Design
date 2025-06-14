from simulation.models.agents.LLMAgent import LLMAgent


class RequirementAnalysisAgent(LLMAgent):
    def __init__(self, agent_name='RAAgent'):
        super().__init__(agent_name=agent_name, has_chat_history=False, online_track=False, json_format=True,
                         system_prompt='',
                         llm_model='deepseek-r1:32b')
        self.system_prompt = '''
        你正在对复杂社会模型系统推演中需求进行分析。你需要扮演一个资深的需求处理工程师的角色，你可以参考自身的经验，但请务必以模拟过程中的内容为主。
        '''
        self.is_first = True


    def requirement_analysis(self, info):
        return
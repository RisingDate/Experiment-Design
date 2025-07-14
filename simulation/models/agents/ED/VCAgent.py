from simulation.models.agents.LLMAgent import LLMAgent

MODEL_LIST = {
    'think': ['deepseek-r1:32b', 'deepseek-r1:32b-qwen-distill-q8_0'],
    'nothink': ['gpt-4o']
}


class VariableControlAgent(LLMAgent):
    def __init__(self, agent_name='VCAgent', llm_model='deepseek-r1:32b-qwen-distill-q8_0'):
        super().__init__(agent_name=agent_name, has_chat_history=False, online_track=False, json_format=True,
                         system_prompt='',
                         llm_model=llm_model)
        self.system_prompt = '''
            你是一名资深的社会政治家，善于用社会学的方法分析国家之间的关系。现在我们正在对用户的某一需求进行分析。
            通过一定的方法，我们获得了能够反映此需求的'响应变量'和能够影响这些'响应变量'的'影响因素'。
            我们简单的对'影响因素'和'响应变量'之间以数学公式的形式建立了一些对应关系。
            你的任务是分析这些'响应变量'和'影响因素'能否正确反映用户的需求以及它们二者之间的对应关系是否合理。
            不论是否合理，请给出你的理由，如果不合理，请重新设计'影响因素'和'响应变量'以及他们之间的对应关系。
        '''
        self.is_first = True
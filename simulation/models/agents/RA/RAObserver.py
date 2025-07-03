from simulation.models.agents.LLMAgent import LLMAgent


class RequirementAnalysisObserver(LLMAgent):
    def __init__(self, agent_name='RAAgent', requirement='',
                 re_analysis_res=None, llm_model='deepseek-r1:32b-qwen-distill-q8_0'):
        super().__init__(agent_name=agent_name,
                         has_chat_history=False,
                         online_track=False,
                         json_format=False,
                         system_prompt='',
                         llm_model=llm_model)
        if re_analysis_res is None:
            re_analysis_res = {}
        print('this is RAObserver')
        self.requirement = requirement
        self.re_analysis_res = re_analysis_res
        self.system_prompt = '''
            我定义了一个用于需求分析的Agent，他会将我输入的需求：{requirement}解析为一个格式化的json数据。
            你是这个Agent观测者，任务为观测他生成的json数据是否是预期的格式，如果是返回True，否则返回False。
            json数据的格式为：{
                
            }
            需求分析Agent解析的结果为：{}
            
        '''
        self.is_first = True
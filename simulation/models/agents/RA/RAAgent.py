from simulation.models.agents.LLMAgent import LLMAgent

MODEL_LIST = {
    'think': ['deepseek-r1:32b', 'deepseek-r1:32b-qwen-distill-q8_0'],
    'nothink': ['gpt-4o']
}


class RequirementAnalysisAgent(LLMAgent):
    def __init__(self, agent_name='RAAgent'):
        super().__init__(agent_name=agent_name, has_chat_history=False, online_track=False, json_format=True,
                         system_prompt='',
                         # llm_model='gpt-4o')
                         llm_model='deepseek-r1:32b-qwen-distill-q8_0')
        self.system_prompt = '''
            你正在对复杂社会模型系统推演中的需求进行分析。你需要扮演一个资深的需求处理工程师的角色，你可以参考自身的经验，但请务必以模拟过程中的内容为主。
            在处理过程中你可能会遇到与实验方法有关的一些内容，这些实验方法指的都是计算实验方法，下面是对计算实验方法的一些粗略的介绍和举例，
            请你在选择实验方法时尽可能的参考下面的内容：
                计算实验方法可以分为确定性实验设计和非确定性实验设计，
                确定性实验设计包括：'一次一因子设计'，'NK因子设计'，'网格设计'，'超饱和设计'，'均匀设计'，'正交设计'，'拉丁方设计'，
                '分布因子设计'，'顺序分支设计'，'迭代分布析因设计'，'多步组筛选设计' 和 '托辛筛选设计'；
                非确定性实验设计包括：'Monte Carlo'，'Markov-Chain Monte Carlo' 和 '重采样'三类方法
        '''
        self.is_first = True

    # 需求分析
    def requirement_analysis(self, req):
        info_prompt = '''
            你需要根据当前提出的实验需求和对需求的目的、影响需求的因素，需求的响应变量和实验分析的方法进行筛选和判断。
            用户提出的需求为：
                {req}
            - 当你回复时，你必须采取下面的json格式，除去goal使用中文回答外，其余请全部使用英文回答，英文变量无需给出中文的解释
                "goal": 用户此次实验或假设的目的，'goal'的类型请尽量从'现象解释'，'趋势预测'，'策略优化'中进行选择，并对其进行简单的解释\
                    'goal'是一个json，包含'category'和'explain'，'category'和'explain'请使用中文回答。
                "influence_factor": 影响因素，即实验的自变量，能够尽可能全面的反应对实验的影响，'influence_factor'应该为一个list。\
                    'influence_factor'的内容全部为英文。
                "response_var": 响应变量，即实验的因变量，能够客观的反映实验的结果，'response_var'应该为一个list，\
                    'response_var'的内容全部为英文。
                "formula": 影响因素和响应变量之间的对应公式，每个响应变量都有一个确定的对应公式，公式以数学公式的形式给出，\
                    'formula'的格式为json，每个元素的key为响应变量的名称，value为影响因素组成的一个公式，'formula'的长度与'response_var'相同\
                    'formula'的内容全部为英文
                "exp_params": 实验参数的格式为json，包含'exp_method'和'params'，\
                    'exp_method'是实验方法，具体参考上面提到的实验设计方法，'exp_method'是一个字符串，\
                    'params'是根据'exp_method'生成的实验参数，你需要根据实验方法生成多组实验，每组实验是影响因素的不同取值水平组合，请设置合理的实验组数。\
                    'param'是一个json，而不是一个list，'param'中key的数量与影响因素相等，每个元素的key为影响因素的名称，value为影响因素的取值，所有影响因素的取值数量应该相同。\
                    'exp_params'的内容全部为英文。
        '''
        param_dict = {
            'req': req,
        }
        if self.llm_model in MODEL_LIST['think']:
            llm_response, think = self.get_response(info_prompt, input_param_dict=param_dict,
                                                    is_first_call=self.is_first)
        else:
            llm_response = self.get_response(info_prompt, input_param_dict=param_dict,
                                             is_first_call=self.is_first)
        self.is_first = False
        res = {
            "goal": {},
            "influence_factor": [],
            "response_var": [],
            "formula": [],
            "exp_params": [],
        }
        try:
            res = {
                "goal": llm_response['goal'],
                "influence_factor": llm_response['influence_factor'],
                "response_var": llm_response['response_var'],
                "formula": llm_response['formula'],
                "exp_params": llm_response['exp_params']
            }
        except Exception as e:
            print(e)

        return res

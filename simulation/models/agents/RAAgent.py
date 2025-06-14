from simulation.models.agents.LLMAgent import LLMAgent


class RequirementAnalysisAgent(LLMAgent):
    def __init__(self, agent_name='RAAgent'):
        super().__init__(agent_name=agent_name, has_chat_history=False, online_track=False, json_format=True,
                         system_prompt='',
                         llm_model='deepseek-r1:32b')
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
            - 当你回复时，你必须采取下面的json格式，请全部使用英文回答
                   "goal": 用户此次实验或假设的目的，goal的类型请尽量从'现象解释'，'趋势预测'，'策略优化'中进行选择，并对其进行简单的解释\
                   'goal'是一个json，包含category和explain。
                   "influence_factor": 影响因素，即实验的自变量，能够尽可能全面的反应，'influence_factor'应该为一个list。
                   "response_var": 响应变量，即实验的因变量，能够客观的反映实验的结果，'response_var'应该为一个list。
                   "formula": 影响因素和响应变量之间的对应公式，每个响应变量都有一个确定的对应公式，公式以数学公式的形式给出，\
                   'formula'是一个数组，数组中每个元素都是一个字典，字典的key为响应变量的名称，value为影响因素组成的一个公式，key和value都需要以英文的形式给出
                   "exp_params": 实验参数的格式为json，包含'exp_method'和'params'，'exp_method'是实验方法，具体参考上面提到的实验设计方法，\
                   'params'是根据'exp_method'生成的实验参数，你需要根据实验方法生成多组实验，每组实验是影响因素的不同取值水平组合，请设置合理的实验组数。\
                   'exp_method'是一个字符串，'param'是一个数组，数组中的每个元素都是一个字典，字典的key为影响因素的名称，value为影响因素的取值。
        '''
        param_dict = {
            'req': req,
        }
        llm_response, think = self.get_response(info_prompt, input_param_dict=param_dict,
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

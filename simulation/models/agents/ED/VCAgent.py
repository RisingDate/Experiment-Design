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
            你是一名资深的社会政治学家，善于用社会学的方法分析国家之间的关系。现在我们正在对用户的某一需求进行分析。
            通过一定的方法，我们获得了能够反映此需求的'响应变量'和能够影响这些'响应变量'的'影响因素'。
            我们简单的对'影响因素'和'响应变量'之间以数学公式的形式建立了一些对应关系。
            你的任务是分析这些'响应变量'和'影响因素'能否正确反映用户的需求以及它们二者之间的对应关系是否合理。
            不论是否合理，请给出你的理由，如果不合理，请重新设计'影响因素'和'响应变量'以及他们之间的对应关系。
        '''
        self.is_first = True

    def VCAnalysis(self, req, influence_factor, response_var, ):
        info_prompt = '''
            在本次需求分析中，用户提出的需求为：{req}
            影响因素为：{influence_factor}
            响应变量为：{response_var}
            影响因素和响应变量之间的对应关系为：{}
            - 你回复的格式均为json，但是包含两种情况：
            - 第一种：如果你认为前面解析的'影响因素'和'响应变量'以及二者之间的对应关系均合理，回复格式为：
                "is_reasonable": 1。
                "var_explain": 对变量的中文解释，包含影响因素和响应变量，'var_explain'的格式为json，包含'influence_factor'和'response_var'两个key，\
                    分别是对'影响因素'和'响应变量'的中文解释，'influence_factor'和'response_var'的内容均为list，\
                    list的内容为dict，dict举例如下："'foreign_policy': '外交政策'"。
            - 第二种：如果你认为前面解析的不合理，回复格式如下：
                "is_reasonable": 0。
                "influence_factor": 影响因素，即实验的自变量，能够尽可能全面的反应对实验的影响，'influence_factor'应该为一个list。\
                    'influence_factor'的内容全部为英文。
                "response_var": 响应变量，即实验的因变量，能够客观的反映实验的结果，'response_var'应该为一个list，\
                    'response_var'的内容全部为英文。
                "formula": 影响因素和响应变量之间的对应公式，每个响应变量都有一个确定的对应公式，公式以数学公式的形式给出，\
                    'formula'的格式为json，每个元素的key为响应变量的名称，value为影响因素组成的一个公式，'formula'的长度与'response_var'相同\
                    'formula'的内容全部为英文
                "var_explain": 对变量的中文解释，包含新生成的影响因素和响应变量，'var_explain'的格式为json，包含'influence_factor'和'response_var'两个key，\
                    分别是对'影响因素'和'响应变量'的中文解释，'influence_factor'和'response_var'的内容均为list，\
                    list的内容为dict，dict举例如下："'foreign_policy': '外交政策'"。
                
                    
                
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
            'influence_factor': influence_factor,
            'response_var': response_var
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
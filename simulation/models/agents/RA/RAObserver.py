import json

from simulation.models.agents.LLMAgent import LLMAgent

MODEL_LIST = {
    'think': ['deepseek-r1:32b', 'deepseek-r1:32b-qwen-distill-q8_0'],
    'nothink': ['gpt-4o']
}


class RequirementAnalysisObserver(LLMAgent):
    def __init__(self, agent_name='RAAgent', requirement='',
                 llm_model='deepseek-r1:32b-qwen-distill-q8_0'):
        super().__init__(agent_name=agent_name,
                         has_chat_history=False,
                         online_track=False,
                         json_format=False,
                         system_prompt='',
                         llm_model=llm_model)
        self.re_analysis_res = None
        print('this is RAObserver')
        self.requirement = requirement
        self.system_prompt = '''
            我定义了一个用于需求分析的Agent，他会将我输入的需求：{requirement}解析为一个格式化的json数据。
            你是这个Agent观测者，任务为观测他生成的json数据是否是预期的格式，如果是返回True，否则返回False。
            json数据的正确格式为：{
                "goal": {
                    "category": str1,
                    "explain": str2,
                },
                "influence_factor": [
                    str,
                    ...
                ],
                "response_var": [
                    str,
                    ...
                ],
                "formula": {
                    key: value,
                    ...
                },
                "exp_params": {
                    "exp_method": str,
                    "params": {
                        key: [str, ...],
                        ...
                    }
                }
            }, 其中str为字符串，str1和str2为中文字符串，其余全部为英文, 省略号表示后面还有相似内容，
            'key: value'表示的是字典，key和value都是英文字符串。
            你需要额外注意'exp_params'的'params'中元素数量与'response_var'的元素数量相同
        '''
        self.is_first = True

    def requirement_observe(self, req, re_analysis_res):
        self.re_analysis_res = re_analysis_res
        info_prompt = '需求分析Agent解析的结果为：{re_analysis_res}'
        param_dict = {
            're_analysis_res': re_analysis_res,
            'requirement': req,
        }
        if self.llm_model in MODEL_LIST['think']:
            llm_response, think = self.get_response(info_prompt, input_param_dict=param_dict,
                                                    is_first_call=self.is_first)
        else:
            llm_response = self.get_response(info_prompt, input_param_dict=param_dict,
                                             is_first_call=self.is_first)
        self.is_first = False

        try:
            res = llm_response
        except Exception as e:
            print(e)

        return res

    def requirement_format_judge(self, analysis_res: json) -> bool:
        target_keys = ['goal', 'influence_factor', 'response_var', 'formula', 'exp_params']
        goal_keys = ['category', 'explain']
        exp_params_keys = ['exp_method', 'params']
        print(target_keys)
        if list(analysis_res.keys()) != target_keys or list(analysis_res['goal'].keys()) != goal_keys \
                or list(analysis_res['exp_params'].keys()) != exp_params_keys \
                or type(analysis_res['exp_params']['params']) is not dict:
            print("JSON格式错误")
            return False
        elif len(analysis_res['response_var']) != len(analysis_res['formula']):
            print("响应变量与公式数量不符")
            return False
        return True

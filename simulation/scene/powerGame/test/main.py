
from simulation.models.agents.RAAgent import RequirementAnalysisAgent

if __name__ == '__main__':
    ra = RequirementAnalysisAgent()
    req = '我想要复现古巴导弹危机中美国和古巴在各个时间段的行为，分析什么因素对战争的走势影响最大'
    res = ra.requirement_analysis(req)
    print(res)

# from openai import OpenAI
#
# client = OpenAI(
#     base_url="https://uc.chatgptten.com/v1",
#     api_key="sk-IMblefS5KQ5ET8izUvenvX71tOXiIZDp3ICQ33mFcUtKV8lq"
# )
# try:
#     response = client.chat.completions.create(
#         model="o1-preview",
#         messages=[
#             {"role": "user", "content": "天津大学怎么样。"}
#         ],
#     )
# except Exception as e:
#     print(e)
'''
response = client.chat.completions.create(
  model="gpt-4o",
  #   这些都可以：
  #   gpt-3.5-turbo-0125
  #   gpt-3.5-turbo-0613
  #   gpt-3.5-turbo-instruct
  #   gpt-3.5-turbo
  #   gpt-4-0125-preview
  #   gpt-4-1106-preview
  #   gpt-4-all
  #   gpt-4-gizmo-*
  #   gpt-4-turbo-2024-04-09
  #   gpt-4-turbo-preview
  #   gpt-4-turbo
  #   gpt-4-vision-preview
  #   gpt-4.1-2025-04-14
  #   gpt-4.1-mini-2025-04-14
  #   gpt-4.1-mini
  #   gpt-4.1-nano-2025-04-14
  #   gpt-4.1-nano
  #   gpt-4.1
  #   gpt-4.5-preview-2025-02-27
  #   gpt-4.5-preview(这个用不了)
  #   gpt-4
  #   gpt-4o-2024-05-13
  #   gpt-4o-2024-08-06
  #   gpt-4o-2024-11-20
  #   gpt-4o-all
  #   gpt-4o-image
  #   gpt-4o-mini-2024-07-18
  #   gpt-4o-mini
  #   gpt-4o-plus
  #   gpt-4o
  #   gpt-image-1
  messages=[
      {"role": "user", "content": "天津大学怎么样。"}
  ],
  # timeout=100,

)
print(response.choices[0].message.content)
'''
'''
{
  "goal": {
    "category": "现象解释",
    "explain": "分析古巴导弹危机中美国和古巴的行为模式及其背后的影响因素。"
  },
  "influence_factor": [
    "policy_decisions", 
    "time_sensitivity", 
    "alliance_support", 
    "information_transparency", 
    "economic_sanctions"
  ],
  "response_var": [
    "tension_level",
    "military_actions",
    "crisis_resolution_speed"
  ],
  "formula": [
    {
      "tension_level": "policy_decisions + time_sensitivity - information_transparency"
    },
    {
      "military_actions": "(time_sensitivity * alliance_support) / economic_sanctions"
    },
    {
      "crisis_resolution_speed": "1 / (economic_sanctions + policy_decisions)"
    }
  ],
  "exp_params": {
    "exp_method": "NK因子设计",
    "params": [
      {
        "policy_decisions": ["conservative", "moderate", "aggressive"]
      },
      {
        "time_sensitivity": ["low", "medium", "high"]
      },
      {
        "alliance_support": ["weak", "neutral", "strong"]
      },
      {
        "information_transparency": ["opaque", "partial", "transparent"]
      },
      {
        "economic_sanctions": ["light", "moderate", "severe"]
      }
    ]
  }
}
'''
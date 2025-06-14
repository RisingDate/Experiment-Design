
from simulation.models.agents.RAAgent import RequirementAnalysisAgent

if __name__ == '__main__':
    ra = RequirementAnalysisAgent()
    req = '我想要复现古巴导弹危机中美国和古巴在各个时间段的行为，分析什么因素对战争的走势影响最大'
    # res = ra.requirement_analysis(req)
    # print(res)

from openai import OpenAI

client = OpenAI(
    base_url="https://uc.chatgptten.com/v1",
    api_key="sk-IMblefS5KQ5ET8izUvenvX71tOXiIZDp3ICQ33mFcUtKV8lq"
)

response = client.chat.completions.create(
  model="gpt-image-1",
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
{
    "goal": {
        "category": "phenomenon explanation",
        "explain": "The goal is to understand and explain the factors that influenced the outcome of the Cuban Missile Crisis by analyzing historical behavior patterns and determining key influencing variables."
    },
    "influence_factor": [
        "political_tension",
        "military_preparedness",
        "diplomatic_communication",
        "public_sentiment",
        "economic_sanctions"
    ],
    "response_var": [
        "conflict escalation",
        "negotiation_success",
        "outcome_resolution"
    ],
    "formula": [
        {
            "conflict_escalation": "political_tension + military_preparedness - diplomatic_communication"
        },
        {
            "negotiation_success": "diplomatic_communication * public_sentiment / economic_sanctions"
        },
        {
            "outcome_resolution": "(military_preparedness + political_tension) * (1 - public_sentiment)"
        }
    ],
    "exp_params": {
        "exp_method": "orthogonal design",
        "params": [
            {
                "political_tension": ["low", "medium", "high"]
            },
            {
                "military_preparedness": ["low", "medium", "high"]
            },
            {
                "diplomatic_communication": ["poor", "average", "excellent"]
            },
            {
                "public_sentiment": ["negative", "neutral", "positive"]
            },
            {
                "economic_sanctions": ["none", "moderate", "severe"]
            }
        ]
    }
}
'''
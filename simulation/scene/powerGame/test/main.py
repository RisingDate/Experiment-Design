
from simulation.models.agents.RAAgent import RequirementAnalysisAgent

if __name__ == '__main__':
    ra = RequirementAnalysisAgent()
    req = '我想要复现古巴导弹危机中美国和古巴在各个时间段的行为，分析什么因素对战争的走势影响最大'
    res = ra.requirement_analysis(req)
    print(res)

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
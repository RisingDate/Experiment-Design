
from openai import OpenAI

model_name = [
    'gpt-3.5-turbo-0125',
    'gpt-3.5-turbo-0613',
    'gpt-3.5-turbo-instruct',
    'gpt-3.5-turbo',
    'gpt-4-0125-preview',
    'gpt-4-1106-preview',
    'gpt-4-all',
    'gpt-4-gizmo-*',
    'gpt-4-turbo-2024-04-09',
    'gpt-4-turbo-preview',
    'gpt-4-turbo',
    'gpt-4-vision-preview',
    'gpt-4.1-2025-04-14',
    'gpt-4.1-mini-2025-04-14',
    'gpt-4.1-mini',
    'gpt-4.1-nano-2025-04-14',
    'gpt-4.1-nano',
    'gpt-4.1',
    'gpt-4.5-preview-2025-02-27',
    'gpt-4',
    'gpt-4o-2024-05-13',
    'gpt-4o-2024-08-06',
    'gpt-4o-2024-11-20',
    'gpt-4o-all',
    'gpt-4o-image',
    'gpt-4o-mini-2024-07-18',
    'gpt-4o-mini',
    'gpt-4o-plus',
    'gpt-4o',
    'gpt-image-1'
]

client = OpenAI(
    base_url="https://uc.chatgptten.com/v1",
    api_key="sk-IMblefS5KQ5ET8izUvenvX71tOXiIZDp3ICQ33mFcUtKV8lq"
)
response = None
try:
    response = client.chat.completions.create(
        model="o1-preview",
        messages=[
            {"role": "user", "content": "天津大学怎么样。"}
        ],
    )
    print(response.choices[0].message.content)

except Exception as e:
    print(e)



from groq import Groq
from config import groq_api_key

client = Groq(api_key=groq_api_key)


def request_to_lmm(content, query):
    return client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct",
        temperature=0,
        max_tokens=80,
        messages=[
            {"role": "system", "content": content},
            {"role": "user", "content": f'User request: "{query}"'}
        ]
    )

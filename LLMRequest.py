from groq import Groq

api_key = "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"
client = Groq(api_key=api_key)


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

from openai import OpenAI

from battlecode.settings import API_URL, API_KEY, MODEL, THINKING_MODE


_client = OpenAI(
    api_key=API_KEY,
    base_url=API_URL,
)


class AIClient:
    @staticmethod
    def chat_response(prompt: str) -> str:
        resp = _client.completions.create(
            model=MODEL,
            prompt=prompt,
            stream=False,
            extra_body={
                "reasoning": {
                    "enabled": THINKING_MODE,
                }
            },
        )
        return resp.choices[0].text

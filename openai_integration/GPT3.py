import openai


class Bot:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def generate(self, system: str):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": "prompt?"},
            ]
        )
        content = response['choices'][0]['message']['content']
        return content

    def talk(self, system: str, message: str):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": message},
            ]
        )
        content = response['choices'][0]['message']['content']
        return content
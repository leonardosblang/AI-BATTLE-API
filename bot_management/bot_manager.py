import os

from openai_integration.GPT3 import Bot
from openai_integration.prompts import Prompts

class BotManager:
    def __init__(self):
        key = os.environ["OPENAI_API_KEY"]
        self.bot = Bot(key)
        self.prompts = Prompts()

    def talk(self, system, message):
        return self.bot.talk(system,message)

    def generate(self, prompt):
        return self.bot.generate(str(prompt))

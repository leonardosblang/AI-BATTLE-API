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

    def generate_theme(self):
        return self.bot.generate_theme()

    def generate_player_classes(self, theme, num_classes):
        return self.bot.generate_player_classes(theme, num_classes)

    def generate_monsters(self, theme, num_monsters):
        return self.bot.generate_monsters(theme, num_monsters)

    def generate_backgrounds(self, theme, num_backgrounds):
        return self.bot.generate_backgrounds(theme, num_backgrounds)

    def generate_cards(self, player_class, num_cards,usernam):
        return self.bot.generate_cards(player_class, num_cards,usernam)

    def generate_items(self, theme, num_items, usernam):
        return self.bot.generate_items(theme, num_items, usernam)
class Prompts:
    def __init__(self):
        self.map_prompt = "you will give me a prompt to generate a map similar to this one: clean map of fictional world,  trending on artstation, no text on it. you will give me only the prompt and nothing else. you can give the map random themes, such as desert, ice, lava, future. describe as much as possible in that way. don't break 20 words. separete words with ",". try to separe words as much as possible. try to be different than the original. answer always with only the prompt"
        # read card.txt and set it to self.card_prompt
        with open('openai_integration/card.txt', 'r') as file:
            self.card_prompt = file.read().replace('\n', '')

        with open('openai_integration/item.txt', 'r') as file:
            self.item_prompt = file.read().replace('\n', '')
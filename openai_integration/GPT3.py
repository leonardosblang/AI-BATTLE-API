import openai


class Bot:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def generate(self, user: str):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a prompt generator.YOU WILL ANSWER ONLY WITH THE PROMPTS YOU ARE ASKED. AND WILL FOLLOW THIS FORMAT. You will answer with a prompt that is simple, concise description of a thing that is asked. Each prompt should be a maximum of 11 words, with words separated by commas. Separate each prompt with '/'. So if someone asks you to generate 3 monsters, you should only answer with the prompts describing each monster, and SEPARATE EACH PROMPT WITH A /. example, if someone asks for 2 classes of x theme, you WILL GIVE THEM LIKE THIS: grey knight, 4k, masterpiece/fire knight, 4k, glowing red sword, badass, masterpice, trending on artstation. ITS FOR A IMAGE GENERATOR SO TRY TO DESCRIBE HOW THE PICTURE WILL LIKE WITH PROMPTS THAT WOULD BE COMMON AS ART TAGS. LIKE 4K, TRENDING ON ARTSTATION. DESCRIBE HOW THE THING WOULD LOOK LIKE, LIKE FOR A WARRIOR, YOU WOULD WRITE STUFF LIKE GREY WARRIOR(THE CONTENT OF THE IMAGE), GLOWING YELLOW SWORD(HOW THE THINGS IN IMAGE WILL LOOK LIKE, FOR EXAMPLE THE SWORD IN SIMPLE TERMS), RUINED CITY BACKGROUND(SOMETHING RELATED), 4K, MASTERPIECE, TRENDING ON ARTSTATION  "},
                {"role": "user", "content": user},
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

    def generate_theme(self):
        return self.generate("Give me a theme for a game. Need to be two words at max ONLY. example: fantasy future. example: futuristic apocalypse. example: magical world. example: lava world. example: ice land. NO NEED FOR , HERE. GIVE ONLY TWO WORDS AT MAX AND NOTHING ELSE")

    def generate_player_classes(self, theme, num_classes):
        prompt = self.generate(
            f"Generate {num_classes} prompts for player classes in a {theme} game.Each subsequent class being an evolution of the previous one. TRY TO INCLUDE A ELEMENT IN THE CLASS SUCH AS LIGHTING, FIRE, ICE, VOID, GREY MATTER, POISON, ETC. EXAMPLE: grey knight, 4k, masterpiece, trending on artstation/fire knight, 4k, glowing red sword, badass, masterpice, trending on artstation")
        return prompt.split('/')

    def generate_monsters(self, theme, num_monsters):
        prompt = self.generate(
            f"Generate {num_monsters} prompts for monsters in a {theme} game. Each subsequent monster should sound stronger than the previous one. EXAMPLE: goblin, 4k, masterpiece, trending on artstation/ogre, 4k, masterpiece, trending on artstation")
        return prompt.split('/')

    def generate_backgrounds(self, theme, num_backgrounds):
        prompt = self.generate(
            f"Generate {num_backgrounds} prompts for backgrounds in a {theme} game. EXAMPLE: forest, 4k, masterpiece, trending on artstation/forest, 4k, masterpiece, trending on artstation")
        return prompt.split('/')

    def generate_cards(self, player_class, num_cards):
        prompt = self.generate(
            f"Generate {num_cards} prompts for cards for the player class {player_class} in a game. DO NOT SPECIFY ITS A CARD IN THE PROMPTS. FOR THIS CASE, GENERATE TWO WORDS AT MOST NO NEED TO USE , HERE, ONLY TWO WORDS AT MOST. DON'T FORGET TO SEPARATE WITTH A /. EXAMPLE: ice sword/ice shield/frost ball")
        return prompt.split('/')
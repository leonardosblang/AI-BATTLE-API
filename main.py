from fastapi import FastAPI
from settings_management.settings_manager import SettingsManager
from settings_management.webhook_manager import WebhookManager
from image_processing.image_processor import ImageProcessor
from bot_management.bot_manager import BotManager
from storage.s3 import S3Manager
from webui_integration.api_manager import APIManager

app = FastAPI()

# Initialize classes
settings_manager = SettingsManager()
webhook_manager = WebhookManager(settings_manager)
webhook_manager.load_ngrok_settings()
bot_manager = BotManager()
s3_manager = S3Manager("storage/config.json")
api_manager = APIManager()

# Initialize ImageProcessor with required arguments
image_processor = ImageProcessor(api_manager, bot_manager, s3_manager)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/models")
async def root():
    return api_manager.return_model()


@app.get("/gen-image/{prompt}/{steps}")
async def gen_image(prompt: str, steps: int):
    return image_processor.generate_image(prompt, steps)


@app.get("/gen-fish/fish/{steps}")
async def gen_fish(steps: int):
    return image_processor.generate_fish_image(steps)


@app.get("/gpt3/{prompt}")
async def gpt3_prompt(system: str, message: str):
    return bot_manager.talk(system, message)


@app.get("/gen-rpg/map/{steps}")
async def gen_map(steps: int):
    return image_processor.generate_map_image(steps)


@app.get("/gen-image/{prompt}/{steps}/s3")
async def gen_image_s3(prompt: str, steps: int):
    return image_processor.generate_image_s3(prompt, steps)


@app.post("/generate_game_images")
async def generate_game_images(user: str,  num_classes: int, num_monsters: int, num_backgrounds: int,
                               num_cards: int):

    steps = 20
    theme = bot_manager.generate_theme()
    print(theme)
    player_class_prompts = bot_manager.generate_player_classes(theme, num_classes)
    player_class_images = image_processor.generate_images_s3(player_class_prompts, steps, user, "class")

    monster_prompts = bot_manager.generate_monsters(theme, num_monsters)
    monster_images = image_processor.generate_images_s3(monster_prompts, steps, user, "monster")

    background_prompts = bot_manager.generate_backgrounds(theme, num_backgrounds)
    background_images = image_processor.generate_images_s3(background_prompts, steps, user, "background")

    card_prompts = bot_manager.generate_cards(player_class_prompts[0], num_cards)
    card_images = image_processor.generate_images_s3(card_prompts, steps, user, "card")

    return {
        "player_class_images": player_class_images,
        "monster_images": monster_images,
        "background_images": background_images,
        "card_images": card_images,
    }

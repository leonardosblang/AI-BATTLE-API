from fastapi import FastAPI
from settings_management.settings_manager import SettingsManager
from settings_management.webhook_manager import WebhookManager
from image_processing.image_processor import ImageProcessor
from bot_management.bot_manager import BotManager
from storage.s3 import S3Manager
from webui_integration.api_manager import APIManager
from database.mongo_connect import MongoDB
from card_generation.card_image_gen import CardCreator

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
async def generate_game_images(user: str, num_classes: int, num_monsters: int, num_backgrounds: int,
                               num_cards: int):
    db = MongoDB()
    user_doc = {
        "username": user,
        "experience": 0,
        "level": 0,
        "current_equips": [],
        "shop_equips": [],
        "deck": [],
        "current_class": "none"
    }
    db.insert_into_collection("users", user_doc)
    steps = 20
    theme = bot_manager.generate_theme()
    print(theme)
    player_class_prompts = bot_manager.generate_player_classes(theme, num_classes)
    player_class_images = image_processor.generate_images_s3(player_class_prompts, steps, user, "class")

    monster_prompts = bot_manager.generate_monsters(theme, num_monsters)
    monster_images = image_processor.generate_images_s3(monster_prompts, steps, user, "monster")

    background_prompts = bot_manager.generate_backgrounds(theme, num_backgrounds)
    background_images = image_processor.generate_images_s3(background_prompts, steps, user, "background")

    card_prompts = bot_manager.generate_cards(player_class_prompts[0], num_cards, user)
    card_images = image_processor.generate_images_s3(card_prompts, steps, user, "card")

    user_doc = db.find_in_collection("users", {"username": user})[0]  # Assuming usernames are unique
    deck = user_doc["deck"]  # Fetch the deck of the user

    for i, card in enumerate(deck):


            card_image_object_name = user + "_" + "card" + str(i+1) + ".webp"
            print(card_image_object_name)
            temp_file_path = s3_manager.download_image_from_s3(card_image_object_name, user, i+1)

            if not temp_file_path:  # Check if a valid file path is returned
                print(f"Error downloading image for card {i+1}")
                continue  # Skip this iteration if image download failed

            # First, check that the card has at least two effects. If it doesn't, use a default value.
            if len(card["effects"]) >= 2:
                main_effect_id = card["effects"][0]["id"]
                target_effect_id = card["effects"][1]["id"]
            else:
                main_effect_id = card["effects"][0]["id"]
                target_effect_id = ""

            card_creator = CardCreator(card["rarity"], temp_file_path, card["name"], main_effect_id, target_effect_id,
                                       str(card["mp_cost"]))

            card_creator.create_card()

            # Upload the generated card back to S3
            new_card_image_object_name = f"{user}_fullcard{i + 1}"
            with open("./card_generation/card.png", "rb") as full_card_image_file:
                new_image_url = s3_manager.upload_image_to_s3(full_card_image_file, new_card_image_object_name)

            # Now 'new_image_url' contains the presigned url
            # Update MongoDB with the URL. Assuming the card's id is stored in card["_id"]
            # Update MongoDB with the URL. Using combination of card's name and order as identifier
            db.update_in_collection("users",
                                    {"username": user,
                                     "deck.name": card["name"],
                                     "deck.order": card["order"]},
                                    {"$set": {"deck.$.image_url": new_image_url}})

    return {
        "player_class_images": player_class_images,
        "monster_images": monster_images,
        "background_images": background_images,
        "card_images": card_images,
    }

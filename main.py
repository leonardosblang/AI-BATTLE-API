import os
import random
import sys
from openai_integration.GPT3 import Bot
from fastapi import FastAPI
from fastapi.logger import logger
from pydantic import BaseSettings
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from images_manip.compression import Compression
import webuiapi
from PIL import Image
from openai_integration.prompts import Prompts

# Setting up ngrok
class Settings(BaseSettings):
    BASE_URL = "http://localhost:8000"
    USE_NGROK = os.environ.get("USE_NGROK", "False") == "True"


settings = Settings()


def init_webhooks(base_url):
    pass


# setting up Fast API
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# loading ngrok settings
if settings.USE_NGROK:
    from pyngrok import ngrok

    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000

    public_url = ngrok.connect(port).public_url
    logger.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    settings.BASE_URL = public_url
    init_webhooks(public_url)

# setting up sd
api = webuiapi.WebUIApi()

options = api.get_sd_models()
#save options to file txt
with open('options.txt', 'w') as f:
    f.write(str(options))



# loading api key
key = os.environ["OPENAI_API_KEY"]
bot = Bot(key)


# models
fish = 'xks_3200.ckpt [3bfc733a]'
#sd = '512-base-ema.ckpt [09dd2ae4]'
sd = 'v1-5-pruned-emaonly.ckpt [cc6cb27103]'

# api endpoints

@app.get("/")
async def root():
    return {"message": "Hello World"}


#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}


# @app.get("/compress/base64")
# async def compress_base64():
#     test = Compression('outputs/samples/000003.1023502011.png')
#     return test.get_base64()


# @app.get("/compress/image")
# async def compress():
#     test = Compression('outputs/samples/000003.1023502011.png')
#     temp_file = test.return_webp()
#     return FileResponse(temp_file.name, media_type="image/webp")



#generic stuff for testing

@app.get("/gen-image/{prompt}/{steps}")
async def gen_image(prompt: str, steps: int):
    options = {}
    options['sd_model_checkpoint'] = sd
    api.set_options(options)
    results = api.txt2img(prompt=prompt,
                          cfg_scale=7,
                          steps=steps,
                          )

    test = Compression(results.image)
    temp_file = test.return_webp()
    return FileResponse(temp_file.name, media_type="image/webp")


@app.get("/gen-fish/fish/{steps}")
async def gen_fish(steps: int):

    fish_num = str(random.randint(1, 32))
    options = {}
    options['sd_model_checkpoint'] = fish
    api.set_options(options)
    im = Image.open('images_for_analysis/'+fish_num+'.png')
    results = api.img2img(images=[im],
                          prompt="xks, sksksk artstyle",
                          cfg_scale=7,
                          steps=steps,
                          )

    im = results.image.convert("RGBA")

    tolerance = 20


    data = im.getdata()
    newData = []
    for item in data:
        if abs(item[0] - 255) <= tolerance and abs(item[1] - 255) <= tolerance and abs(item[2] - 255) <= tolerance:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    im.putdata(newData)

    temp_file = 'temp.png'
    im.save(temp_file, "PNG")

    return FileResponse(temp_file, media_type="image/png")


@app.get("/gpt3/{prompt}")
async def gpt3_prompt(system: str, message: str):
    return bot.generate(system,message)

#ai rpg stuff

ai_prompt = Prompts()
@app.get("/gen-rpg/map/{steps}")
async def gen_map(steps: int):

    map_num = str(random.randint(1, 2))
    options = {}
    options['sd_model_checkpoint'] = sd
    api.set_options(options)
    im = Image.open('maps_for_analysis/' + map_num + '.png')


    prompt = bot.generate(str(ai_prompt.map_prompt))

    results = api.img2img(images=[im], prompt=prompt, cfg_scale=7, denoising_strength=0.7)

    print(prompt)

    test = Compression(results.image)
    temp_file = test.return_webp()
    return FileResponse(temp_file.name, media_type="image/webp")


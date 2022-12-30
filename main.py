import os
import random
import sys
import openai
from fastapi import FastAPI
from fastapi.logger import logger
from pydantic import BaseSettings
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from images_manip.compression import Compression
import webuiapi
from PIL import Image


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
api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)
api = webuiapi.WebUIApi(sampler='Euler a', steps=20)

# loading api key
openai.api_key = "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"

# models
fish = 'xks_3200.ckpt [3bfc733a]'
sd = '512-base-ema.ckpt [09dd2ae4]'


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
async def gen_image(steps: int):

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
async def gpt3_prompt(prompt: str):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response

import os
import sys

from fastapi import FastAPI
from fastapi.logger import logger
from pydantic import BaseSettings
from starlette.middleware.cors import CORSMiddleware

from images_manip.compression import Compression


class Settings(BaseSettings):
    BASE_URL = "http://localhost:8000"
    USE_NGROK = os.environ.get("USE_NGROK", "False") == "True"


settings = Settings()


def init_webhooks(base_url):
    pass


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.USE_NGROK:
    from pyngrok import ngrok

    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000

    public_url = ngrok.connect(port).public_url
    logger.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    settings.BASE_URL = public_url
    init_webhooks(public_url)




@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/compress/base64/{data}")
async def compress_base64():
    test = Compression('outputs/samples/000003.1023502011.png')
    return test.get_base64()


import sys
from fastapi.logger import logger
from pyngrok import ngrok

class WebhookManager:
    def __init__(self, settings_manager):
        self.settings = settings_manager

    def init_webhooks(self, base_url):
        pass  # Your webhook initialization code here

    def load_ngrok_settings(self):
        if self.settings.USE_NGROK:
            port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000
            public_url = ngrok.connect(port).public_url
            logger.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))
            self.settings.BASE_URL = public_url
            self.init_webhooks(public_url)

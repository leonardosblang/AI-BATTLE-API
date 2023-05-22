import webuiapi

class APIManager:
    def __init__(self):
        self.api = webuiapi.WebUIApi()
        self.options = self.api.get_sd_models()
        with open('options.txt', 'w') as f:
            f.write(str(self.options))

    def set_options(self, options):
        self.api.set_options(options)

    def txt2img(self, prompt, cfg_scale, steps):
        return self.api.txt2img(prompt=prompt, cfg_scale=cfg_scale, steps=steps)

    def img2img(self, images, prompt, cfg_scale, denoising_strength):
        return self.api.img2img(images=images, prompt=prompt, cfg_scale=cfg_scale, denoising_strength=denoising_strength)

    def return_model(self):
        return self.api.get_sd_models()
from PIL import Image
import random
from .compression import Compression
from fastapi.responses import FileResponse


class ImageProcessor:
    def __init__(self, api_manager, bot_manager, s3_manager):
        self.api_manager = api_manager
        self.bot_manager = bot_manager
        self.s3_manager = s3_manager
        self.fish = 'xks_3200.ckpt [3bfc733a]'
        self.sd = 'anything-v4.5.ckpt [fbcf965a62]'

    def generate_image(self, prompt, steps):
        options = {}
        options['sd_model_checkpoint'] = self.sd
        self.api_manager.set_options(options)
        results = self.api_manager.txt2img(prompt=prompt,
                                           cfg_scale=7,
                                           steps=steps,
                                           )

        test = Compression(results.image)
        temp_file = test.return_webp()
        return FileResponse(temp_file, media_type="image/webp")  # Removed .name

    def generate_fish_image(self, steps):
        fish_num = str(random.randint(1, 32))
        options = {}
        options['sd_model_checkpoint'] = self.fish
        self.api_manager.set_options(options)
        im = Image.open('images_for_analysis/' + fish_num + '.png')
        results = self.api_manager.img2img(images=[im],
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

    def generate_map_image(self, steps):
        map_num = str(random.randint(1, 2))
        options = {}
        options['sd_model_checkpoint'] = self.sd
        self.api_manager.set_options(options)
        im = Image.open('maps_for_analysis/' + map_num + '.png')

        prompt = self.bot_manager.generate(str(self.bot_manager.prompts.map_prompt))

        results = self.api_manager.img2img(images=[im], prompt=prompt, cfg_scale=7, denoising_strength=0.7)

        print(prompt)

        test = Compression(results.image)
        temp_file = test.return_webp()
        return FileResponse(temp_file, media_type="image/webp")

    def generate_image_s3(self, prompt, steps, user, image_type, number):
        options = {}
        options['sd_model_checkpoint'] = self.sd
        self.api_manager.set_options(options)
        results = self.api_manager.txt2img(prompt=prompt,
                                           cfg_scale=7,
                                           steps=steps,
                                           )

        test = Compression(results.image)
        temp_file_path = test.return_webp()  # Assuming this returns a file path now
        object_name = f"{user}_{image_type}{number}.webp"

        # Reopen the file before uploading
        #   with open(temp_file_path, 'rb') as temp_file:
        #      self.s3_manager.upload_image_to_s3(temp_file, object_name)
        # return FileResponse(temp_file_path, media_type="image/webp")

        with open(temp_file_path, 'rb') as temp_file:
            presigned_url = self.s3_manager.upload_image_to_s3(temp_file, object_name)



        return presigned_url

    def generate_images_s3(self, prompts, steps, user, image_type):
        images = []
        for i, prompt in enumerate(prompts):
            print(f"Generating {image_type} image {i + 1} with prompt: {prompt}")
            image = self.generate_image_s3(prompt, steps, user, image_type, i + 1)
            images.append(image)
        return images

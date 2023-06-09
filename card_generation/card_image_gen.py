from PIL import Image, ImageDraw, ImageFont


class CardCreator:
    def __init__(self, rarity, image_path, card_name, card_description, card_description2, card_cost):
        self.rarity = rarity
        self.image_path = image_path
        self.card_name = card_name
        self.card_description = card_description
        self.card_description2 = card_description2
        self.card_cost = card_cost

    @staticmethod
    def format_string(text):
        words = text.split('_')
        formatted_words = [word.capitalize() for word in words]
        formatted_string = ' '.join(formatted_words)
        return formatted_string

    def create_card(self):
        # Define images based on rarity
        rarity_images = {"common": './card_generation/bg.png',
                         "uncommon": './card_generation/bguncommon.png',
                         "rare": './card_generation/bgrare.png',
                         "legendary": './card_generation/bglegendary.png'}

        self.card_description = self.format_string(self.card_description)
        self.card_description2 = self.format_string(self.card_description2)

        # Open the base image
        base_img = Image.new('RGBA', (120, 200))

        # Open and place the bg1 image
        bg1_img = Image.open('./card_generation/bg1.png')
        if bg1_img.mode != 'RGBA':
            bg1_img = bg1_img.convert('RGBA')

        base_img.paste(bg1_img, (0, 0), bg1_img)

        # Open and resize the card image
        card_img = Image.open(self.image_path).resize((120, 150))

        # If the image is not RGBA, convert it
        if card_img.mode != 'RGBA':
            card_img = card_img.convert('RGBA')

        # Place the card image at the center of the base image
        base_img.paste(card_img, (0, 0))  # Adjusted to place image 'a' at center

        # Open the bg image based on rarity
        bg_img = Image.open(rarity_images[self.rarity])
        if bg_img.mode != 'RGBA':
            bg_img = bg_img.convert('RGBA')

        base_img.paste(bg_img, (0, 0), bg_img)

        # Open the bg3 image
        bg3_img = Image.open('./card_generation/bg3.png')
        if bg3_img.mode != 'RGBA':
            bg3_img = bg3_img.convert('RGBA')

        base_img.paste(bg3_img, (0, 0), bg3_img)

        # Initialize the drawing context
        draw = ImageDraw.Draw(base_img)

        # Define the font (assuming that 'unispace bd.otf' is in your working directory)
        font = ImageFont.truetype('./card_generation/unispace bd.otf', 8)

        # Draw the card name above the image
        draw.text((50, 10), self.card_name, fill='white', font=font)

        # Draw the card description below the image
        draw.text((5, 160), self.card_description, fill='white', font=font)

        draw.text((5, 175), self.card_description2, fill='white', font=font)

        font = ImageFont.truetype('./card_generation/unispace bd.otf', 12)
        # Draw the cost text on the blue circle
        draw.text((16, 11), self.card_cost, fill='white', font=font)  # Adjusted position for cost text

        # Save the image
        base_img.save('./card_generation/card.png')


# Use the class

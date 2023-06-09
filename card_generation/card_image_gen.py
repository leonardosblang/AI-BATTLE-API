from PIL import Image, ImageDraw, ImageFont

def create_card(rarity: str, image_path: str, card_name: str, card_description: str, card_cost: str):
    # Define images based on rarity
    rarity_images = {"common": 'bg.png',
                     "uncommon": 'bguncommon.png',
                     "rare": 'bgrare.png',
                     "legendary": 'bglegendary.png'}

    # Open the base image
    base_img = Image.new('RGBA', (120, 200))

    # Open and place the bg1 image
    bg1_img = Image.open('bg1.png')
    if bg1_img.mode != 'RGBA':
        bg1_img = bg1_img.convert('RGBA')

    base_img.paste(bg1_img, (0, 0), bg1_img)

    # Open and resize the card image
    card_img = Image.open(image_path).resize((120, 150))

    # If the image is not RGBA, convert it
    if card_img.mode != 'RGBA':
        card_img = card_img.convert('RGBA')

    # Place the card image at the center of the base image
    base_img.paste(card_img, (0, 0))  # Adjusted to place image 'a' at center

    # Open the bg image based on rarity
    bg_img = Image.open(rarity_images[rarity])
    if bg_img.mode != 'RGBA':
        bg_img = bg_img.convert('RGBA')

    base_img.paste(bg_img, (0, 0), bg_img)

    # Open the bg3 image
    bg3_img = Image.open('bg3.png')
    if bg3_img.mode != 'RGBA':
        bg3_img = bg3_img.convert('RGBA')

    base_img.paste(bg3_img, (0, 0), bg3_img)

    # Initialize the drawing context
    draw = ImageDraw.Draw(base_img)

    # Define the font (assuming that 'unispace bd.otf' is in your working directory)
    font = ImageFont.truetype('unispace bd.otf', 8)



    # Draw the card name above the image
    draw.text((50, 10), card_name, fill='white', font=font)

    # Draw the card description below the image
    draw.text((5, 160), card_description, fill='white', font=font)



    font = ImageFont.truetype('unispace bd.otf', 12)
    # Draw the cost text on the blue circle
    draw.text((12, 11), card_cost, fill='white', font=font)  # Adjusted position for cost text

    # Save the image
    base_img.save('card.png')

# Use the function
create_card('rare', 'a.png', 'Card Name', 'Card Description', '33')

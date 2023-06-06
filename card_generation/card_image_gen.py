from PIL import Image, ImageDraw, ImageFont, ImageOps

def colorize(image: Image.Image, color: str) -> Image.Image:
    # Convert the image to grayscale
    gray = image.convert('L')

    # Colorize the grayscale image with the given color
    result = ImageOps.colorize(gray, "black", color)

    return result.convert('RGBA')

def create_card(rarity: str, image_path: str, card_name: str, card_description: str, card_cost: str):
    # Define colors based on rarity
    rarity_colors = {"common": '#FFFFFF',  # no change
                     "uncommon": '#0000FF',  # blue
                     "rare": '#800080',  # purple
                     "legendary": '#FFD700'}  # gold

    # Open the base image
    base_img = Image.open('bg.png')

    # If the image is not RGBA, convert it
    if base_img.mode != 'RGBA':
        base_img = base_img.convert('RGBA')

    # Colorize the base image based on rarity
    if rarity != "common":  # common won't change color
        base_img = colorize(base_img, rarity_colors[rarity])

    # Open and resize the card image
    card_img = Image.open(image_path).resize((128, 128))

    # If the image is not RGBA, convert it
    if card_img.mode != 'RGBA':
        card_img = card_img.convert('RGBA')

    # Place the card image at the center of the base image
    base_img.paste(card_img, (-5, 25))

    # Initialize the drawing context
    draw = ImageDraw.Draw(base_img)

    # Define the font (assuming that arial.ttf is in your working directory)
    font = ImageFont.truetype('arial.ttf', 15)

    ellipse_position = (90, 0, 115, 25)  # Adjusted bounding box for a circle
    draw.ellipse(ellipse_position, fill='blue')

    # Draw the card name above the image
    draw.text((10, 5), card_name, fill='white', font=font)

    # Draw the cost text on the blue circle
    draw.text((100, 5), card_cost, fill='white', font=font)  # Adjusted position for cost text

    # Draw the card description below the image
    draw.text((5, 160), card_description, fill='white', font=font)

    # Save the image
    base_img.save('card.png')

# Use the function
create_card('rare', 'a.png', 'Card Name', 'Card Description', '3')

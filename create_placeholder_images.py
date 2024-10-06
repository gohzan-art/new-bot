from PIL import Image, ImageDraw, ImageFont
import os

def create_image(filename, size, text, color):
    if not os.path.exists(filename):
        img = Image.new('RGB', size, color)
        d = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        textwidth, textheight = d.textsize(text, font)
        x = (size[0] - textwidth) / 2
        y = (size[1] - textheight) / 2
        d.text((x, y), text, fill=(255, 255, 255), font=font)
        img.save(filename)
        print(f"Created placeholder image: {filename}")
    else:
        print(f"Image already exists, skipping: {filename}")

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

# Ensure base directories exist
ensure_directory('assets/images')
ensure_directory('assets/images/backgrounds')
ensure_directory('assets/images/rank_insignias')

# Create platoon logo
create_image('assets/images/platoon_logo.png', (800, 800), 'Platoon Logo', 'blue')

# Create camo background
create_image('assets/images/backgrounds/camo_background.png', (1920, 1080), 'Camo Background', 'green')

# Create welcome banner
create_image('assets/images/welcome_banner.png', (1200, 300), 'Welcome to the Platoon', 'navy')

# Create mission icon
create_image('assets/images/mission_icon.png', (200, 200), 'Mission', 'red')

# Create training icon
create_image('assets/images/training_icon.png', (200, 200), 'Training', 'orange')

# Create rank insignias
ranks = ['Private', 'Corporal', 'Sergeant', 'Staff Sergeant', 'Sergeant First Class', 'Master Sergeant', 'First Sergeant', 'Sergeant Major']
for rank in ranks:
    create_image(f'assets/images/rank_insignias/{rank.lower().replace(" ", "_")}.png', (200, 200), rank, 'red')

print("Placeholder image creation process completed!")
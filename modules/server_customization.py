import discord
from PIL import Image, ImageDraw, ImageFont
import io
import os

async def create_welcome_image(ctx, message):
    # Load background image
    background = Image.open("assets/images/backgrounds/camo_background.png")
    
    # Load and paste platoon logo
    logo = Image.open("assets/images/platoon_logo.png")
    logo = logo.resize((200, 200))
    background.paste(logo, (50, 50), logo)
    
    # Load welcome banner
    banner = Image.open("assets/images/welcome_banner.png")
    banner = banner.resize((800, 200))
    background.paste(banner, (560, 50), banner)
    
    # Add text
    draw = ImageDraw.Draw(background)
    title_font = ImageFont.truetype("assets/fonts/military_font.ttf", 48)
    body_font = ImageFont.truetype("assets/fonts/body_font.ttf", 24)
    
    draw.text((300, 300), "Welcome, Soldier!", font=title_font, fill='#FFFFFF')
    draw.text((300, 400), message, font=body_font, fill='#FFFFFF')
    
    # Save the image to a buffer
    buffer = io.BytesIO()
    background.save(buffer, 'PNG')
    buffer.seek(0)
    
    # Send the welcome image
    await ctx.send(file=discord.File(buffer, 'welcome.png'))

async def set_server_banner(ctx):
    # Check if the user uploaded an image
    if len(ctx.message.attachments) == 0:
        # Use default camo background if no image is uploaded
        banner_path = "assets/images/backgrounds/camo_background.png"
        with open(banner_path, 'rb') as f:
            banner_image = f.read()
    else:
        attachment = ctx.message.attachments[0]
        
        # Check if the file is an image
        if not attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            await ctx.send("The uploaded file must be an image (PNG, JPG, or GIF).")
            return

        # Download the image
        banner_image = await attachment.read()

    try:
        await ctx.guild.edit(banner=banner_image)
        await ctx.send("Server banner has been updated successfully!")
    except discord.errors.Forbidden:
        await ctx.send("I don't have permission to change the server banner.")
    except Exception as e:
        await ctx.send(f"An error occurred while updating the server banner: {str(e)}")

async def show_rank_insignia(ctx, rank):
    rank_file = f"assets/images/rank_insignias/{rank.lower().replace(' ', '_')}.png"
    if os.path.exists(rank_file):
        await ctx.send(file=discord.File(rank_file))
    else:
        await ctx.send(f"Rank insignia for {rank} not found.")

# Add this to your bot commands
@bot.command(name='rank')
async def rank(ctx, *, rank_name):
    await show_rank_insignia(ctx, rank_name)
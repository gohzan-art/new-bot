import discord
from discord.ext import commands
import asyncio
from PIL import Image, ImageDraw, ImageFont
import io

class XPSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.categories = ['fitness', 'acft', 'gaming', 'weapons', 'music', 'meme']

    @commands.command()
    async def rank(self, ctx, category=None):
        if category not in self.categories:
            await ctx.send("Invalid category, numbnuts. Try: " + ", ".join(self.categories))
            return
        
        # Placeholder for database query
        # In a real implementation, you'd fetch this data from your database
        xp = 1000
        level = 5
        
        rank_file = await self.create_rank_image(ctx.author, category, level)
        embed = discord.Embed(title=f"{category.capitalize()} Rank", color=discord.Color.red())
        embed.add_field(name="Level", value=level)
        embed.add_field(name="XP", value=xp)
        embed.set_image(url="attachment://rank.png")
        
        await ctx.send(file=rank_file, embed=embed)

    async def create_rank_image(self, user, category, level):
        rank_image = Image.open(f"assets/images/ranks/{self.get_rank_image(category, level)}")
        font = ImageFont.truetype("assets/fonts/military_stencil.ttf", 36)
        draw = ImageDraw.Draw(rank_image)
        draw.text((10, 10), f"{user.name}\nLevel {level}", font=font, fill=(255, 255, 255))
        
        buffer = io.BytesIO()
        rank_image.save(buffer, format="PNG")
        buffer.seek(0)
        return discord.File(buffer, filename="rank.png")

    def get_rank_image(self, category, level):
        ranks = {
            'fitness': ['couch_potato.png', 'beast_mode.png', 'freak_of_nature.png'],
            'acft': ['boot_bitch.png', 'warrior_god.png'],
            'gaming': ['fucking_noob.png', 'death_incarnate.png'],
            'weapons': ['range_jester.png', 'goddamn_deadeye.png'],
            'music': ['tone_deaf.png', 'music_maestro.png'],
            'meme': ['meme_peasant.png', 'legendary_shitposter.png']
        }
        rank_index = min(level // 10, len(ranks[category]) - 1)
        return ranks[category][rank_index]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Placeholder for XP calculation logic
        # In a real implementation, you'd have more complex logic here
        xp_gained = len(message.content) // 10

        # Placeholder for database update
        # In a real implementation, you'd update the user's XP in your database
        
        # Check for level up (placeholder logic)
        old_level = 1  # Placeholder, fetch this from your database in real implementation
        new_level = (old_level + 1) if xp_gained > 100 else old_level

        if new_level > old_level:
            await message.channel.send(f"Congratulations {message.author.mention}! You've leveled up to level {new_level}!")

async def setup(bot):
    await bot.add_cog(XPSystem(bot))
from PIL import Image, ImageDraw, ImageFont
import io

# Add this to the XPSystem class

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
        'weapons': ['range_jester.png', 'goddamn_deadeye.png']
    }
    rank_index = min(level // 10, len(ranks[category]) - 1)
    return ranks[category][rank_index]

@commands.command()
async def rank(self, ctx, category=None):
    if category not in self.categories:
        await ctx.send("Invalid category, numbnuts. Try: " + ", ".join(self.categories))
        return
    
    async with self.bot.db.acquire() as conn:
        row = await conn.fetchrow('''
            SELECT xp, level FROM user_xp
            JOIN user_levels USING (user_id, category)
            WHERE user_id = $1 AND category = $2
        ''', ctx.author.id, category)
    
    if not row:
        await ctx.send(f"You haven't even started in {category}. Get off your ass and do something!")
        return
    
    rank_file = await self.create_rank_image(ctx.author, category, row['level'])
    embed = discord.Embed(title=f"{category.capitalize()} Rank", color=discord.Color.red())
    embed.add_field(name="Level", value=row['level'])
    embed.add_field(name="XP", value=row['xp'])
    embed.set_image(url="attachment://rank.png")
    
    await ctx.send(file=rank_file, embed=embed)
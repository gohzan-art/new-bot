import discord
import random
import asyncio
import os

async def play_guess_the_rank(ctx):
    ranks = ['Private', 'Corporal', 'Sergeant', 'Staff Sergeant', 'Sergeant First Class', 'Master Sergeant', 'First Sergeant', 'Sergeant Major']
    rank_to_guess = random.choice(ranks)
    
    rank_file = f"assets/images/rank_insignias/{rank_to_guess.lower().replace(' ', '_')}.png"
    
    embed = discord.Embed(title="Guess the Rank", description="Can you guess this rank insignia?", color=discord.Color.blue())
    file = discord.File(rank_file, filename="rank.png")
    embed.set_image(url="attachment://rank.png")
    
    await ctx.send(file=file, embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    tries = 3
    while tries > 0:
        try:
            guess = await ctx.bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            return await ctx.send(f'Sorry, you took too long. The rank was {rank_to_guess}.')

        if guess.content.lower() == rank_to_guess.lower():
            return await ctx.send(f'Correct! The rank was {rank_to_guess}. You earned 15 XP!')
        else:
            tries -= 1
            if tries > 0:
                await ctx.send(f'Wrong guess. You have {tries} {"try" if tries == 1 else "tries"} left.')
            else:
                await ctx.send(f'Sorry, you\'re out of tries. The rank was {rank_to_guess}.')
import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class NotesSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def take_notes(self, ctx, *, notes):
        if not notes:
            await ctx.send("You didn't provide any notes, numbnuts. Try again.")
            return

        await ctx.send("Roger that. Processing your chicken scratch. Stand by...")

        try:
            response = client.chat.completions.create(
                model="gpt-4-0613",
                messages=[
                    {"role": "system", "content": "You are SGT Dickburgler, a no-nonsense military note-taking assistant. Organize and streamline the following notes into a clear, concise format. Use military time, organize information by topic, and include a brief summary at the top. Be direct and use military jargon where appropriate."},
                    {"role": "user", "content": notes}
                ]
            )
            
            organized_notes = response.choices[0].message.content

            notes_channel = discord.utils.get(ctx.guild.text_channels, name="notes-output")
            if not notes_channel:
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
                    ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                notes_channel = await ctx.guild.create_text_channel("notes-output", overwrites=overwrites)

            embed = discord.Embed(title="Organized Notes", description=organized_notes, color=discord.Color.green())
            embed.set_footer(text=f"Notes taken by {ctx.author.display_name} | {ctx.message.created_at.strftime('%Y-%m-%d %H:%M')}")

            await notes_channel.send(embed=embed)
            await ctx.send(f"Notes processed and posted in {notes_channel.mention}. Now drop and give me 20 for making me do your paperwork!")

        except Exception as e:
            await ctx.send(f"Listen here, maggot. An error occurred while processing your notes: {str(e)}. Fix it or you'll be on latrine duty for a month!")

def setup(bot):
    bot.add_cog(NotesSystem(bot))
import discord
from discord.ext import commands

class Feedback(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='feedback')
    async def submit_feedback(self, ctx, *, feedback):
        # Create an embed for the feedback
        embed = discord.Embed(title="New Feedback", description=feedback, color=discord.Color.green())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_footer(text=f"Submitted at {ctx.message.created_at}")

        # Send the feedback to a specific channel
        feedback_channel = self.bot.get_channel(FEEDBACK_CHANNEL_ID)  # Replace with your channel ID
        await feedback_channel.send(embed=embed)

        # Confirm to the user
        await ctx.send("Thank you for your feedback! It has been submitted for review.")

def setup(bot):
    bot.add_cog(Feedback(bot))
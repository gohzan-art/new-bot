import discord
from discord.ext import commands
from modules.xp_system import XPSystem
from modules.calendar_integration import CalendarIntegration
from modules.notes_system import NotesSystem
from modules.ui_elements import ProfileView, LeaderboardView, CalendarView, NotesView, OnboardingView, ServerSetupView

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_system = XPSystem(bot)
        self.calendar_integration = CalendarIntegration(bot)
        self.notes_system = NotesSystem(bot)

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Bot Commands", description="Here are all available commands:", color=discord.Color.blue())
        embed.add_field(name="!setupserver", value="Sets up the entire server layout (admin only)", inline=False)
        embed.add_field(name="!calendar", value="Shows calendar options", inline=False)
        embed.add_field(name="!notes", value="Opens the notes interface", inline=False)
        embed.add_field(name="!onboarding", value="Shows onboarding options for new members", inline=False)
        embed.add_field(name="!rank [category]", value="Displays your rank and XP in a specific category", inline=False)
        embed.add_field(name="!leaderboard", value="Shows interactive leaderboard for different categories", inline=False)
        embed.add_field(name="!profile", value="Shows your interactive profile with stats across categories", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def calendar(self, ctx):
        embed = discord.Embed(title="Calendar Options", description="Select an action:", color=discord.Color.green())
        view = CalendarView()
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def notes(self, ctx):
        embed = discord.Embed(title="Notes System", description="Click to take notes:", color=discord.Color.purple())
        view = NotesView()
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def onboarding(self, ctx):
        embed = discord.Embed(title="Onboarding", description="Welcome! Select an action:", color=discord.Color.orange())
        view = OnboardingView()
        await ctx.send(embed=embed, view=view)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setupserver(self, ctx):
        embed = discord.Embed(title="Server Setup", description="Warning: This will reset the server layout. Proceed?", color=discord.Color.red())
        view = ServerSetupView()
        await ctx.send(embed=embed, view=view)

    # Existing commands (leaderboard, profile, etc.) remain unchanged...

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
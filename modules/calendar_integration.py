import discord
from discord.ext import commands
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz
import asyncio
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io

class CalendarIntegration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.service = self.get_calendar_service()
        self.timezone = pytz.timezone('America/El_Paso')

    def get_calendar_service(self):
        creds = Credentials.from_service_account_file('service_account.json', scopes=['https://www.googleapis.com/auth/calendar.readonly'])
        return build('calendar', 'v3', credentials=creds)

    @commands.command()
    async def update_calendar(self, ctx):
        calendar_view_channel = discord.utils.get(ctx.guild.text_channels, name="calendar-view")
        if not calendar_view_channel:
            await ctx.send("Calendar view channel not found. Please contact an administrator.")
            return

        await calendar_view_channel.purge()

        now = datetime.utcnow().isoformat() + 'Z'
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=10, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            await calendar_view_channel.send('No upcoming events found.')
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                embed = discord.Embed(title=event['summary'], description=event.get('description', 'No description'), color=discord.Color.blue())
                embed.add_field(name="Start", value=start, inline=True)
                embed.add_field(name="End", value=end, inline=True)
                await calendar_view_channel.send(embed=embed)

        await ctx.send("Calendar view updated successfully.")

    @commands.command()
    async def visual_calendar(self, ctx):
        now = datetime.now(self.timezone)
        end = now + timedelta(days=30)
        events_result = self.service.events().list(calendarId='primary', timeMin=now.isoformat(),
                                                   timeMax=end.isoformat(), singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_title("Upcoming Events (Next 30 Days)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Events")

        dates = [datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date'))) for event in events]
        labels = [event['summary'] for event in events]

        ax.plot(dates, range(len(dates)), 'ro')
        for i, (date, label) in enumerate(zip(dates, labels)):
            ax.annotate(label, (date, i), xytext=(5, 5), textcoords='offset points')

        ax.xaxis.set_major_locator(mdates.WeekdayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        await ctx.send(file=discord.File(buf, 'calendar.png'))

    @commands.Cog.listener()
    async def on_ready(self):
        self.bg_task = self.bot.loop.create_task(self.background_calendar_update())

    async def background_calendar_update(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            for guild in self.bot.guilds:
                calendar_view_channel = discord.utils.get(guild.text_channels, name="calendar-view")
                if calendar_view_channel:
                    ctx = await self.bot.get_context(await calendar_view_channel.fetch_message(calendar_view_channel.last_message_id))
                    await self.update_calendar(ctx)
            await asyncio.sleep(3600)  # Update every hour

async def setup(bot):
    await bot.add_cog(CalendarIntegration(bot))
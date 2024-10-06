import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

class Onboarding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pending_soldiers = {}  # Store soldiers who haven't completed onboarding
        self.bot.loop.create_task(self.check_pending_soldiers())

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.initiate_onboarding(member)

    async def initiate_onboarding(self, member):
        self.pending_soldiers[member.id] = datetime.now()
        await member.send("Welcome to the Unit, recruit. You've got 2 minutes to set your nickname to your Rank and Last Name (e.g., PVT Smith). Failure to comply will result in immediate removal. Do you understand?")
        
        def check(m):
            return m.author == member and m.guild is None
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=120.0)
            if msg.content.lower() in ['yes', 'understood', 'roger', 'affirmative']:
                await self.prompt_nickname(member)
            else:
                await member.send("Failure to acknowledge. You're out, recruit.")
                await member.kick(reason="Failed to acknowledge onboarding instructions")
        except asyncio.TimeoutError:
            await member.send("Time's up, recruit. You're out.")
            await member.kick(reason="Failed to respond to onboarding instructions")

    async def prompt_nickname(self, member):
        await member.send("Set your nickname now, soldier. Format: RANK LASTNAME. You have 2 minutes.")
        
        def check(before, after):
            return before.id == member.id and after.nick is not None
        
        try:
            before, after = await self.bot.wait_for('member_update', check=check, timeout=120.0)
            if self.validate_nickname(after.nick):
                await self.assign_soldier_role(after)
            else:
                await member.send("Invalid nickname format. You're out, recruit.")
                await member.kick(reason="Failed to set proper nickname")
        except asyncio.TimeoutError:
            await member.send("Time's up, recruit. You're out.")
            await member.kick(reason="Failed to set nickname in time")

    def validate_nickname(self, nickname):
        valid_ranks = ['PVT', 'PFC', 'SPC', 'CPL', 'SGT', 'SSG', 'SFC', 'MSG', '1SG', 'SGM', 'CSM']
        parts = nickname.split()
        return len(parts) == 2 and parts[0] in valid_ranks and parts[1].isalpha()

    async def assign_soldier_role(self, member):
        role = discord.utils.get(member.guild.roles, name="Soldier")
        await member.add_roles(role)
        del self.pending_soldiers[member.id]
        await self.send_welcome_message(member)

    async def send_welcome_message(self, member):
        welcome_msg = f"""Welcome to the Unit, {member.nick}. You've got a lot to prove, and there's no time to waste. Here's what you need to know:

1. Check out #orders-channel for ongoing events and missions.
2. Head over to #pt-hall if you think you've got what it takes to keep up.
3. Need help or want to prove yourself? #questions-and-challenges is where you can ask or get assigned tasks.

Complete this tour for some starter XP. Now move it, soldier!"""
        
        await member.send(welcome_msg)
        await self.start_orientation_tour(member)

    async def start_orientation_tour(self, member):
        channels = ['orders-channel', 'pt-hall', 'questions-and-challenges', 'meme-central']
        for channel_name in channels:
            channel = discord.utils.get(member.guild.channels, name=channel_name)
            if channel:
                await channel.send(f"{member.mention}, report in by saying 'Present!'")
                
                def check(m):
                    return m.author == member and m.content.lower() == 'present!' and m.channel == channel
                
                try:
                    await self.bot.wait_for('message', check=check, timeout=300.0)
                    await channel.send(f"Good job, {member.nick}. Move on to the next objective.")
                except asyncio.TimeoutError:
                    await channel.send(f"{member.nick} couldn't keep up. Tour failed.")
                    return

        await self.complete_orientation(member)

    async def complete_orientation(self, member):
        xp_reward = 100  # Set the XP reward for completing orientation
        # Add XP to the member's account (implement this based on your XP system)
        await member.send(f"""Congratulations, you've completed your orientation and earned {xp_reward} XP. 
Now stop browsing and get involved. Check out #pt-hall, start logging your workouts, or visit #meme-central and prove you're not completely useless.""")

    @commands.command()
    @commands.has_role("NCO")
    async def requestNCO(self, ctx):
        if "Soldier" in [role.name for role in ctx.author.roles]:
            nco_channel = discord.utils.get(ctx.guild.channels, name="nco-approvals")
            if nco_channel:
                message = await nco_channel.send(f"{ctx.author.mention} has requested the NCO role. React with 👍 to approve or 👎 to deny.")
                await message.add_reaction("👍")
                await message.add_reaction("👎")

                def check(reaction, user):
                    return user.get_role("NCO") is not None and str(reaction.emoji) in ["👍", "👎"]

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=86400.0, check=check)
                    if str(reaction.emoji) == "👍":
                        nco_role = discord.utils.get(ctx.guild.roles, name="NCO")
                        await ctx.author.add_roles(nco_role)
                        await ctx.author.send("Congratulations, soldier. You've been promoted to NCO. Don't screw it up.")
                    else:
                        await ctx.author.send("NCO request denied. Shape up and try again when you've earned it.")
                except asyncio.TimeoutError:
                    await ctx.author.send("Your NCO request has timed out. Try again later.")
            else:
                await ctx.send("NCO approval channel not found. Contact an administrator.")
        else:
            await ctx.send("You need to be a Soldier to request NCO status. Nice try, boot.")

    async def check_pending_soldiers(self):
        while not self.bot.is_closed():
            now = datetime.now()
            for member_id, join_time in list(self.pending_soldiers.items()):
                member = self.bot.get_user(member_id)
                if member:
                    if now - join_time > timedelta(hours=1):
                        await member.send("Reminder: You've got until 1800 to set your nickname and receive your role. If you're too slow for that, this might not be the place for you.")
                    elif now - join_time > timedelta(hours=48):
                        await member.send("Clearly, you're not serious. Consider this your marching orders—get out.")
                        guild = member.guild
                        await guild.kick(member, reason="Failed to complete onboarding in 48 hours")
                        del self.pending_soldiers[member_id]
            await asyncio.sleep(3600)  # Check every hour

async def setup(bot):
    await bot.add_cog(Onboarding(bot))
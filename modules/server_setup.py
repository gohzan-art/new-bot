import discord
from discord.ext import commands

async def setup_server_layout(ctx, bot):
    guild = ctx.guild
    
    # Delete all existing channels and categories
    for channel in guild.channels:
        await channel.delete()
    
    # Create categories and channels
    categories = {
        "📢 Welcome & Onboarding": [
            "welcome", "rules-and-info", "roles-and-titles", "faq", "readme"
        ],
        "🶂️ Work Stuff (Operations)": [
            "announcements", "training-schedule", "pt-schedule", "pt-scores", "missions-and-tasks", "appointments", "ai-chat"
        ],
        "🏰 Soldier Resources": [
            "blank-forms", "tms", "ltt-conops", "archive-examples", "command-orders"
        ],
        "🕹️ Team Operations": [
            "scouts-chat", "infantry-chat", "hangout-chat"
        ],
        "💬 General Engagement (Social)": [
            "general", "meme-warfare", "gaming-squad", "youtube", "ai", "meme-generator-and-ranking", "fun-challenges"
        ],
        "📈 Leaderboards & Logs": [
            "fitness-leaderboard", "acft-leaderboard", "gaming-leaderboard", "weapons-qualification-leaderboard", "music-leaderboard", "meme-leaderboard"
        ],
        "📚 Resources and Links": [
            "weekend-adventure-suggestions", "guides-and-documents", "army-links", "external-resources", "si-and-property"
        ],
        "📝 Task Creation and Updates": [
            "task-management"
        ],
        "🎖️ NCO Hideout (NCO/Admin Only)": [
            "counseling-logs", "absence-logs", "soldier-info-database"
        ],
        "📝 Daily/Weekly Reports & Notes": [
            "notes", "notes-output"
        ],
        "📅 Calendar": [
            "calendar-view", "calendar-commands"
        ],
        "🏆 XP and Leveling System": [
            "xp-announcements", "level-up-celebrations", "leaderboard-updates"
        ]
    }
    
    for category_name, channels in categories.items():
        category = await guild.create_category(category_name)
        for channel_name in channels:
            if category_name == "🎖️ NCO Hideout (NCO/Admin Only)":
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.get_role(bot.config.NCO_ROLE_ID): discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                await category.create_text_channel(channel_name, overwrites=overwrites)
            else:
                await category.create_text_channel(channel_name)
    
    # Create voice channels
    team_ops_category = discord.utils.get(guild.categories, name="🕹️ Team Operations")
    await team_ops_category.create_voice_channel("Scouts Voice Channel")
    await team_ops_category.create_voice_channel("Infantry Voice Channel")
    await team_ops_category.create_voice_channel("Hangout Voice Channel")
    
    # Create NCO voice chat
    nco_category = discord.utils.get(guild.categories, name="🎖️ NCO Hideout (NCO/Admin Only)")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(connect=False),
        guild.get_role(bot.config.NCO_ROLE_ID): discord.PermissionOverwrite(connect=True)
    }
    await nco_category.create_voice_channel("NCO Voice Chat", overwrites=overwrites)
    
    await ctx.send("Server layout has been set up successfully!")

    # Set up team themes
    await setup_team_themes(guild)

async def setup_team_themes(guild):
    team_themes = {
        "Scouts": {
            "color": discord.Color.from_rgb(34, 139, 34),  # Forest Green
            "icon": "assets/images/team_icons/scouts_icon.png",
            "banner": "assets/images/team_banners/scouts_banner.png"
        },
        "Infantry": {
            "color": discord.Color.from_rgb(0, 0, 128),  # Navy Blue
            "icon": "assets/images/team_icons/infantry_icon.png",
            "banner": "assets/images/team_banners/infantry_banner.png"
        },
        "Hangout": {
            "color": discord.Color.from_rgb(255, 165, 0),  # Warm Orange
            "icon": "assets/images/team_icons/hangout_icon.png",
            "banner": "assets/images/team_banners/hangout_banner.png"
        }
    }

    for team, theme in team_themes.items():
        role = await guild.create_role(name=team, color=theme["color"])
        channel = discord.utils.get(guild.text_channels, name=f"{team.lower()}-chat")
        if channel:
            await channel.edit(topic=f"{team} Team Channel", overwrites={
                guild.default_role: discord.PermissionOverwrite(read_messages=True),
                role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            })
            await channel.send(file=discord.File(theme["banner"]))

async def setup(bot):
    bot.add_command(setup_server_layout)
# Add this import at the top of the file
from modules.bot_commands import BotCommands

# Add this line in the on_ready event
await bot.add_cog(BotCommands(bot))
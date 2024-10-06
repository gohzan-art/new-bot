import discord
import asyncio

async def create_dynamic_message(ctx, title, description, fields):
    embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
    
    for name, value in fields.items():
        embed.add_field(name=name, value=value, inline=False)
    
    message = await ctx.send(embed=embed)
    
    # Add reactions for interaction
    reactions = ['👍', '👎', '❓']
    for reaction in reactions:
        await message.add_reaction(reaction)
    
    # Update the message periodically
    asyncio.create_task(update_message_periodically(message, embed))

async def update_message_periodically(message, embed):
    while True:
        await asyncio.sleep(60)  # Update every minute
        embed.set_field_at(0, name="Last Updated", value=f"<t:{int(discord.utils.utcnow().timestamp())}:R>", inline=False)
        await message.edit(embed=embed)

@bot.command(name='dynamic')
async def dynamic(ctx):
    title = "Dynamic Message Example"
    description = "This message will update periodically and allows for reactions!"
    fields = {
        "Field 1": "Some static content",
        "Field 2": "More static content",
        "Last Updated": "Just now"
    }
    await create_dynamic_message(ctx, title, description, fields)
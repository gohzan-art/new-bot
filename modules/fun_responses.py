import discord
import random

async def fun_response(message):
    content = message.content.lower()
    
    if "attention" in content:
        await message.channel.send("**PLATOON, ATTEN-TION!** :saluting_face:")
    
    if "at ease" in content:
        await message.channel.send("At ease, carry on. :relieved:")
    
    if "drop and give me" in content:
        number = ''.join(filter(str.isdigit, content))
        if number:
            await message.channel.send(f"Aye aye! {number} pushups coming right up! :muscle:")
        else:
            await message.channel.send("How many, Drill Sergeant? :sweat_smile:")
    
    if "chow time" in content:
        meals = ["MREs", "mystery meat", "powdered eggs", "lukewarm coffee"]
        await message.channel.send(f"Grab your trays! Today's special is {random.choice(meals)}. :fork_and_knife:")
    
    if "sitrep" in content:
        situations = ["All quiet on the western front", "SNAFU", "TARFU", "FUBAR"]
        await message.channel.send(f"SITREP: {random.choice(situations)}, sir! :saluting_face:")

# Add this to your on_message event handler
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await fun_response(message)
    await bot.process_commands(message)
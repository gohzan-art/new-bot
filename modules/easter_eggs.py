import discord
import random

async def trigger_easter_egg(message):
    content = message.content.lower()
    
    if "hooah" in content:
        await message.channel.send("Hooah! :muscle:")
    
    if "airborne" in content:
        await message.channel.send("All the way! :parachute:")
    
    if "roger that" in content:
        responses = [
            "Lima Charlie!",
            "Solid copy!",
            "10-4, good buddy!",
            "Affirmative, ghost rider!",
        ]
        await message.channel.send(random.choice(responses))
    
    if "pt" in content and ("sucks" in content or "hate" in content):
        await message.channel.send("Pain is weakness leaving the body, soldier! :sweat_drops:")
    
    if "mre" in content:
        mre_jokes = [
            "Meals Refusing to Exit",
            "Meals Rejected by Everyone",
            "Meals Rarely Edible",
            "Maybe Rotten Eggs",
        ]
        await message.channel.send(f"Ah, MREs... also known as {random.choice(mre_jokes)} :nauseated_face:")
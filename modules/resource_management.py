async def pin_si_property_link(channel, link):
    message = await channel.send(f"SI and Property Accountability Spreadsheet: {link}")
    await message.pin()
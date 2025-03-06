import os
import discord
from dotenv import load_dotenv
from gcsa.google_calendar import GoogleCalendar

load_dotenv() # load all the variables from the .env file

gc = GoogleCalendar('ce2db4bd90ceeb1456a64923ae8d74801ca09077c5cb388bbb821449b9c362d8@group.calendar.google.com')
for event in gc:
    print(event)


bot = discord.Bot()

@bot.event
async def on_ready():
    await bot.sync_commands()

    print(f"{bot.user} is ready and online!")

# Load cogs without having to hardcode them all
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.getenv('DISCORD_TOKEN')) # run the bot with the token
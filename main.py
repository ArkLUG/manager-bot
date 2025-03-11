import os
import discord
from dotenv import dotenv_values
from gcsa.google_calendar import GoogleCalendar
import asyncio
from discord.ext import commands

class Manager:
	def __init__(self):
		self.config = dotenv_values(".env")
		self.bot = discord.Bot(intents=discord.Intents.all(), guild=[self.config['DISCORD_GUILD']])
		# self.database = Database()
		
		self.calendar = GoogleCalendar(self.config['GOOGLE_CALENDAR_ID'], credentials_path='config/credentials.json')


		setattr(self.bot, 'manager', self)
		asyncio.run(self.setup())

	async def setup(self):
		# Load all the cogs
		for filename in os.listdir('./cogs'):
			if filename.endswith('.py'):
				self.bot.load_extension(f'cogs.{filename[:-3]}')

		@self.bot.event
		async def on_ready(once=True):
			await self.bot.sync_commands()
			print(f"{self.bot.user} is ready and online!")

	def run(self):
		self.bot.run(self.config['DISCORD_TOKEN'])

def main():
	manager = Manager()
	manager.run()

if __name__ == "__main__":
	main()

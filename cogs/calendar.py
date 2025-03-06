import discord
from discord.commands import slash_command
from discord.ext import commands

class Calendar(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{type(self).__name__} Cog is loaded!")

	@slash_command(name="calendar", description="Shows the calendar")
	async def calendar(self, ctx):
		events = self.bot.manager.calendar.get_events()
		embed = discord.Embed(title="Calendar")
		for event in events:
			embed.add_field(
				name=event.summary,
				value=f"Start: {event.start}\nEnd: {event.end}",
				inline=False
			)
		await ctx.respond(embed=embed)

def setup(bot):
	bot.add_cog(Calendar(bot))
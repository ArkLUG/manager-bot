import discord
from discord.commands import slash_command
from discord.ext import commands
import datetime

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

	async def events_autocomplete(self: discord.AutocompleteContext):
		events = self.bot.manager.calendar.get_events()
		return [str(f"{event.summary} | {event.start.date() if isinstance(event.start, datetime.datetime) else event.start}") for event in events]

	@slash_command(name="event", description="Shows a specific event")
	async def event(self, ctx, event_name: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(events_autocomplete))):
		summary, date = "", ""
		try:
			summary, date = event_name.split(" | ")
		except ValueError:
			await ctx.respond("Event not found")
			return
		this_event = None
		events = self.bot.manager.calendar.get_events()
		for event in events:
			if event.summary == summary:
				if isinstance(event.start, datetime.datetime):
					if event.start.date() == datetime.datetime.strptime(date, "%Y-%m-%d").date():
						this_event = event
						break
				else:
					if event.start == datetime.datetime.strptime(date, "%Y-%m-%d").date():
						this_event = event
						break
		if this_event is None:
			await ctx.respond("Event not found")
			return
		embed = discord.Embed(title=event.summary)
		embed.add_field( name="Start", value=event.start, inline=False)
		embed.add_field(name="End", value=event.end, inline=False)
		await ctx.respond(embed=embed)
	
	@slash_command(name="link_event", description="Links a discord channel to a calendar event")
	async def link_event(self, ctx, event_name: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(events_autocomplete))):
		summary, date = "", ""
		try:
			summary, date = event_name.split(" | ")
		except ValueError:
			await ctx.respond("Event not found")
			return
		this_event = None
		events = self.bot.manager.calendar.get_events()
		for event in events:
			if event.summary == summary:
				if isinstance(event.start, datetime.datetime):
					if event.start.date() == datetime.datetime.strptime(date, "%Y-%m-%d").date():
						this_event = event
				else:
					if event.start == datetime.datetime.strptime(date, "%Y-%m-%d").date():
						this_event = event
		if this_event is None:
			await ctx.respond("Event not found")
			return
		await ctx.respond(f"Event {event.summary} has been linked to nothing cause this doesn't work yet")

def setup(bot):
	bot.add_cog(Calendar(bot))

import discord
from discord.commands import slash_command
from discord.ext import commands
import datetime
from beautiful_date import Apr, hours
import gcsa
import os

class CalendarManagement(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener(once=True)
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
		embed.add_field(name="Description", value=event.description
			if event.description is not None else "No description", inline=False)
		embed.add_field(name="Location", value=event.location
			if event.location is not None else "No location", inline=False)
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

	@slash_command(name="create_event", description="Creates a new event")
	async def create_event(self, ctx, summary: str, start: str, end: str, description: str = None, location: str = None):
		# convert to datetime
		start_time = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M")
		end_time = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M")

		# Create thread in Event Planning forum
		if not self.bot.manager.config['EVENT_PLANNING_CHANNEL']:
			await ctx.respond("Event Planning forum not set! Please set it in the .env file")
			return
		forum = self.bot.get_channel(int(self.bot.manager.config['EVENT_PLANNING_CHANNEL']))
		if not forum:
			await ctx.respond("Event Planning forum not found")
			return
		else:
			await forum.create_thread(name=summary, content=description)

		# Send Announcement in Event Announcements channel
		if not self.bot.manager.config['EVENT_ANNOUNCEMENT_CHANNEL']:
			await ctx.respond("Event Announcements channel not set! Please set it in the .env file")
			return
		channel = self.bot.get_channel(int(self.bot.manager.config['EVENT_ANNOUNCEMENT_CHANNEL']))
		if not channel:
			await ctx.respond("Event Announcements channel not found")
			return
		else:
			announcement = discord.Embed(title=summary)
			announcement.add_field(name="Start", value=start_time)
			announcement.add_field(name="End", value=end_time)
			announcement.add_field(name="Description", value=description)
			announcement.add_field(name="Location", value=location)
			await channel.send(embed=announcement)

		# Create Scheduled event in discord
		try:
			await ctx.guild.create_scheduled_event(
				name=summary,
				start_time=start_time,
				end_time=end_time,
				description=description,
				location=location,
				privacy_level=discord.ScheduledEventPrivacyLevel.guild_only
			)
		except discord.HTTPException as e:
			await ctx.respond(f"Failed to create scheduled event: {e}")
			return

		# add it to the google calendar
		new_event = gcsa.event.Event(
			summary,
			start=start_time,
			end=end_time,
			description=description,
			location=location
		)
		self.bot.manager.calendar.add_event(new_event)


		await ctx.respond(f"Event {summary} has been created")

def setup(bot):
	bot.add_cog(CalendarManagement(bot))

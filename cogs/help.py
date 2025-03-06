import discord
from discord.commands import slash_command
from discord.ext import commands


class Help(commands.Cog):

	def __init__(self,bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{type(self).__name__} Cog is loaded!")

	@slash_command(name="help", description="Display Studlybot's commands")
	async def help(self, ctx: discord.ApplicationContext, command: discord.Option(discord.SlashCommandOptionType.string, "command", required=False, default=None)):
		help_embed = discord.Embed(title="Studly commands:")
		command_names_list = [x.name for x in self.bot.commands]
		if not command:
			help_embed.add_field(
				name="List of supported commands:",
				value="\n".join([str(i+1)+". "+x.name for i,x in enumerate(self.bot.commands)]),
				inline=False
			)
			help_embed.add_field(
			name="Details",
			value="Type `/help <command name>` for more details about each command.",
			inline=False
		)

		elif command in command_names_list:
			help_embed.add_field(
			name=command,
			value=self.bot.get_command(command).description
		)
		else:
			help_embed.add_field(
			name="Error",
			value="Not a valid command"
		)
		await ctx.respond(embed=help_embed)

def setup(bot):
	bot.add_cog(Help(bot))
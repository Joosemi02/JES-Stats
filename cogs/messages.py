import nextcord as discord
from nextcord.ext import commands
from bot import get_embed


class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name}: The messages extension was loaded successfully.")

    @commands.command()
    async def help(self, ctx: commands.Context, command: str = None):
        if not command:
            embed = get_embed(
                title="__**Stats Bot help**__",
                description="You can get info about Just an Earth server witht this bot.\n\n**Command list:**\n\n`/online, /town, /resident, /nation, /townless, /status, /onlinemayors, /townonline, /ruins`\n\nDo `/help` `command` to learn how to use one of these commands or `/help` `messages` to learn about message commands.",
            )
            return await ctx.send(embed=embed)
        command = command.lower()
        if command == "messages":
            embed = get_embed(tite="__**Message commands**__")
            for cmd in self.bot.commands:
                if cmd.brief == "messages":
                    embed.add_field(name=cmd.name, value=cmd.description)
            await ctx.send(embed=embed)
        slash_commands = {
            "online": "Use this command to get a list of online players.",
            "town": "Use this command to view a town's info.",
            "resident": "Use this command to get a player's info. Make sure to type the '_' if it's a bedrock player.",
            "nation": "Use this command to find info about a specific nation.",
            "townless": "Use this command to get the name of online players that aren't in a town.",
            "status": "Use this command to get info about the server's network.",
            "onlinemayors": "Use this command to get a list of the mayors that are online in the server.",
            "townonline": "Use this command to view who is online in a town.",
            "ruins": "Use this command to get the names.",
        }
        if command in slash_commands:
            embed = get_embed(
                title=f"__**{command.capitalize()} help**__",
                description=slash_commands[command],
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def guilds(self, ctx: commands.Context):
        li = "\n".join(g.name for g in self.bot.guilds)
        embed = get_embed(description=li)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Messages(bot))

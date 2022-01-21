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
    async def help(self, ctx: commands.Context, command: str =None):
        if not command:
            embed = await get_embed(
                title="__**Stats Bot help**__",
                description="You can get info about Just an Earth server witht this bot.\n\n**Command list:**\n\n`/online, /town, /resident, /nation, /townless, /status, /onlinemayors, /townonline, /ruins`\n\nDo `/help` `command` to learn how to use one of these commands or `/help` `messages` to learn about message commands.",
            )
            return await ctx.send(embed=embed)
        if command == "messages":
            print(1)
        if command in {
            "online",
            "town",
            "resident",
            "nation",
            "townless",
            "status",
            "onlinemayors",
            "townonline",
            "ruins",
        }:
            for c in self.bot.commands:
                if c.qualified_name == command:
                    print(c.description)
    
    @commands.command()
    async def guilds(self, ctx: commands.Context):
        await ctx.send(f"{'\n'.join(self.bot.guilds)}")

def setup(bot):
    bot.add_cog(Messages(bot))
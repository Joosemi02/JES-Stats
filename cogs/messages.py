import nextcord as discord
from nextcord.ext import commands
from nextcord.interactions import Interaction
from nextcord import slash_command, SlashOption

from bot import get_embed


class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name}: The messages extension was loaded successfully.")

    @slash_command(name="help", description="Get bot help.", guild_ids=[929264724854571058])
    async def help(
        self,
        i: Interaction,
        command: str = SlashOption(
            name="command",
            required=False,
            choices={
                "online": "online",
                "town": "town",
                "resident": "resident",
                "nation": "nation",
                "townless": "townless",
                "status": "status",
                "onlinemayors": "onlinemayors",
                "townonline": "townonline",
                "ruins": "ruins",
                "messages": "messages"
            },
        ),
    ):
        if not command:
            embed = await get_embed(
                i,
                title="__**Stats Bot help**__",
                description="You can get info about Just an Earth server witht this bot.\n\nCommand list:\n\n`/online, /town, /resident, /nation, /townless, /status, /onlinemayors, /townonline, /ruins`\n\nDo `/help` `command` to learn how to use one of these commands or `/help` `messages` to learn about message commands.",
            )
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
                    print("abc")

def setup(bot):
    bot.add_cog(Messages(bot))
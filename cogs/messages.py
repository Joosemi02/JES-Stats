import nextcord as discord
from nextcord.ext import commands
from bot import get_embed


class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name}: The messages extension was loaded successfully.")

    async def send_messages(self, ctx):
        li = [cmd.name for cmd in self.bot.commands if cmd.brief == "messages"]
        embed = get_embed(title="__**Message commands**__", description="\n".join(li))
        await ctx.send(embed=embed)

    @discord.slash_command(
        name="messages", description="Get info about message commands."
    )
    async def messages(self, i):
        await self.send_messages(i)

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
            await self.send_messages(ctx)
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

    @commands.command(brief="messages")
    async def brewery(self, ctx):
        await ctx.send("https://github.com/DieReicheErethons/Brewery/wiki/Homepage")

    @commands.command(brief="messages")
    async def ip(self, ctx):
        embed = get_embed(
            title="Just an Earth Server",
            description="Name: JES (Any name will work)\nIP: jes.earth\nBedrock Port: 19132 (default)\n\n- How to join in PC, mobile, PS4/5, Xbox, Nintendo Switch: https://discord.gg/g8VBhuDqGC",
        )
        await ctx.send(embed=embed)

    @commands.command(brief="messages")
    async def map(self, ctx):
        embed = get_embed(
            description="Earth1: http://map.jes.earth/\nEarth2: http://map2.jes.earth/\nSMP: http://smp.jes.earth/",
        )
        await ctx.send(embed=embed)

    @commands.command(brief="messages")
    async def marriage(self, ctx):
        embed = get_embed(
            title="➡️Unofficial Marriage Server",
            description="https://discord.gg/7gyvNDAEPJ",
        )
        await ctx.send(embed=embed)

    @commands.command(brief="messages")
    async def mcmmo(self, ctx):
        embed = get_embed(
            description="https://mcmmo.org/wiki/Main_Page",
        )
        await ctx.send(embed=embed)

    @commands.command(brief="messages")
    async def news(self, ctx):
        embed = get_embed(
            title="UNOFFICIAL JES NEWS",
            description="https://discord.gg/9dC2tE9JQs\nhttps://discord.gg/urz3ZUdm",
        )
        await ctx.send(embed=embed)

    @commands.command(brief="messages")
    async def oneblock(self, ctx):
        embed = get_embed(
            title="Oneblock commands",
            description="(do /is help in game for more)\n/is\n/is go\n/is level\n/is count\n/is phases\n/is spawn\n/is warp\n/is reset\n/is info (player)\n/is setname (name)\n/is language (language)\n/is ban\n/is unban\n/is banlist\n/is expel\n/is team\n/is team invite (player)\n/is team accept",
        )
        await ctx.send(embed=embed)

    @commands.command(brief="messages")
    async def reputation(self, ctx):
        embed = get_embed(
            title="Reputation",
            description="**All Tags:**\nNEW -> USER -> KNOWN -> TRUSTED\n\n**User requirements:**\n- 5 days of /playtime or a donator rank.\n\nJoin https://discord.gg/a4VuZkk3mr to request your [USER] tag.",
        )
        await ctx.send(embed=embed)

    @commands.command(
        brief="messages", aliases=["qs", "shop", "shops", "cs", "quickshop"]
    )
    async def chestshop(self, ctx):
        await ctx.send("https://www.youtube.com/watch?v=o7hgoNCDWQk")

    @commands.command(brief="messages")
    async def rules(self, ctx):
        await ctx.send("http://rules.jes.earth/")

    @commands.command(brief="messages")
    async def spawners(self, ctx):
        await ctx.send(
            "Elder Guardian/Guardian: disabled\nZombie Villager: disabled\nDonkey: spawned only by egg\nMule: spawned only by egg\nCreeper: only by egg\nSkeleton: only by egg\nSpider: only by egg\nZombie: only by egg\nSlime: doesn't work/disabled\nEnderman: only by egg\nCave spider: only by egg\nBlaze: spawners\nPig: spawners\nSheep: spawners\nCow: spawners\nChickens: spawners\nWolf: enabled\nHorse: enabled\nRabbit: enabled\nParrot: disabled"
        )

    @commands.command(brief="messages")
    async def siegewar(self, ctx):
        embed = get_embed(
            title="What is SiegeWar?",
            description="- ⚔️ **Sieges**: Wars are conducted by means of sieges. A siege occurs when a nation attacks a town.\n- 🤖 **Automatic**: Sieges are started by players and automatically managed by the plugin. Daily staff management of war is not required.\n- 🏙️ **Minimally Destructive**: During sieges, towns cannot be damaged or stolen from.\n- 🚶 **Slow Paced**: Sieges last 3 days, giving defenders a chance to respond to attacks, and also making the system friendly to casual players.\n- 🗺️ **Geopolitical**: The whole server is involved, with no opt-outs. Nations and towns always have a Peaceful option, where they can become immune to attack, but vulnerable to peaceful occupation.\n- ♟️ **Strategic**: The system has many strategic elements (e.g. deciding when/where/who to attack, organizing army composition/logisitics/movement, and diplomacy/occupation/peacefulness etc). This can be great for thoughful/mature playerbases, but for servers which require more simplistic PVP contests, alternative war systems should be considered.\n- 🍎 **Non-Toxic**: If you install the recommended TownyResources plugin, this can help to focus wars on the strategic acquisition of material resources, rather than the toxic settlement of personal grudges.\n\nhttps://github.com/TownyAdvanced/SiegeWar",
        )
        await ctx.send(embed=embed)

    @commands.command(brief="messages")
    async def support(self, ctx):
        await ctx.send("https://discord.gg/TUugwRrRmJ")

    @commands.command(brief="messages")
    async def towny(self, ctx):
        await ctx.send("https://github.com/TownyAdvanced/Towny/wiki/Towny-Commands")

    @commands.command(brief="messages")
    async def vehicles(self, ctx):
        await ctx.send("https://vehicles.gitbook.io/wiki/faq")

    @commands.command(brief="messages", aliases=["jestats"])
    async def add(self, ctx):
        await ctx.send(
            "https://discord.com/api/oauth2/authorize?client_id=931130747841048638&permissions=274877908992&scope=applications.commands%20bot"
        )

    @commands.command(brief="messages", aliases=["tr"])
    async def townyresources(self, ctx):
        embed = get_embed(
            title="Towny Resources",
            description="- TownyResources adds value to towns, by giving each one a unique set of automatically-produced resources which can be collected by players (e.g. Emeralds, Coal, Oak Log, Wheat etc.).\n\n**BENEFITS:**\n\n- :cityscape: Encourages Town Building.\n- :united_nations: Encourages Nation Building.\n- :moneybag: Encourages Trading.\n- :zzz: Reduces Grind.\n- :woman_fairy: Assists Roleplaying.\n- :crossed_swords: Improves the SiegeWar experience, by adding a new non-toxic reason for war: Capturing Resources.\n\nUser Guide (Read More): https://github.com/TownyAdvanced/TownyResources#readme",
        )
        await ctx.send(embed=embed)

    @commands.command(brief="messages")
    async def ores(self, ctx: commands.Context):
        d_embed = discord.Embed(
            title="Diamond Ore Distribution", color=discord.Color.blue()
        )
        d_embed.set_image(
            url="https://images-ext-1.discordapp.net/external/peMCFOgvgO1lEz7UZvhtAm7XVJQPrhrtBrrxzGWNH8Y/https/cdn-longterm.mee6.xyz/plugins/commands/images/767803717549948940/eb46e4c6f24326a4a05f623dd582e602f223f768b0299a021cdfe17435c2a0f1.jpeg"
        )
        g_embed = discord.Embed(
            title="Gold Ore Distribution", color=discord.Color.blue()
        )
        g_embed.set_image(
            url="https://images-ext-2.discordapp.net/external/2XORysVW07j-fooscm7kPg_zmBE9w_gogkqd1vjj8a4/https/cdn-longterm.mee6.xyz/plugins/commands/images/767803717549948940/4ea2e0edf332f91c78fa81aa381dc050f2d09fd3e18dc1e761f7d79ed5cd0532.jpeg"
        )
        g_embed.set_footer(
            text="Coal, iron and other ores can be found anywhere in the map.",
            icon_url=self.bot.user.avatar.url,
        )
        await ctx.send(embeds=[d_embed, g_embed])


def setup(bot):
    bot.add_cog(Messages(bot))

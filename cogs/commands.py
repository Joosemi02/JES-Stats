import nextcord as discord, requests
from nextcord.ext import commands
from nextcord.enums import ButtonStyle
from nextcord.interactions import Interaction
from nextcord import slash_command
from bot import get_embed, is_server_online
from config import api_1, api_2, api_3, api_4, api_5, api_6, api_8


class PreviousButton(discord.ui.Button):
    def __init__(self, disabled):
        super().__init__(
            style=ButtonStyle.blurple,
            custom_id="paginator_previous",
            emoji="⏮️",
            disabled=disabled,
        )

    async def callback(self, i: Interaction):
        n_embed: discord.Embed = self.view.message.embeds[0]
        self.view.page -= 1
        n_embed.remove_field(4)
        n_embed.add_field(
            name=f"[{self.view.num}] Residents:",
            value="\n".join(self.view.split_list[self.view.page - 1]),
        )
        self.view.count.label = f"{self.view.page}/{self.view.total_pages}"
        self.view.previous.disabled = self.view.page == 1
        self.view.next.disabled = self.view.page == self.view.total_pages
        await i.response.edit_message(embed=n_embed, view=self.view)
        return await super().callback(i)


class NextButton(discord.ui.Button):
    def __init__(self, disabled):
        super().__init__(
            style=ButtonStyle.blurple,
            custom_id="paginator_next",
            emoji="⏩",
            disabled=disabled,
        )

    async def callback(self, i: Interaction):
        n_embed: discord.Embed = self.view.message.embeds[0]
        self.view.page += 1
        n_embed.remove_field(4)
        n_embed.add_field(
            name=f"[{self.view.num}] Residents:",
            value="\n".join(self.view.split_list[self.view.page - 1]),
        )
        self.view.count.label = f"{self.view.page}/{self.view.total_pages}"
        self.view.next.disabled = self.view.page == self.view.total_pages
        self.view.previous.disabled = self.view.page == 1
        await i.response.edit_message(embed=n_embed, view=self.view)
        return await super().callback(i)


class PageCountButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(
            style=ButtonStyle.blurple,
            custom_id="paginator_count",
            disabled=True,
            label=label,
        )


class Paginator(discord.ui.View):
    def __init__(self, bot, interaction, li, timeout=30):
        self.bot: commands.Bot = bot
        self.interaction: commands.Context = interaction
        self.num = len(li)
        self.split_list = [li[i : i + 10] for i in range(0, len(li), 10)]
        self.page = 1
        self.total_pages = len(self.split_list)
        p_disabled = self.page == 1
        n_disabled = self.page == self.total_pages
        super().__init__(timeout=timeout)
        self.previous = PreviousButton(p_disabled)
        self.add_item(self.previous)
        self.count = PageCountButton(f"{self.page}/{self.total_pages}")
        self.add_item(self.count)
        self.next = NextButton(n_disabled)
        self.add_item(self.next)

    async def interaction_check(self, i: Interaction) -> bool:
        i.user.id == self.interaction.user.id
        return await super().interaction_check(i)

    async def on_timeout(self) -> None:
        if not hasattr(self, "message"):
            return
        n_embed = self.message.embeds[0]
        n_embed.set_footer(text="The buttons to switch pages have timed out.")
        for child in self.children:
            child.disabled = True
        await self.message.edit(embed=n_embed, view=self)
        return await super().on_timeout()


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """async def online(self):
        if not self.arg2:
            if not await (player := find_linked(self.ctx.message.author)):
                return await self.ctx.send_help(self.ctx.command)
            resident = requests.get(f"{api_1}/{player}")
            self.arg2 = resident.json()["town"]
        res = requests.get(api_5)
        embed = await get_embed(
            self.ctx, title=f"Online Players in {self.arg2.lower()}"
        )
        li = [
            res.json()[i]["name"]
            for i in range(len(res.json()))
            if "town" in res.json()[i]
            and res.json()[i]["town"].lower() == self.arg2.lower()
        ]

        embed.add_field(name="Online: ", value=str(len(li)), inline=False)
        if li:
            embed.add_field(
                name="Names: ", value="```" + "\n".join(li) + "```", inline=False
            )
        await self.reslist.delete()
        await self.ctx.send(embed=embed)"""

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name}: The commands extension was loaded successfully.")

    @slash_command(
        name="town",
        description="Use this command to view a town's info.",
        guild_ids=[911944157625483264],
    )
    async def town(self, i: Interaction, town=None):
        if not town:
            return await i.send(
                "Please enter a town name in the `town` field.", ephemeral=True
            )
        res = requests.get(f"{api_1}/{town}")
        if res.json() == "That town does not exist!":
            return await i.send(
                embed=await get_embed(
                    i,
                    description="<a:crya:912762373591420989> This town doesn't exist...",
                    color=discord.Color.red(),
                )
            )

        await i.response.defer()
        embed = await get_embed(i, f"Town: {res.json()['name']}")
        embed.add_field(name="Mayor", value=res.json()["mayor"], inline=True)
        embed.add_field(name="Nation", value=res.json()["nation"], inline=True)
        embed.add_field(
            name="Dynmap",
            value=f"[{res.json()['x']},{res.json()['z']}](http://jes.enviromc.com:25568/#/?worldname=earth&mapname=flat&zoom=6&x={res.json()['x']}&y=64&z={res.json()['z']})",
            inline=False,
        )
        embed.add_field(
            name="Claims",
            value=f'{res.json()["area"]}/{len(res.json()["residents"] * 8)}',
            inline=False,
        )

        reslist: list = res.json()["residents"]
        view = Paginator(self.bot, i, reslist)
        embed.add_field(
            name=f"[{len(reslist)}] Residents: ",
            value="\n".join(view.split_list[0]),
            inline=False,
        )
        view.message = await i.followup.send(embed=embed, view=view)

    @commands.command(
        aliases=["resident", "residents"],
        usage="Usage: `{prefixcommand}` `(username)`.\nLeave `username` empty to view your /linked resident info.",
        description="Use this commands to get a player's info. Make sure to type the '_' if it's a bedrock player.",
    )
    async def res(self, ctx: commands.Context, res=None):
        if await is_server_online(ctx) != True:
            return

        wait_msg = await ctx.reply(
            embed=await get_embed(
                ctx=ctx,
                description="<a:happy_red:912452454669508618> Fetching resident data ...",
            )
        )

        embed = await get_embed(ctx, title=f"Resident: {res.json()['name']}")
        embed.add_field(name="Nation: ", value=str(res.json()["nation"]), inline=False)
        embed.add_field(name="Town: ", value=str(res.json()["town"]), inline=False)
        embed.add_field(name="Rank: ", value=str(res.json()["rank"]), inline=False)
        await wait_msg.delete()
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["nation", "nations"],
        usage="Usage: `{prefixcommand}` `(nation)`. Leave `nation` empty to view your /linked nation info.",
        description="Use this command to find info about a specific nation.",
    )
    async def n(self, ctx: commands.Context, arg=None):
        if await is_server_online(ctx) != True:
            return

        wait_msg = await ctx.reply(
            embed=await get_embed(
                ctx=ctx,
                description="<a:happy_red:912452454669508618> Fetching nation data ...",
            )
        )

        res = requests.get(f"{api_2}/{arg}")
        embed = await get_embed(ctx, title=f"Nation: {res.json()['name']}")
        embed.add_field(name="King: ", value=res.json()["king"], inline=True)
        embed.add_field(name="Capital: ", value=res.json()["capitalName"], inline=True)
        embed.add_field(name="Claims: ", value=str(res.json()["area"]), inline=False)
        embed.add_field(
            name="Towns: ", value=str(len(res.json()["towns"])), inline=False
        )
        embed.add_field(
            name="Population: ", value=str(len(res.json()["residents"])), inline=False
        )
        await wait_msg.delete()
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["notown"],
        usage="Usage: `prefixcommand`.",
        description="Use this command to get the anme of online players that aren't in a town.",
    )
    async def townless(self, ctx):
        if await is_server_online(ctx) != True:
            return

        wait_msg = await ctx.reply(
            embed=await get_embed(
                ctx=ctx,
                description="<a:happy_red:912452454669508618> Fetching resident data ...",
            )
        )

        res = requests.get(api_6)
        li = [res.json()[i]["name"] for i in range(len(res.json()))]
        if li:
            embed = await get_embed(ctx, title="Townless Players")
            embed.add_field(
                name="Names: ", value="```" + "\n".join(li) + "```", inline=False
            )
        else:
            embed = await get_embed(
                ctx,
                description="🚨 No townless players were found.",
                color=discord.Color.red(),
            )
        await wait_msg.delete()
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["server", "jestatus"],
        usage="Usage: `{prefixcommand}`.",
        description="Use this command to get info about the server's network",
    )
    async def status(self, ctx):
        wait_msg = await ctx.reply(
            embed=await get_embed(
                ctx=ctx,
                description="<a:happy_red:912452454669508618> Fetching network status ...",
            )
        )
        res = requests.get(api_4)
        embed = await get_embed(ctx, title="Network Status")
        embed.add_field(
            name="Towny: ", value=f'```{res.json()["towny"]}/110```', inline=False
        )

        embed.add_field(
            name="Network: ",
            value=f'```{res.json()["online"]}/110```',
            inline=False,
        )

        active = res.json()["serverOnline"]
        if active:
            embed.add_field(name="Server: ", value=":green_circle:", inline=False)
        else:
            embed.add_field(name="Server: ", value=":red_circle:", inline=False)
        await wait_msg.delete()
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["onlineplayer"],
        usage="Usage: `{prefixcommand}`.",
        description="Use this command to get a list of online players.",
    )
    async def online(self, ctx):
        if await is_server_online(ctx) != True:
            return

        wait_msg = await ctx.reply(
            embed=await get_embed(
                ctx=ctx,
                description="<a:happy_red:912452454669508618> Fetching resident data ...",
            )
        )

        res = requests.get(api_5)
        embed = await get_embed(ctx, title="Online Players")
        li = [res.json()[i]["name"] for i in range(len(res.json()))]
        embed.add_field(
            name="Names: ", value="```" + "\n".join(li) + "```", inline=False
        )
        await wait_msg.delete()
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["onlinemayors", "mayor", "omayors", "onlinem"],
        usage="Usage: `{prefixcommand}`.",
        description="Use this command to get a list of the mayors that are online in the server.",
    )
    async def mayors(self, ctx):
        if await is_server_online(ctx) != True:
            return

        wait_msg = await ctx.reply(
            embed=await get_embed(
                ctx=ctx,
                description="<a:happy_red:912452454669508618> Fetching mayor data ...",
            )
        )
        res = requests.get(api_5)
        embed = await get_embed(ctx, title="Online Mayors")
        li = [
            f"{res.json()[i]['name']}({res.json()[i]['town']})"
            for i in range(len(res.json()))
            if "rank" in res.json()[i] and res.json()[i]["rank"] == "Mayor"
        ]

        embed.add_field(
            name="Names: ", value="```" + "\n".join(li) + "```", inline=False
        )
        await wait_msg.delete()
        await ctx.send(embed=embed)

    @commands.command(
        usage="Usage: `{prefixcommand}` `town`.",
        description="Use this command to view who is online in a town. Leave `town` empty to view your /linked town's info.",
    )
    async def tonline(self, ctx: commands.Context, arg=None):
        if await is_server_online(ctx) != True:
            return

        wait_msg = await ctx.reply(
            embed=await get_embed(
                ctx=ctx,
                description="<a:happy_red:912452454669508618> Fetching resident data ...",
            )
        )

        res = requests.get(api_5)
        embed = await get_embed(ctx, title=f"Online Players in {arg}")
        li = [
            res.json()[i]["name"]
            for i in range(len(res.json()))
            if "town" in res.json()[i] and res.json()[i]["town"].lower() == arg.lower()
        ]

        embed.add_field(name="Online: ", value=str(len(li)), inline=False)
        if li:
            embed.add_field(
                name="Names: ", value="```" + "\n".join(li) + "```", inline=False
            )
        await wait_msg.delete()
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["ruined", "ruins", "ruin", "ruinedtown"],
        usage="Usage: `{prefixcommand}`.",
        description="Use this command to get the names",
    )
    async def ruinedtowns(self, ctx):
        if await is_server_online(ctx) != True:
            return

        wait_msg = await ctx.reply(
            embed=await get_embed(
                ctx=ctx,
                description="<a:happy_red:912452454669508618> Fetching town data ...",
            )
        )

        res = requests.get(api_1)
        embed = await get_embed(ctx, title="Ruined towns list")
        li = [
            res.json()[i]["name"]
            for i in range(len(res.json()))
            if len(res.json()[i]["residents"]) == 1
            and res.json()[i]["residents"][0][:3].lower() == "bot"
        ]

        if li:
            embed.add_field(
                name="Town Names: ",
                value="```" + "\n".join(li) + "```",
                inline=False,
            )
        await wait_msg.delete()
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["sieges", "sw", "swar", "war", "siegew", "battles"],
        usage="Usage: `{prefixcommand}` `(sieged town)`.\nLeave town empty to see a list of all sieged towns.",
        description="Use this command to get info about a siege happening at the moment or a list of all sieges.",
    )
    async def siege(self, ctx: commands.Context, arg=None):
        if await is_server_online(ctx) != True:
            return

        wait_msg = await ctx.reply(
            embed=await get_embed(
                ctx=ctx,
                description="<a:happy_red:912452454669508618> Fetching siege data ...",
            )
        )

        res = requests.get(api_8)
        if not arg:
            if len(res.json()) > 0:
                a = [res.json()[i]["name"] for i in range(len(res.json()))]
                embed = await get_embed(ctx, title="Sieged Towns: ")
                embed.add_field(
                    name="Town Names", value=f"```{', '.join(a)}```", inline=False
                )
            else:
                embed = await get_embed(
                    ctx,
                    description="🚨 No towns are being sieged at the moment.",
                    color=discord.Color.red(),
                )
            await wait_msg.delete()
            return await ctx.send(embed=embed)
        for i in range(len(res.json())):
            if res.json()[i]["name"].lower() == arg.lower():
                a = res.json()[i]
                embed = await get_embed(ctx, title="Sieged Town: " + a["name"])
                embed.add_field(name="Attacker", value=a["attacker"], inline=True)
                embed.add_field(name="Type", value=a["type"], inline=True)
                embed.add_field(
                    name="Dynmap",
                    value=f"[{a['x']},{a['z']}](http://jes.enviromc.com:25568/#/?worldname=earth&mapname=flat&zoom=9&x={a['x']}&y=64&z={a['z']})",
                    inline=False,
                )
                embed.add_field(name="Siege Balance", value=a["balance"], inline=False)
                if int(a["balance"]) > 0:
                    embed.add_field(
                        name="Current Winner", value="Attackers", inline=True
                    )
                else:
                    embed.add_field(
                        name="Current Winner", value="Defenders", inline=True
                    )
                embed.add_field(name="Time Left", value=a["time"], inline=False)
                embed.add_field(name="War Chest", value=a["chest"], inline=False)

                await wait_msg.delete()
                await ctx.send(embed=embed)
                return

        embed = await get_embed(
            ctx,
            description="<a:tnt:912834869845958686> This town doesn't exist or isn't besieged...",
            color=discord.Color.red(),
        )
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Commands(bot))

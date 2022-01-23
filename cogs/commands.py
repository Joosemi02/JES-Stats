import nextcord as discord, requests
from nextcord.ext import commands
from nextcord.enums import ButtonStyle
from nextcord.interactions import Interaction
from nextcord import slash_command
from bot import get_embed, is_server_online
from config import api_1, api_2, api_3, api_4, api_5, api_6


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
        if self.view.type == "town":
            n_embed.remove_field(4)
            n_embed.add_field(
                name=f"[{self.view.num}] Residents:",
                value="\n".join(self.view.split_list[self.view.page - 1]),
            )
        if self.view.type == "online":
            n_embed.remove_field(0)
            n_embed.add_field(
                name="Names:", value="\n".join(self.view.split_list[self.view.page - 1])
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
        if self.view.type == "town":
            n_embed.remove_field(4)
            n_embed.add_field(
                name=f"[{self.view.num}] Residents:",
                value="\n".join(self.view.split_list[self.view.page - 1]),
            )
        if self.view.type == "online":
            n_embed.remove_field(0)
            n_embed.add_field(
                name="Names:", value="\n".join(self.view.split_list[self.view.page - 1])
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
    def __init__(self, bot, interaction, li, type, timeout=30):
        self.bot: commands.Bot = bot
        self.interaction: commands.Context = interaction
        self.type = type
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
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name}: The commands extension was loaded successfully.")

    @slash_command(
        name="online",
        description="Use this command to get a list of online players.",
    )
    async def online(self, i: Interaction):
        await i.response.defer()

        if await is_server_online(i) == False:
            embed = get_embed(
                title="The server is offline at the moment.", color=discord.Color.red()
            )
            return await i.followup.send(embed=embed)

        res = requests.get(api_5)
        li = [res.json()[i]["name"] for i in range(len(res.json()))]

        view = Paginator(self.bot, i, li, "online")
        embed = get_embed(title=f"[{len(li)}] Online Players")
        embed.add_field(
            name="Names: ", value="\n".join(view.split_list[0]), inline=False
        )

        view.message = await i.followup.send(embed=embed, view=view)

    @slash_command(
        name="town",
        description="Use this command to view a town's info.",
    )
    async def town(self, i: Interaction, town=None):
        await i.response.defer()

        if not town:
            return await i.followup.send(
                "Please enter a town name in the `town` field.", ephemeral=True
            )

        if await is_server_online(i) == False:
            embed = get_embed(
                title="The server is offline at the moment.", color=discord.Color.red()
            )
            return await i.followup.send(embed=embed)

        res = requests.get(f"{api_1}/{town}")
        if res.json() == "That town does not exist!":
            return await i.send(
                embed=get_embed(
                    description="<a:crya:912762373591420989> This town doesn't exist...",
                    color=discord.Color.red(),
                )
            )

        embed = get_embed(title=f"Town: {res.json()['name']}")
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
        view = Paginator(self.bot, i, reslist, "town")
        embed.add_field(
            name=f"[{len(reslist)}] Residents: ",
            value="\n".join(view.split_list[0]),
            inline=False,
        )

        view.message = await i.followup.send(embed=embed, view=view)

    @slash_command(
        name="resident",
        description="Use this command to get a player's info. Make sure to type the '_' if it's a bedrock player.",
    )
    async def resident(self, i: Interaction, resident=None):
        await i.response.defer()

        if not resident:
            return await i.followup.send(
                "Please enter a resident username in the `resident` field.",
                ephemeral=True,
            )

        if await is_server_online(i) == False:
            embed = get_embed(
                title="The server is offline at the moment.", color=discord.Color.red()
            )
            return await i.followup.send(embed=embed)

        res = requests.get(f"{api_3}/{resident}")
        embed = get_embed(title=f"Resident: {res.json()['name']}")
        embed.add_field(name="Nation: ", value=str(res.json()["nation"]), inline=False)
        embed.add_field(name="Town: ", value=str(res.json()["town"]), inline=False)
        embed.add_field(name="Rank: ", value=str(res.json()["rank"]), inline=False)

        await i.followup.send(embed=embed)

    @slash_command(
        name="nation",
        description="Use this command to find info about a specific nation.",
    )
    async def nation(self, i: Interaction, nation=None):
        await i.response.defer()

        if not nation:
            return await i.followup.send(
                "Please enter a nation name in the `nation` field."
            )

        if await is_server_online(i) == False:
            embed = get_embed(
                title="The server is offline at the moment.", color=discord.Color.red()
            )
            return await i.followup.send(embed=embed)

        res = requests.get(f"{api_2}/{nation}")
        embed = get_embed(title=f"Nation: {res.json()['name']}")
        embed.add_field(name="Capital: ", value=res.json()["capitalName"], inline=True)
        embed.add_field(name="King: ", value=res.json()["king"], inline=True)
        embed.add_field(
            name="Population: ", value=str(len(res.json()["residents"])), inline=True
        )
        embed.add_field(name="Claims: ", value=str(res.json()["area"]), inline=True)
        embed.add_field(
            name="Towns: ", value=str(len(res.json()["towns"])), inline=True
        )

        await i.followup.send(embed=embed)

    @slash_command(
        name="townless",
        description="Use this command to get the name of online players that aren't in a town.",
    )
    async def townless(self, i: Interaction):
        await i.response.defer()

        if await is_server_online(i) == False:
            embed = get_embed(
                title="The server is offline at the moment.", color=discord.Color.red()
            )
            return await i.followup.send(embed=embed)

        res = requests.get(api_6)
        li = [res.json()[i]["name"] for i in range(len(res.json()))]
        if li:
            embed = get_embed(title="Townless Players")
            embed.add_field(
                name="Names: ", value="```" + "\n".join(li) + "```", inline=False
            )
        else:
            embed = get_embed(
                description="🚨 No townless players were found.",
                color=discord.Color.red(),
            )

        await i.followup.send(embed=embed)

    @slash_command(
        name="status",
        description="Use this command to get info about the server's network.",
    )
    async def status(self, i: Interaction):
        await i.response.defer()

        res = requests.get(api_4)
        embed = get_embed(title="Network Status")
        embed.add_field(
            name="Main Earth:", value=f'```{res.json()["towny"]}/110```', inline=False
        )
        embed.add_field(
            name="All servers:",
            value=f'```{res.json()["online"]}/110```',
            inline=False,
        )
        active = res.json()["serverOnline"]
        if active:
            embed.add_field(name="Server: ", value=":green_circle:", inline=False)
        else:
            embed.add_field(name="Server: ", value=":red_circle:", inline=False)

        await i.followup.send(embed=embed)

    @slash_command(
        name="onlinemayors",
        description="Use this command to get a list of the mayors that are online in the server.",
    )
    async def onlinemayors(self, i: Interaction):
        await i.response.defer()

        if await is_server_online(i) == False:
            embed = get_embed(
                title="The server is offline at the moment.", color=discord.Color.red()
            )
            return await i.followup.send(embed=embed)

        res = requests.get(api_5)
        embed = get_embed(title="Online Mayors")
        li = [
            f"{res.json()[i]['name']}: {res.json()[i]['town']}"
            for i in range(len(res.json()))
            if "rank" in res.json()[i] and res.json()[i]["rank"] == "Mayor"
        ]
        embed.add_field(
            name="Names: ", value="```" + "\n".join(li) + "```", inline=False
        )

        await i.followup.send(embed=embed)

    @slash_command(
        name="townonline",
        description="Use this command to view who is online in a town.",
    )
    async def townonline(self, i: Interaction, town=None):
        await i.response.defer()

        if await is_server_online(i) == False:
            embed = get_embed(
                title="The server is offline at the moment.", color=discord.Color.red()
            )
            return await i.followup.send(embed=embed)

        res = requests.get(api_5)
        embed = get_embed(title=f"Online Players in {town}")
        li = [
            res.json()[i]["name"]
            for i in range(len(res.json()))
            if "town" in res.json()[i] and res.json()[i]["town"].lower() == town.lower()
        ]
        embed.add_field(name="Online: ", value=str(len(li)), inline=False)
        if li:
            embed.add_field(
                name="Names: ", value="```" + "\n".join(li) + "```", inline=False
            )

        await i.followup.send(embed=embed)

    @slash_command(
        name="ruins",
        description="Use this command to get the names.",
    )
    async def ruinedtowns(self, i: Interaction):
        await i.response.defer()

        if await is_server_online(i) == False:
            embed = get_embed(
                title="The server is offline at the moment.", color=discord.Color.red()
            )
            return await i.followup.send(embed=embed)

        res = requests.get(api_1)
        embed = get_embed(title="Ruined towns list")
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

        await i.followup.send(embed=embed)


def setup(bot):
    bot.add_cog(Commands(bot))

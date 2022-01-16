import nextcord as discord, requests
from nextcord.ext import commands
from nextcord import Interaction
from typing import Union
from config import token, db, api_4, EMBED_COLOR

linked = db["linked"]


async def get_embed(i: Interaction, title=None, description=None, color=None):
    if not color:
        color = EMBED_COLOR
    kwargs = {"color": color}
    if title:
        kwargs["title"] = title
    if description:
        kwargs["description"] = description
    embed = discord.Embed(**kwargs)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/icons/911944157625483264/359028bbc374ee43f60e25e35c39874b.png?size=1024"
    )
    return embed


async def is_server_online(i):
    res = requests.get(api_4)
    active = res.json()["serverOnline"]
    if active:
        return True
    return await i.send(
        embed=await get_embed(
            i,
            ":red_circle: The server is offline, can't find that info",
            discord.Color.red(),
        )
    )


intents = None

bot = commands.Bot(
    command_prefix="/",
    intents=intents,
    help_command=None,
    case_insensitive=True,
)


@bot.event
async def on_ready():
    print(f"{bot.user.name}: Bot loaded successfully. ID: {bot.user.id}")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="how I'm being developed."
        ),
    )


if __name__ == "__main__":
    bot.load_extension("cogs.commands")

    bot.run(token)

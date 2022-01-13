import nextcord as discord, requests, os
from nextcord.ext import commands, tasks
from typing import Union

EMBED_COLOR = discord.Color.blue()

async def get_embed(ctx: commands.Context, title=None, description=None, color=None):
    if not color:
        color = EMBED_COLOR
    kwargs = {"color": color}
    if title:
        kwargs["title"] = title
    if description:
        kwargs["description"] = description
    embed = discord.Embed(**kwargs)
    embed.set_author(
        name=ctx.message.author.display_name, icon_url=ctx.author.avatar.url
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/911944157625483264/359028bbc374ee43f60e25e35c39874b.png?size=1024")
    return embed


async def is_server_online(ctx):
    res = requests.get(os.api_4)
    active = res.json()["serverOnline"]
    if active:
        return True
    return await ctx.send(
        embed=await get_embed(
            ctx, ":red_circle: The server is offline, can't find that info"
        )
    )
  else:
    return False


async def find_linked(user: Union[discord.User, int, commands.Context]):
    if isinstance(user, commands.Context):
        id_ = user.message.author.id
    elif isinstance(user, (discord.User, discord.Member)):
        id_ = user.id
    else:
        id_ = user
    players = await links.find_one({"_id": "players"})
    if id_ in players:
        return players["ign"]
    else:
        return


intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="/",
    intents=intents,
    help_command=CustomHelpCommand(),
    case_insensitive=True,
)
DiscordComponents(bot)

@bot.event
async def on_ready():
    print(f"{bot.user.name}: Bot loaded successfully. ID: {bot.user.id}")
    await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="how I'm being developed.")


if __name__ == "__main__":
    #bot.load_extension("cogs.commands")

    bot.run(token)

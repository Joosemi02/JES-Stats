import nextcord as discord
from nextcord.ext import commands
from config import token, db, EMBED_COLOR

config = db["config"]


def get_embed(title=None, description=None, color=None):
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
    online = await config.find_one({"_id": "config"})
    return online["crashed"] != True


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
            type=discord.ActivityType.playing, name="Just and Earth Server"
        ),
    )


@bot.command()
@commands.is_owner()
async def guilds(ctx: commands.Context):
    li = "\n".join(g.name for g in bot.guilds)
    embed = get_embed(description=li)
    await ctx.send(embed=embed)


@bot.command()
async def test(ctx):
    await ctx.send(await bot.application_info().members)


@bot.command()
@commands.is_owner()
async def crashed(ctx: commands.Context, bool: bool):
    if bool:
        await config.update_one({"_id": "config"}, {"$set": {"crashed": True}})
    else:
        await config.update_one({"_id": "config"}, {"$set": {"crashed": False}})
    await ctx.message.delete()


if __name__ == "__main__":
    bot.load_extension("cogs.commands")
    bot.load_extension("cogs.messages")

    bot.run(token)

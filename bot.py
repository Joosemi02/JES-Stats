import nextcord as discord
from nextcord.ext import commands
from nextcord import Interaction
from config import token, db, EMBED_COLOR

config = db["config"]


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
    online = await config.find_one({"_id": "online"})
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


if __name__ == "__main__":
    bot.load_extension("cogs.commands")
    bot.load_extension("cogs.messages")

    bot.run(token)

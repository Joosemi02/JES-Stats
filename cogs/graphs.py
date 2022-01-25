import matplotlib
import nextcord as discord
import requests
from nextcord.ext import commands, tasks
from config import db, api_1, api_2, api_3, api_4, api_5, api_6, api_7

graphs = db["graphs"]


class Graphs(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name}: The graphs extension was loaded successfully.")

    @tasks.loop(minutes=10)
    async def get_data():
        nations = 0

    @commands.command()
    async def test(self, ctx):
        print(requests.get(api_3).json())
        # print(requests.get(api_4).json())
        # print(requests.get(api_5).json())
        # print(requests.get(api_6).json())
        # print(requests.get(api_7).json())


def setup(bot):
    bot.add_cog(Graphs(bot))

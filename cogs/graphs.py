import matplotlib
import nextcord as discord
import requests
from asyncio import tasks
from nextcord.ext import commands
from config import db, api_1, api_2, api_3, api_4, api_5, api_6, api_7, api_8

graphs = db["graphs"]

class Graphs(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name}: The graphs extension was loaded successfully.")

    @tasks.loop()
    async def get_data():
        pass
    
    @commands.command()
    async def test(self, ctx):
        print(requests.get(api_1))
        print(requests.get(api_2))
        print(requests.get(api_3))
        print(requests.get(api_4))
        print(requests.get(api_5))
        print(requests.get(api_6))
        print(requests.get(api_7))
        print(requests.get(api_8))

def setup(bot):
    bot.add_cog(Graphs(bot))
import matplotlib
import nextcord as discord
from asyncio import tasks
from nextcord.ext import commands
from config import db

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

def setup(bot):
    bot.add_cog(Graphs(bot))
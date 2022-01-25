from datetime import date
import matplotlib
import nextcord as discord
import requests
from nextcord.ext import commands, tasks
from config import db, api_5, api_6, api_7

graphs = db["graphs"]


class Graphs(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name}: The graphs extension was loaded successfully.")

    @tasks.loop(minutes=10)
    async def get_data():
        res = requests.get(api_5).json()
        spain = sum(
            ("nation" in res[i] and res[i]["nation"].lower() == "spanish_republic")
            for i in range(len(res))
        )
        online = sum("nation" in res[i] for i in range(len(res)))
        time = date.timetuple()
        day = date.today()
        try:
            await graphs.insert_one(
                {"_id": day, f"{time}": {"spain": spain, "online": online}}
            )
        except:
            await graphs.update_one(
                {
                    "_id": day,
                    "$set": {f"{time}": {"spain": spain, "online": online}},
                }
            )

    @commands.command()
    async def test(self, ctx):
        print(requests.get(api_6).json())
        # print(requests.get(api_7).json())


def setup(bot):
    bot.add_cog(Graphs(bot))

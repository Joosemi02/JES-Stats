from datetime import date
import matplotlib
import nextcord as discord
import requests
from nextcord.ext import commands, tasks
from config import db, api_5

graphs = db["graphs"]


class Graphs(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name}: The graphs extension was loaded successfully.")

    @tasks.loop(seconds=15)
    async def get_data(self):
        res = requests.get(api_5).json()
        spain = sum(
            ("nation" in res[i] and res[i]["nation"].lower() == "spanish_republic")
            for i in range(len(res))
        )
        online = sum("nation" in res[i] for i in range(len(res)))
        time = date.timetuple()
        day = date.today()
        try:
            print(online, time)
            await graphs.insert_one(
                {"_id": day, f"{time}": {"spain": spain, "online": online}}
            )
        except:
            print(spain, day)
            await graphs.update_one(
                {
                    "_id": day,
                    "$set": {f"{time}": {"spain": spain, "online": online}},
                }
            )
    get_data.start()

def setup(bot):
    bot.add_cog(Graphs(bot))

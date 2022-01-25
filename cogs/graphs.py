from datetime import date, datetime
from json import JSONDecodeError
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
        self.get_data.start()

    @tasks.loop(minutes=15)
    async def get_data(self):
        try:
            res = requests.get(api_5).json()
            spain = sum(
                ("nation" in res[i] and res[i]["nation"].lower() == "spanish_republic")
                for i in range(len(res))
            )
            online = sum("nation" in res[i] for i in range(len(res)))
        except JSONDecodeError:
            spain = 0
            online = 0
        n = datetime.now()
        time = f"{n.hour}.{n.minute}"
        day = date.today()
        await graphs.insert_one(
            {"_id": day, f"{time}": {"spain": spain, "online": online}}
        )
        await graphs.update_one(
            {"_id": day},
            {
                "$set": {f"{time}": {"spain": spain, "online": online}},
            },
        )


def setup(bot):
    bot.add_cog(Graphs(bot))

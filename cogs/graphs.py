import asyncio
import io
import matplotlib as mpl
import matplotlib.image as mpi
import matplotlib.pyplot as plt
import nextcord as discord
import numpy as np
import requests
import schedule
from datetime import datetime
from json import JSONDecodeError
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

    async def send_graph(self):
        c: discord.TextChannel = self.bot.get_channel(851216632155865161)
        graph = await self.get_graph()
        embed = discord.Embed()
        embed.set_author(name=c.guild.name, icon_url=c.guild.icon.url)
        embed.set_image(url="attachment://graph.png")
        await c.send(embed=embed, file=graph)

    @tasks.loop(minutes=1)
    async def get_data(self):
        n = datetime.now()
        if n.minute not in (0, 15, 30, 45):
            return
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
        min = "00" if n.minute == 0 else n.minute
        time = f"{n.hour+1}:{min}"
        day = n.strftime("%Y/%m/%d")
        try:
            await graphs.insert_one(
                {"_id": day, f"{time}": {"spain": spain, "online": online}}
            )
        except:
            await graphs.update_one(
                {"_id": day},
                {
                    "$set": {f"{time}": {"spain": spain, "online": online}},
                },
            )

    @commands.command(name="graph")
    async def make_graph(self, ctx):
        data = await graphs.find_one({"_id": datetime.now().strftime("%Y/%m/%d")})
        spain = []
        online = []
        for n in data.keys():
            if n == "_id":
                continue
            spain.append(data[n]["spain"])
            online.append(data[n]["online"])
        fig = plt.figure()
        fig, ax = plt.subplots()
        x = list(data.keys())
        x.remove("_id")
        ax.plot(x, spain, "-b")
        ax.plot()
        storage = self.bot.get_channel(935596324127129740)
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        fig = discord.File(fp=buf, filename="graph.png")
        await storage.send(file=fig)

    async def get_graph(self):
        storage = self.bot.get_channel(935596324127129740)
        for m in await storage.history(limit=1).flatten():
            m: discord.Message
            for a in m.attachments:
                return await a.to_file()

    schedule.every().day.at("23:59").do(make_graph)
    schedule.every().day.at("08:00").do(send_graph)


def setup(bot):
    bot.add_cog(Graphs(bot))

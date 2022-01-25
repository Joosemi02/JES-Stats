import asyncio
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
        c: discord.TextChannel = self.bot.get_channel(
            871434957308985374
        )  # 851216632155865161
        graph = await self.get_graph()
        embed = discord.Embed()
        embed.set_author(name=c.guild.name, icon_url=c.guild.icon.url)
        embed.set_image(url="attachments://graph.png")
        await c.send(embed=embed, file=graph)

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
        if n.minute == 0:
            n.minute = 00
        time = f"{n.hour+1}:{n.minute}"
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

    @get_data.before_loop
    async def before_task(self):
        await self.bot.wait_until_ready()
        while datetime.now().minute not in (0, 15, 30, 45):
            await asyncio.sleep(60)

    @commands.command(name="graph")
    async def make_graph(self, ctx):
        data = await graphs.find_one({"_id": datetime.now().strftime("%Y/%m/%d")})
        spain = []
        online = []
        for n in data.keys():
            spain.append(data[n]["spain"])
            online.append(data[n]["online"])
        fig = plt.figure()
        fig, ax, bx = plt.subplots(2, 2)
        ax.plot(data.keys(), spain)
        bx.plot(data.keys(), online)
        fig.show()
        storage = self.bot.get_channel(935596324127129740)
        await storage.send(file=fig)

    async def get_graph(self):
        storage = self.bot.get_channel(935596324127129740)
        for m in storage.history(1).flatten():
            m: discord.Message
            for a in m.attachments:
                return a.url

    # schedule.every().day.at("00:00").do(send_graph)


def setup(bot):
    bot.add_cog(Graphs(bot))

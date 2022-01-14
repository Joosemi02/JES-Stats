import nextcord as discord, os
from motor import motor_tornado

token = os.environ["token"]

client = motor_tornado.MotorClient(os.environ["db_token"])
db = client["jesbot"]

EMBED_COLOR = discord.Color.blue()

api_1 = os.environ["api_1"]
api_2 = os.environ["api_2"]
api_3 = os.environ["api_3"]
api_4 = os.environ["api_4"]
api_5 = os.environ["api_5"]
api_6 = os.environ["api_6"]
api_7 = os.environ["api_7"]
api_8 = os.environ["api_8"]

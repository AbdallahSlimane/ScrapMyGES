import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

bot_token = os.getenv("BOT_TOKEN")


@client.event
async def on_ready():
    print("Le bot est prêt !")


@client.command()
async def ping(ctx):
    await ctx.send("Pong")


client.run(bot_token)

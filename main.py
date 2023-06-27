import os

import discord
from bot_answers import Answer
from discord.ext import commands
from dotenv import load_dotenv
from myges_scrap_marks import *
from myges_scrap_planning import *

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

bot_token = os.getenv("BOT_TOKEN")
username = os.getenv("MYGES_USERNAME")
password = os.getenv("MYGES_PASSWORD")


@client.event
async def on_ready():
    print(Answer.READY.value)


@client.command()
async def ping(ctx):
    await ctx.send(Answer.PONG.value)


@client.command()
async def marks(ctx):
    await ctx.send(Answer.WAIT.value)
    scraper = MyGesScrapMarks(username, password)
    scraper.login()
    get_marks = scraper.scrape_and_save_marks_for_specific_semesters()
    scraper.close()
    for m in get_marks["body"]:
        await ctx.send(m)
    await ctx.send(Answer.OK.value)


@client.command()
async def plannings(ctx):
    await ctx.send(Answer.WAIT.value)
    scraper = MyGesScrapPlanning(username, password)

    scraper.login()
    scraper.navigate_to_planning()
    get_planning = scraper.scrape_planning()
    # scraper.next_week()
    # scraper.scrape_planning()
    print(get_planning)
    for v in get_planning:
        await ctx.send(get_planning[v])

    await ctx.send(Answer.OK.value)


client.run(bot_token)

import os
import discord

from bot_answers import Answer
from discord.ext import commands
from dotenv import load_dotenv

from myges_scrap_marks import *
from myges_scrap_planning import *
from login import *

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

bot_token = os.getenv("BOT_TOKEN")


@client.event
async def on_ready():
    print(Answer.READY.value)


@client.command()
async def ping(ctx):
    await ctx.send(Answer.PONG.value)


@client.command()
async def my(ctx: discord.ext.commands.Context):
    author = ctx.author
    guild = ctx.guild
    if ctx.me.guild_permissions.manage_channels:
        if discord.utils.get(ctx.guild.channels, name=author.name) is not None:
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            author: discord.PermissionOverwrite(read_messages=True),
        }
        name = author.name.lower().replace(" ", "_")
        channel = await guild.create_text_channel(name, overwrites=overwrites)
        await channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
        await channel.send("# Discord ne demandera jamais vos identifiants MYGES !")
        await channel.send(
            "## Pour vous connectez, saisissez: \n!login *identifiant* *mot de passe*\n*> Vous aurez accès au bot pendant 5 min*")
    else:
        await ctx.send("Vous n'avez pas les autorisations nécessaires pour créer des canaux.")

    await ctx.send("OK")


@client.command()
async def login(ctx: discord.ext.commands.Context, *args):
    await ctx.message.delete()
    author = ctx.author
    if author.name.lower().replace(" ", "_") != ctx.channel.name:
        print(author.name, ctx.channel.name)
        await ctx.message.delete()  # delete
        await ctx.send("## Vous ne pouvez pas executer cette commande dans ce channel", delete_after=5)
        return

    if len(args) != 2:
        await ctx.message.delete()  # delete
        await ctx.send("## Vous devez renseigner 2 paramètres", delete_after=5)
        return

    username = args[0]
    pwd = args[1]

    await ctx.send(f"identifiants:||{username} {pwd}||", delete_after=100)


@client.command()
async def marks(ctx: discord.ext.commands.Context):
    user_login = Login()
    await user_login.get_username(ctx)
    if user_login.is_empty():
        await ctx.message.delete()  # delete
        await ctx.send("Vous devez vous connecter avant de poursuivre", delete_after=5)
        return

    scraper = MyGesScrapMarks()
    user_login.login(scraper.driver)
    get_marks = scraper.scrape_and_save_marks_for_specific_semesters()
    scraper.close()
    for m in get_marks["body"]:
        await ctx.send(m)
    await ctx.message.delete() #delete


@client.command()
async def plannings(ctx):
    user_login = Login()
    await user_login.get_username(ctx)
    if user_login.is_empty():
        await ctx.message.delete()  # delete
        await ctx.send("Vous devez vous connecter avant de poursuivre", delete_after=5)
        return

    scraper = MyGesScrapPlanning()
    user_login.login(scraper.driver)
    scraper.navigate_to_planning()
    get_planning = scraper.scrape_planning()
    scraper.next_week()
    scraper.scrape_planning()
    for v in get_planning:
        await ctx.send(get_planning[v])
    await ctx.message.delete() #delete


client.run(bot_token)

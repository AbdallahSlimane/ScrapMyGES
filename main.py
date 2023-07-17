import os

from discord.ext import commands
from dotenv import load_dotenv

from all_enum import *
from help_command import MyHelp
from login import *
from myges_scrap_marks import *
from myges_scrap_planning import *
from myges_scrap_syllabus import *
from myges_scrap_student import *

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)
client.help_command = MyHelp()

bot_token = os.getenv("BOT_TOKEN")

days = [
    "Lundi",
    "Mardi",
    "Mercredi",
    "Jeudi",
    "Vendredi",
    "Samedi",
    "Dimanche",
]


@client.event
async def on_ready():
    print(Answer.READY.value)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await command_not_found(ctx, Answer.CMD_NOT_FOUND.value)

    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        print(type(error), error)
        await command_not_found(ctx, Answer.CMD_ERROR.value)


async def command_not_found(ctx, message):
    error_message = message
    embed = discord.Embed(description=error_message, color=discord.Color.red())
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    """Retourne pong"""
    await ctx.send(Answer.PONG.value)


@client.command()
async def commands(ctx):
    """Retourne la documentation de toutes les commandes disponibles"""

    description = ""
    for command in client.commands:
        description += f"### - {command.name}\n{command.help}\n"

    embed = discord.Embed(title="Commandes", description=description, color=discord.Color.green())
    await ctx.send(embed=embed)


@client.command()
async def my(ctx: discord.ext.commands.Context):
    """Création de ton channel privé"""
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
        await channel.send(Answer.CMD_MY_Id.value)
        await channel.send(Answer.CMD_MY_TUTO.value)
    else:
        await ctx.send(Answer.CMD_NOT_AUTHORIZED.value)

    await ctx.send(Answer.OK.value)


@client.command()
async def login(ctx: discord.ext.commands.Context, *args):
    """Connexion à MYGES. Deux paramètres: Identifiant + Mot de passe """
    await ctx.message.delete()
    author = ctx.author
    if author.name.lower().replace(" ", "_") != ctx.channel.name:
        await ctx.message.delete()  # delete
        await ctx.send(Answer.CMD_CANNOT_EXEC.value, delete_after=5)
        return

    if len(args) != 2:
        await ctx.message.delete()  # delete
        await ctx.send(Answer.CMD_WARNING_PARAM.value, delete_after=5)
        return

    username = args[0]
    pwd = args[1]

    await ctx.send(f"identifiants:||{username} {pwd}||", delete_after=3 * 60)


@client.command()
async def marks(ctx: discord.ext.commands.Context):
    """Récupère toutes tes notes du semestre 1 et 2"""
    user_login = await checks_login(ctx)

    path = Filename.FOLDER_MARK.value + Filename.FILE_MARK.get_filename(user_login.username, "1")
    path_2 = Filename.FOLDER_MARK.value + Filename.FILE_MARK.get_filename(user_login.username, "2")

    scraper = MyGesScrapMarks()
    user_login.login(scraper.driver)
    scraper.scrape_and_save_marks_for_specific_semesters(path, path_2)
    scraper.close()

    with open(path, 'r', encoding='utf-8') as f:
        semester1 = json.load(f)
        await ctx.send(f"# Notes Semestre 1")
        await send_marks(semester1, ctx)

    with open(path_2, 'r', encoding='utf-8') as f:
        semester2 = json.load(f)
        await ctx.send(f"# Notes Semestre 2")
        await send_marks(semester2, ctx)

    await ctx.send(Answer.CMD_DONE.value)


async def send_marks(all_marks, ctx: discord.ext.commands.Context):
    for m in all_marks["body"]:
        await ctx.send(
            f"## Matière: {m['Matière']} :\n"
            f"- {m['Intervenant']}\n"
            f"- Coef: {m['Coef.']}\n"
            f"- ECTS: {m['ECTS']}\n"
            f"- CC1: {m['CC1']}\n"
            f"- CC2: {m['CC2']}\n"
            f"- Exam: {m['Exam']}"
        )


@client.command()
async def syllabus(ctx: discord.ext.commands.Context):
    """Récupère toutes les syllabus du semestre 1 et 2"""
    user_login = await checks_login(ctx)

    path = Filename.FOLDER_SYLLABUS.value + Filename.FILE_SYLLABUS.get_filename(user_login.username, "1")
    path_2 = Filename.FOLDER_SYLLABUS.value + Filename.FILE_SYLLABUS.get_filename(user_login.username, "2")

    scraper = MyGesScrapSyllabus()
    user_login.login(scraper.driver)
    scraper.scrape_and_save_syllabus_for_specific_semesters(path, path_2)
    scraper.close()

    with open(path, 'r', encoding='utf-8') as f:
        semester1 = json.load(f)
        await ctx.send(f"# Syllabus Semestre 1")
        await send_syllabus(semester1, ctx)

    with open(path_2, 'r', encoding='utf-8') as f:
        semester2 = json.load(f)
        await ctx.send(f"# Syllabus Semestre 2")
        await send_syllabus(semester2, ctx)

    await ctx.send(Answer.CMD_DONE.value)


async def send_syllabus(syllabus_to_send, ctx: discord.ext.commands.Context):
    for s in syllabus_to_send["body"]:
        await ctx.send(
            f"## Matière: {s['Matière']} :\n"
            f"- {s['Syllabus']}\n"
            f"- {s['Intervenant']}\n"
        )


@client.command()
async def students(ctx: discord.ext.commands.Context):
    """Récupère le trombinoscope"""

    user_login = await checks_login(ctx)
    path = Filename.FOLDER_STUDENT.value + Filename.FILE_STUDENT.get_filename(user_login.username, "")

    scraper = MyGesScrapStudent()
    user_login.login(scraper.driver)
    scraper.scrape_student(path)
    scraper.close()

    with open(path, 'r', encoding='utf-8') as f:
        get_students = json.load(f)

        for s in get_students:
            await ctx.send(
                f"{s['name']} :\n"
                f"- {s['image_url']}\n"
            )
    await ctx.send(Answer.CMD_DONE.value)


@client.command()
async def plannings(ctx):
    """Récupère l'emploi du temps de la semaine"""

    user_login = await checks_login(ctx)
    path = Filename.FOLDER_PLANNING.value + Filename.FILE_PLANNING.get_filename(user_login.username, "")

    scraper = MyGesScrapPlanning()
    user_login.login(scraper.driver)
    scraper.navigate_to_planning()
    get_planning = scraper.scrape_planning(path)

    await ctx.send(f"# {get_planning['week']}\n\t *{get_planning['last_update']}*")
    for i, day in enumerate(get_planning['events']):
        await ctx.send(f"# {days[i]} :\n" + "\n".join(
            [f"- [{event['start_at']} - {event['end_at']}] {event['title']} *{event['room']}*" for event in day]))

    await ctx.send(Answer.CMD_DONE.value)


async def checks_login(ctx):
    user_login = Login()
    await user_login.get_username(ctx)
    if user_login.is_empty():
        await ctx.message.delete()  # delete
        await ctx.send(Answer.CMD_MUST_CONNECT_BEFORE.value, delete_after=5)
        return
    else:
        return user_login


client.run(bot_token)

import os

from discord.ext import commands
from dotenv import load_dotenv

from bot_answers import Answer
from login import *
from myges_scrap_marks import *
from myges_scrap_planning import *

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

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
        await channel.send(Answer.CMD_MY_Id.value)
        await channel.send(Answer.CMD_MY_TUTO.value)
    else:
        await ctx.send(Answer.CMD_NOT_AUTHORIZED.value)

    await ctx.send(Answer.OK.value)


@client.command()
async def login(ctx: discord.ext.commands.Context, *args):
    await ctx.message.delete()
    author = ctx.author
    if author.name.lower().replace(" ", "_") != ctx.channel.name:
        print(author.name, ctx.channel.name)
        await ctx.message.delete()  # delete
        await ctx.send(Answer.CMD_CANNOT_EXEC.value, delete_after=5)
        return

    if len(args) != 2:
        await ctx.message.delete()  # delete
        await ctx.send(Answer.CMD_WARNING_PARAM.value, delete_after=5)
        return

    username = args[0]
    pwd = args[1]

    await ctx.send(f"identifiants:||{username} {pwd}||", delete_after=3*60)


@client.command()
async def marks(ctx: discord.ext.commands.Context):
    user_login = await checks_login(ctx)

    scraper = MyGesScrapMarks()
    user_login.login(scraper.driver)
    scraper.scrape_and_save_marks_for_specific_semesters()
    scraper.close()

    with open(f'ScrapMark/marks_semester_1.json', 'r', encoding='utf-8') as f:
        semester1 = json.load(f)
        await send_marks(semester1, ctx)
        await ctx.send(f"# Notes Semestre 1")

    with open(f'ScrapMark/marks_semester_2.json', 'r', encoding='utf-8') as f:
        semester2 = json.load(f)
        await ctx.send(f"# Notes Semestre 2")
        await send_marks(semester2, ctx)

    await ctx.message.delete()  # delete


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
async def plannings(ctx):
    user_login = await checks_login(ctx)

    scraper = MyGesScrapPlanning()
    user_login.login(scraper.driver)
    scraper.navigate_to_planning()
    get_planning = scraper.scrape_planning()
    scraper.next_week()
    scraper.scrape_planning()

    await ctx.send(f"# {get_planning['week']}\n\t *{get_planning['last_update']}*")
    for i, day in enumerate(get_planning['events']):
        await ctx.send(f"# {days[i]} :\n" + "\n".join(
            [f"- [{event['start_at']} - {event['end_at']}] {event['title']} *{event['room']}*" for event in day]))


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

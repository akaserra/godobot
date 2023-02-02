import discord
import asyncio
import jthon
from discord.ext import tasks, commands
from discord.ext.commands import cooldown, BucketType
from mcrcon import MCRcon
from mcstatus import JavaServer
import random


TOKEN = "token"  # token di sto cazzo

GUILD_ID = 1021423190783823964  # ID del server

try:
    host = "127.0.0.1"  # ip server minecraft
    query_port = 25565  # porta query
    rcon_port = 25575  # porta rcon
    rcon_pwd = "godo"  # password rcon
    query_server = JavaServer.lookup(host + ":" + str(query_port))
    status = query_server.status()
except ConnectionRefusedError:
    pass

intents = discord.Intents.all()

intents.message_content = True

bot = commands.Bot(
    command_prefix=".",  # prefix del bot
    owner_id="777231224753750057",  # id vostro
    case_insensitive=True,
    intents=intents,
    help_command=None
)

skidders = jthon.load("skidder", [])

lista_skidders = ["Mercoledii", "ImGqbbo", "svantaggiato", "SmoDev_", "sonoDoge", "FixMem", "danilotallaric", "WinPrefetchView"]  
# Se avete altri IGN di skidder mandatemeli pure su Telgram

welcomerid = 1021423938066202625  # id canale welcome


@bot.event
async def on_ready():
    '''
    # Playing status
    await bot.change_presence(activity=discord.Game(name="con tua madre"))

    # Streaming status
    await bot.change_presence(activity=discord.Streaming(name="GodoBot", url=godo))

    # Listening status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="gli orgasmi di mammt"))

    # Watching status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="I porno"))'''
    status_task.start()
    anti_joosgral.start()

    print("\r──────────────────────────")
    print("Username: %s" % bot.user.name)
    print("ID: %s" % bot.user.id)
    print("──────────────────────────")


async def change_nick(member):
    if not member.bot:
        if member.id not in skidders.data:
            skidders.data.append(member.id)
            skidders.save()
        await member.edit(
            nick=f"Skidder #{skidders.data.index(member.id)+1}" # cambia i nomi dei nuovi arrivati in skidder #numero
        )


@bot.event
async def on_member_join(member):
    await change_nick(member)
    await asyncio.sleep(1)
    embed = discord.Embed( # embed di benvenuto
        title=f"Benvenuto {member.name}",
        description="Odio gli skidder, nel caso tu sia uno skidder...beh sei morto\n\nSe sei un furetto di nome mercoledì puoi tranquillamente bruciarti, non sentiremo la tua mancanza.",
        color=discord.Color.dark_purple(),
        url="https://github.com/akaserra/godobot"

    )
    embed.set_author(name=bot.user.name, url="https://github.com/akaserra/godobot",
                     icon_url=bot.user.display_avatar)
    embed.set_footer(text="Buona permanenza nel Team")
    embed.set_image(url="https://cdn.discordapp.com/attachments/984091942549852190/1070380955371585638/godobot.png")
    await bot.get_channel(welcomerid).send(embed=embed)


@bot.event
async def on_user_update(before, after):

    if before.name != after.name:
        guild = bot.get_guild(GUILD_ID)
        member = guild.get_member(after.id)
        await change_nick(member)



@tasks.loop()
async def status_task() -> None:
    try:
        # discord.Status.dnd
        # discord.Status.idle
        # discord.Status.online
        query_server = JavaServer.lookup(host + ":" + str(query_port))
        status = query_server.status()
        giocatori = status.players.online
        if giocatori > 1:
            await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{status.players.online} utenti online"))
        elif giocatori > 0:
            await bot.change_presence(status=discord.Status.online,
                                      activity=discord.Activity(type=discord.ActivityType.watching,
                                                                name=f"{status.players.online} utente online"))
        else:
            await bot.change_presence(status=discord.Status.idle,
                                      activity=discord.Activity(type=discord.ActivityType.watching,
                                                                name=f"Nessun giocatore online :("))

        # se non capisci sto codice ti puoi tranquillamente dar fuoco

        await asyncio.sleep(3)
    except ConnectionRefusedError:
        await bot.change_presence(status=discord.Status.dnd,
                                  activity=discord.Activity(type=discord.ActivityType.watching,
                                                            name=f"Server offiline"))


# ANTI SKIDDER SYSTEM
@tasks.loop()
async def anti_joosgral() -> None:
    query_server = JavaServer.lookup(host + ":" + str(query_port))
    query = query_server.query()
    query = f"{', '.join(query.players.names)}"
    if "joosgral" in query:
        with MCRcon(host=host, password=rcon_pwd, port=rcon_port) as mcr:
            mcr.command(f"kick joosgral L'anti skidder system ti ha identificato stupido furetto.")
            mcr.command(f'alert Attenzione! Tutti al riparo! E\' arrivato il maestro-skidder dell\'universo! Ritiratevi nei vostri rifugi prima che vi skidda l\'identita e vi exposa senza motivo, perche\' non ha un cazzo da fare nella sua vita oltre skiddare!')
    await asyncio.sleep(1)

# .status mostra delle info sul server minecraft
@bot.command()
async def status(ctx):
    try:
        query_server = JavaServer.lookup(host + ":" +str(query_port))
        status = query_server.status()
        ping = str(status.latency)
        ping = ping[0]
        utenti = status.players.online
        if utenti > 1:
            await ctx.send(f"Il server ha {status.players.online} utenti online e pinga {ping} ms")
        elif utenti > 0:
            await ctx.send(f"Il server ha {status.players.online} utente online e pinga {ping} ms")
        else:
            await ctx.send(f"Il server ha non ha nessun giocatore online e pinga {ping} ms")
    except ConnectionRefusedError:
        await ctx.send("Il Server è offilne")


# .alert args manda l'alert su mc
@bot.command()
async def alert(ctx, *, arg):
    with MCRcon(host=host, password=rcon_pwd, port=rcon_port) as mcr:
        mcr.command(f"alert {arg}")
        await ctx.reply(f"Alert godurioso inviato")


# .skidder che skidder sei oggi?
@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)  # cooldown di un giorno (espresso in secondi)
async def skidder(ctx):
    global skidderino
    skidderino = random.choice(lista_skidders)  # sceglie uno degli skidder nella lista
    url = "https://namemc.com/profile/"
    tb = "https://mc-heads.net/body/"

    embed = discord.Embed(
        title=f"{skidderino}",
        description=f"{ctx.author.display_name} oggi sei {skidderino}",
        color=discord.Color.dark_purple(),
        url=url + skidderino

    )
    embed.set_author(name=bot.user.name, url="https://github.com/akaserra/godobot",
                     icon_url=bot.user.display_avatar)
    embed.set_thumbnail(url=tb + skidderino)
    await ctx.send(embed=embed)

@skidder.error
async def skidder_error(ctx, error):  # manda l'embed precedente se esegue il comando prima che il cooldown finisca
    if isinstance(error, commands.CommandOnCooldown):
        url = "https://namemc.com/profile/"
        tb = "https://mc-heads.net/body/"


        embed = discord.Embed(
            title=f"{skidderino}",
            description=f"{ctx.author.display_name} oggi sei {skidderino}",
            color=discord.Color.dark_purple(),
            url=url + skidderino

        )
        embed.set_author(name=bot.user.name, url="https://github.com/akaserra/godobot",
                         icon_url=bot.user.display_avatar)
        embed.set_thumbnail(url=tb + skidderino)
        await ctx.send(embed=embed)


bot.run(TOKEN)


import asyncio
import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get
from youtubesearchpython import VideosSearch

BOT_PREFIX = '-'
bot = commands.Bot(command_prefix=BOT_PREFIX)
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


def leer_token():
    with open("token.txt", "r") as f:
        linea = f.readlines()
        return linea[0].strip()


token = leer_token()


def url_gen(*args):
    busqueda = " ".join(args[:])
    search = VideosSearch(busqueda, limit=1)
    url = (search.result()['result'][0]['link'])
    return url


async def player_gen(link):
    player = await YTDLSource.from_url(link, stream=True)
    return player


def parar(ctx):
    voz = get(bot.voice_clients, guild=ctx.guild)
    voz.stop()


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Juanito Juan"))
    print(f"bot ready as {bot.user.name}")


@bot.command()
async def send_announce(ctx):
    embed = discord.Embed(title="xXPapakebab ChangesXx", description="Los muerto la version ya",
                          color=0xff0000)
    embed.add_field(name="Sobre los cambios",
                    value="Ya no se enviará este mensaje cada vez que el puto servidor se reinicie, grasia.",
                    inline=True)
    embed.set_footer(text="Creado por MizfitZ (ig: @rafaelgc2002)")
    for guild in bot.guilds:
        for channel in guild.channels:
            if channel.name in ("general", "General", "musica", "Musica", "música", "Música", "Music", "music") and str(channel.type) == 'text':
                await channel.send(embed=embed)


@bot.command()
async def test(ctx, *arg):
    print(" ".join(arg[:]))


@bot.command()
async def hola(ctx):
    await ctx.send(f"Pa ti mi cola, te falta calle{ctx.message.author.mention}")


@bot.command()
async def nada(ctx):
    await ctx.send(f"Te he dicho que no hay nada subnormal {ctx.message.author.mention}")


@bot.command(aliases=["u"])
async def users(ctx):
    num_miembros = ctx.guild.member_count
    await ctx.send(f"el número de miembros totales es: {num_miembros}")


@bot.event
async def on_member_join(member):
    await member.send(f"Bienvenido a la whyskería, {member.mention}")


@bot.command(aliases=["i"])
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}"
                          , description="Posiblemente el mejor bot del mundo, es muy trabajador y simpático...",
                          color=0xea0606)
    embed.set_thumbnail(
        url="https://www.google.com/imgres?imgurl=https%3A%2F%2Fimg2.freepng.es%2F20180328%2Fvuq%2Fkisspng-baked"
            "-potato-kebab-pizza-baked-beans-chicken-nugge-potato-5abc136e100bb4.0432096215222751820657.jpg&imgrefurl"
            "=https%3A%2F%2Fwww.freepng.es%2Fpng-f7po6e%2F&tbnid=l1C1zp_BzSxxcM&vet=12ahUKEwjXk"
            "-Llo4TyAhVNgc4BHfcMBnMQMyhNegUIARCDAQ..i&docid=BoIjstQYlcll4M&w=900&h=600&q=papa%20kebab&hl=es&ved"
            "=2ahUKEwjXk-Llo4TyAhVNgc4BHfcMBnMQMyhNegUIARCDAQ")
    embed.add_field(name="-hola", value="Saluda al bot!", inline=True)
    embed.add_field(name="-nada", value="No hay nada", inline=True)
    embed.add_field(name="-youtube", value="Busca un video en YouTube -> -y, -you", inline=True)
    embed.add_field(name="-users", value="Devuelve el número de usuarios totales del canal -> -u", inline=True)
    embed.add_field(name="-join",
                    value="Hace que el bot entre al canal de voz (no es necesario si usas directamente !play) -> -j",
                    inline=True)
    embed.add_field(name="-leave", value="Hace que el bot salga del canal de voz -> -l", inline=True)
    embed.add_field(name="-play",
                    value="Reproduce una canción e inicializa la cola. Si hay una cola existente, reproduce la "
                          "canción al instante sin modificar la cola. -> -p",
                    inline=True)
    embed.add_field(name="-queue", value="Añade una canción a la cola de reproducción. -> -q", inline=True)
    embed.add_field(name="-skip", value="Pasa a la siguiente canción que haya en la cola de reproducción. -> -s", inline=True)
    embed.add_field(name="-stop", value="Elimina la cola y hace que el Bot pare de hacer lo que esté haciendo.",
                    inline=True)
    embed.add_field(name="-pause", value="Para la reproducción de música.", inline=True)
    embed.add_field(name="-resume", value="Reanuda la reproducción de música.", inline=True)
    embed.set_footer(text="Creado por MizfitZ (ig: @rafaelgc2002)")
    await ctx.send(embed=embed)


@bot.command(aliases=["y", "you"])
async def youtube(ctx, *args):
    url = url_gen(*args)
    await ctx.send(url)


@bot.command(pass_context=True, aliases=["j"])
async def join(ctx):
    global voice
    try:
        canal = ctx.message.author.voice.channel
    except:
        canal = None

    voice = get(bot.voice_clients, guild=ctx.guild)
    if canal is None:
        await ctx.send(f"Si te conectaras a algun canal, sabría donde meterme {ctx.message.author.mention}")
    else:
        if voice is None:
            await canal.connect()
        elif voice.channel == canal:
            await ctx.send(f"Ya estoy conectado al canal puto ciego {ctx.message.author.mention}")
        elif voice and voice.is_connected:
            await voice.move_to(canal)


@bot.command(pass_context=True, aliases=["l"])
async def leave(ctx):
    clients = bot.voice_clients
    voz = get(bot.voice_clients, guild=ctx.guild)
    if voz and voz.is_connected:
        for i in clients:
            if i.guild == ctx.guild:
                await i.disconnect()
    else:
        await ctx.send(f"No estoy conectado a ningún canal puto subnormal {ctx.message.author.mention}")


colas = {}


def check_queue(ctx):
    iden = ctx.guild.id
    lista = colas[iden]
    if len(lista) > 0:
        play_next(ctx)


def play_next(ctx):
    iden = ctx.guild.id
    repro = colas[iden].pop(0)
    nombre = repro.title
    playing_url = url_gen(nombre)
    ctx.voice_client.play(repro, after=lambda x: check_queue(ctx))
    bot.loop.create_task(ctx.send(f"Está sonando este temita: \n{playing_url}"))


@bot.command(pass_context=True, aliases=["p"])
async def play(ctx, *args):
    try:
        canal = ctx.message.author.voice.channel
    except:
        canal = None

    voz = get(bot.voice_clients, guild=ctx.guild)
    link = url_gen(*args)
    player = await player_gen(link)
    iden = ctx.guild.id

    if canal is None:
        await ctx.send(f"Si te conectaras a algun canal, sabría donde meterme {ctx.message.author.mention}")
        return
    else:
        if voz is None:
            await canal.connect()
        elif voz.channel == canal:
            pass
        elif voz and voz.is_connected:
            await voz.move_to(canal)
    lista = [player]
    voz = get(bot.voice_clients, guild=ctx.guild)
    if iden in colas:
        colas[iden] = lista + colas[iden]
        if voz.is_playing():
            parar(ctx)
            return
    else:
        colas[iden] = []
        colas[iden].append(player)
    play_next(ctx)


@bot.command(pass_context=True, aliases=["q"])
async def queue(ctx, *args):
    iden = ctx.guild.id
    url = url_gen(*args)
    player = await player_gen(url)
    if iden in colas:
        colas[iden].append(player)
        await ctx.send(f"Añadido a la cola:\n{url}\n\n por: {ctx.message.author.mention}")
    else:
        await ctx.send(f"No he encontrado ninguna cola a la que añadir tu canción, prueba a usar !p para iniciar una "
                       f"cola {ctx.message.author.mention}")


@bot.command(pass_context=True, aliases=["s"])
async def skip(ctx):
    parar(ctx)
    iden = ctx.guild.id
    if iden in colas:
        if len(colas[iden]) >= 1:
            await ctx.send(f"¿No te gusta esta canción? ¡Pues la paso! {ctx.message.author.mention}")
        else:
            await ctx.send(f"No hay mas canciones en la cola, añade la primera usando el comando !play")
    else:
        await ctx.send(f"No hay ninguna cola, para crearla, usa el comando !play")


@bot.command(pass_context=True)
async def pause(ctx):
    voz = get(bot.voice_clients, guild=ctx.guild)
    if voz.is_playing():
        voz.pause()
    else:
        await ctx.send(f"Como voy a parar algo que no está sonando, hijo mio, {ctx.message.author.mention}")


@bot.command(pass_context=True)
async def resume(ctx):
    voz = get(bot.voice_clients, guild=ctx.guild)
    if voz.is_paused():
        voz.resume()
    else:
        await ctx.send(f"ahora mimo no hay temita sonando ermano, {ctx.message.author.mention}")


@bot.command(pass_context=True)
async def stop(ctx):
    iden = ctx.guild.id
    if iden in colas:
        colas[iden].clear()
        await ctx.send(f"{ctx.message.author.mention} ha borrado la cola de reproducción")
    else:
        pass
    parar(ctx)
    await ctx.send(f"Ya me callo pesao, {ctx.message.author.mention}")


@bot.command(pass_context=True, aliases=["c"])
async def clear(ctx):
    iden = ctx.guild.id
    if iden in colas:
        colas[iden].clear()
        await ctx.send(f"{ctx.message.author.mention} ha borrado la cola de reproducción")
    else:
        await ctx.send(f"No he podido encontrar ninguna cola de reproducción... {ctx.message.author.mention}")


@bot.command(pass_context=True)
async def laura(ctx):
    await ctx.send(
        f"Es la mejor, la mas guapa, tiene las teta mu gorda, es muy divertida y si no la pongo en algun sitio del "
        f"codigo me zumba :( \n \n tambien es mi novia :)")


bot.run(token)

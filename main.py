import os
import discord
import asyncio
import youtube_dl
import functions as f
from discord.utils import get
from discord.ext import commands

PREFIX = '-'
bot = commands.Bot(command_prefix = PREFIX)
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Bot is ready to rock!')

    await bot.change_presence(status = discord.Status.online, 
                              activity = discord.Game('D&D 5e | -help'))


@bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def help(ctx):
    emb = discord.Embed(title = 'Commands list')
    
    emb.add_field(name = '{}clear'.format(PREFIX), value = 'Clearing chat')

    await ctx.send(embed = emb)


@bot.command(pass_content = True)
async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit = amount)  


# @bot.command()
# async def join(ctx):
#     global voice 
#     channel = ctx.message.author.voice.channel
#     voice = get(bot.voice_clients, guild = ctx.guild)

#     if voice and voice.is_connected():
#         await voice.move_to(channel)
#     else:
#         voice = await channel.connect()


@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()


@bot.command(pass_context=True)
async def YoYoPiraka(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)
    
    voice = await channel.connect()
    voice.play(discord.FFmpegPCMAudio('Piraka Rap.mp3'))
        

# @bot.command()
# async def play(ctx, url: str):
#     song_there = os.path.isfile('song.mp3')

#     try:
#         if song_there:
#             os.remove('song.mp3')
#             print('[log] Olf dile deleted')
#     except PermissionError:
#         print('[log] Failure to download file')
    
#     await ctx.send('Please, standby')

#     voice = get(bot.voice_clients, guild = ctx.guild)

#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3', 
#             'preferredquality': '192'
#         }],
#     }

#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         print('[log] Downloading music...')
#         ydl.download([url])

#     for file in os.listdir('./'):
#         if file.endswith('.mp3'):
#             name = file
#             print('[log] Renaming file: {file}')
#             os.rename(file, 'song.mp3')

#     voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, music ended'))
#     voice.source = discord.PCMVolumeTransformer(voice.source)
#     voice.source.volume = 0.07

#     song_name = name.rsplit('-', 2)
#     await ctx.send(f'Now playing: {song_name[0]}')


@bot.command()
async def roll(ctx, arg):
    author = ctx.message.author
    result = f.show_score(arg)
    await ctx.send(f'{result} {author.mention}')


@bot.command()
async def advRoll(ctx, arg):
    author = ctx.message.author
    result = f.advantage_roll(arg)
    await ctx.send(f'{result} {author.mention}')


@bot.command()
async def dadvRoll(ctx, arg):
    author = ctx.message.author
    result = f.disadvantage_roll(arg)
    await ctx.send(f'{result} {author.mention}')


@bot.command()
async def deathRoll(ctx):
    author = ctx.message.author
    result = f.death_roll()
    await ctx.send(f'{result} {author.mention}')


@bot.command()
async def flipCoin(ctx):
    author = ctx.message.author
    result = f.flip_coin()
    await ctx.send(f'{result} {author.mention}')


@bot.command()
async def randParams(ctx):
    author = ctx.message.author
    result = f.rand_params()
    await ctx.send(f'{result} {author.mention}')


token = open('token.txt', 'r').readline()
bot.run(token)

import discord
import youtube_dl
import os
from discord.ext import commands
from discord.utils import get

PREFIX = '-'
bot = commands.Bot(command_prefix = PREFIX)
bot.remove_command('help')


@bot.event
async def on_ready():
    print('BOT connected')

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


@bot.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else: 
        voice = await channel.connect()
        await ctx.send(f'Bot connected to the channel: {channel}')


@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else: 
        voice = await channel.connect()
        await ctx.send(f'Bot disconnected from the channel: {channel}')


token = open('token.txt', 'r').readline()
bot.run(token)
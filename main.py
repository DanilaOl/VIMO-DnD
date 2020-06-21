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


#Checking for connection and setting up bot status
@bot.event
async def on_ready():
    print('Bot is ready to rock!')

    await bot.change_presence(status = discord.Status.online, 
                              activity = discord.Game('D&D 5e | -help'))


#List of bot's commands
@bot.command(pass_context = True)
async def help(ctx):
    emb = discord.Embed(title = 'Commands list')
    
    emb.add_field(name = '{}clear'.format(PREFIX), value = 'Clearing chat')

    await ctx.send(embed = emb)


#Clears last 100 messages
@bot.command(pass_content = True)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit = amount)  


#Kicks user
@bot.command(pass_content = True)
@commands.has_permissions(administrator = True)
async def kick(ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    
    await member.kick(reason = reason)
    await ctx.send(f'User kicked {member.mention}')


#Bans user
@bot.command(pass_content = True)
@commands.has_permissions(administrator = True)
async def ban(ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    
    await member.ban(reason = reason)
    await ctx.send(f'User banned {member.mention}')


#Unbans user
@bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    await ctx.channel.purge(limit = 1)

    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        await ctx.guild.unban(user)
        await ctx.send(f'User unbanned {user.mention}')

        return 


#Leaves voice-chat
@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()


#The most awesome easter-egg in the world XD
@bot.command(pass_context=True)
async def YoYoPiraka(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)
    
    voice = await channel.connect()
    voice.play(discord.FFmpegPCMAudio('Piraka Rap.mp3'))
        

#Rolls dices in xdy format
@bot.command()
async def roll(ctx, arg):
    author = ctx.message.author
    result = f.show_score(arg)
    await ctx.send(f'{result} {author.mention}')


#Rolls dices with advantage
@bot.command()
async def advRoll(ctx, arg):
    author = ctx.message.author
    result = f.advantage_roll(arg)
    await ctx.send(f'{result} {author.mention}')


#Rolls dices with disadvantage
@bot.command()
async def dadvRoll(ctx, arg):
    author = ctx.message.author
    result = f.disadvantage_roll(arg)
    await ctx.send(f'{result} {author.mention}')


#Rolls dices to make a death check
@bot.command()
async def deathRoll(ctx):
    author = ctx.message.author
    result = f.death_roll()
    await ctx.send(f'{result} {author.mention}')


#Flips coin 
@bot.command()
async def flipCoin(ctx):
    author = ctx.message.author
    result = f.flip_coin()
    await ctx.send(f'{result} {author.mention}')


#Generates random parametres for charachter
@bot.command()
async def randParams(ctx):
    author = ctx.message.author
    result = f.rand_params()
    await ctx.send(f'{result} {author.mention}')


token = open('token.txt', 'r').readline()
bot.run(token)

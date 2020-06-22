import os
import discord
import functions as f
import characters as ch
from time import sleep
from discord.utils import get
from discord.ext import commands
from discord import client

PREFIX = '-'
bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command('help')


# Checking for connection and setting up bot status
@bot.event
async def on_ready():
    print('Bot is ready to rock!')

    await bot.change_presence(status=discord.Status.online, 
                              activity=discord.Game('D&D 5e | -help'))


# List of bot's commands
@bot.command(pass_context=True)
async def help(ctx):
    emb = discord.Embed(title='Commands list')
    
    emb.add_field(name='{}clear'.format(PREFIX), value='Clearing chat')

    await ctx.send(embed=emb)


# Clears last 100 messages
@bot.command(pass_content=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)  


# Kicks user
@bot.command(pass_content=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    
    await member.kick(reason=reason)
    await ctx.send(f'User kicked {member.mention}')


# Bans user
@bot.command(pass_content=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit = 1)
    
    await member.ban(reason = reason)
    await ctx.send(f'User banned {member.mention}')


# Unbans user
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    await ctx.channel.purge(limit=1)

    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        await ctx.guild.unban(user)
        await ctx.send(f'User unbanned {user.mention}')

        return 


# Leaves voice-chat
@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()


# The most awesome easter-egg in the world XD
@bot.command(pass_context=True)
async def YoYoPiraka(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    voice = await channel.connect()
    voice.play(discord.FFmpegPCMAudio('Piraka Rap.mp3'))
        

# Rolls dices in xdy format
@bot.command()
async def roll(ctx, arg):
    author = ctx.message.author
    result = f.show_score(arg)
    await ctx.send(f'{result} {author.mention}')


# Rolls dices with advantage
@bot.command()
async def advRoll(ctx, arg):
    author = ctx.message.author
    result = f.advantage_roll(arg)
    await ctx.send(f'{result} {author.mention}')


# Rolls dices with disadvantage
@bot.command()
async def dadvRoll(ctx, arg):
    author = ctx.message.author
    result = f.disadvantage_roll(arg)
    await ctx.send(f'{result} {author.mention}')


# Rolls dices to make a death check
@bot.command()
async def deathRoll(ctx):
    author = ctx.message.author
    successes, failures = 0, 0
    await ctx.send(f'Бросаю кубики для {author.mention}')

    while successes < 3 and failures < 3:
        for i in range(3):
            sleep(1)
            await ctx.send('...')
        sleep(1)
        if f.flip_coin() == 'Орёл':
            await ctx.send(f'Успех {author.mention}')
            successes += 1
        else:
            await ctx.send(f'Провал {author.mention}')
            failures += 1
    sleep(1)
    if successes == 3:
        await ctx.send(f'Поздравляю, ваш персонаж выжил {author.mention}')
    elif failures == 3:
        await ctx.send(f'К сожалению, ваш персонаж погиб {author.mention}')


# Flips coin 
@bot.command()
async def flipCoin(ctx):
    author = ctx.message.author
    result = f.flip_coin()
    await ctx.send(f'{result} {author.mention}')


# Generates random parameters for character
@bot.command()
async def randParams(ctx):
    author = ctx.message.author
    result = f.rand_params()
    await author.send(f'{result}')


# Creates character using your stats
@bot.command()
async def createCharacter(ctx, *args):
    author = ctx.message.author
    await ctx.send(f"{args}")
    if len(args) != 9:
        await ctx.send(f'Передано недостаточно аргументов\n'
                       f'Синтакс команды -createCharacter\n'
                       f'ИмяПерсонажа  Раса Класс Сила Ловкость Телосложение Интеллект Мудрость Харизма\n'
                       f'{author.mention}')

    elif (type(args[0]) is not str) or (type(args[1]) is not str) or (type(args[2]) is not str):
        await ctx.send(f'Неправильный порядок аргументов \n'
                       f'Синтакс команды -createCharacter\n'
                       f'ИмяПерсонажа  Раса Класс Сила Ловкость Телосложение Интеллект Мудрость Харизма\n'
                       f'{author.mention}')

    else:
        output = ch.create_character(*args)
        await author.send(output)


token = open('token.txt', 'r').readline()
bot.run(token)

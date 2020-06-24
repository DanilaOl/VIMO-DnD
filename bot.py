import os
import json
import discord
import config as c
import functions as f
import characters as ch
from time import sleep
from random import randint
from discord.utils import get
from discord.ext import commands
from exceptions import WrongCharacterRace, WrongCharacterClass

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

bot = commands.Bot(command_prefix=c.PREFIX)
bot.remove_command('help')


# Checking for connection and setting up a status
@bot.event
async def on_ready():
    print('Bot is ready to rock!')

    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game('D&D 5e | -help'))


# Adds a role to the user
@bot.event
async def on_raw_reaction_add(ctx):
    if ctx.message_id == c.POST_ID:
        channel = bot.get_channel(ctx.channel_id)
        message = await channel.fetch_message(ctx.message_id)
        member = get(message.guild.members, id=ctx.user_id)

        emoji = str(ctx.emoji)
        role = get(message.guild.roles, id=c.ROLES[emoji])
        admin_role = get(message.guild.roles, id=c.EXCROLE['admin'])
        
        if admin_role in member.roles and len(member.roles) <= (c.MAX_ROLES_PER_USER + 1):
            await member.add_roles(role)
        elif len(member.roles) <= c.MAX_ROLES_PER_USER:
            await member.add_roles(role)
        else:
            await message.remove_reaction(ctx.emoji, member)


# Removes a role from user
@bot.event
async def on_raw_reaction_remove(ctx):
    channel = bot.get_channel(ctx.channel_id)
    message = await channel.fetch_message(ctx.message_id)
    member = get(message.guild.members, id=ctx.user_id)

    emoji = str(ctx.emoji)
    role = get(message.guild.roles, id=c.ROLES[emoji])

    await member.remove_roles(role)


# List of bot's commands
@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    emb = discord.Embed(
        title='Список команд',
        colour=discord.Colour.from_rgb(114, 137, 218)
    )

    emb.add_field(name='{}join'.format(c.PREFIX),
                  value="[Мастер] Только свистните и я появлюсь в голосовом канале!", inline=False)
    
    emb.add_field(name='{}leave'.format(c.PREFIX),
                  value='[Мастер] Оставлю игроков наедине в голосовом канале...', inline=False)
    
    emb.add_field(name='{}play [battle, civil, journey, mystic]'.format(c.PREFIX),
                  value='[Мастер] Бард, сыграй что-нибудь!', inline=False)
    
    emb.add_field(name='{}pause'.format(c.PREFIX),
                  value='[Мастер] Кому-то нужно отойти? Сейчас поставим музыку на паузу!', inline=False)
    
    emb.add_field(name='{}resume'.format(c.PREFIX),
                  value='[Мастер] Ну что ж, игроки, продолжим!', inline=False)
    
    emb.add_field(name='{}stop'.format(c.PREFIX),
                  value='[Мастер] Эй, бард, игрокам не нравится музыка, хватит играть!', inline=False)
    
    emb.add_field(name='{}roll [dy или xdy]'.format(c.PREFIX),
                  value='[Мастер и игроки] Брошу кубик, дабы вершить ваши судьбы!', inline=False)
    
    emb.add_field(name='{}advRoll [dy или xdy]'.format(c.PREFIX),
                  value='[Мастер и игроки] Сделаю бросок с преимуществом', inline=False)
   
    emb.add_field(name='{}dadvRoll [dy or xdy]'.format(c.PREFIX),
                  value='[Мастер и игроки] Сделаю бросок с помехой', inline=False)
    
    emb.add_field(name='{}deathRoll'.format(c.PREFIX),
                  value='[Мастер и игроки] Пройдите испытание смерти и узнайте судьбу Вашего персонажа!', inline=False)
    
    emb.add_field(name='{}flipCoin'.format(c.PREFIX),
                  value='[Мастер и игроки] Сколько уже веков решают вопросы монеткой?', inline=False)
    
    emb.add_field(name='{}randName [race]'.format(c.PREFIX),
                  value='[Мастер и игроки] Давай подберём тебе имя!', inline=False)
    
    emb.add_field(name='{}randParams'.format(c.PREFIX),
                  value='[Мастер и игроки] Не можете подобрать характеристики? Сейчас исправим', inline=False)
    
    emb.add_field(name='{}createCharacter [Имя] [Раса] [Класс] [Сила] [Лов.] [Телосл.] [Инт.] [Мудр.] [Хар.]'.format(c.PREFIX),
                  value='[Мастер и игроки] Как это у тебя нет персонажа? Ничего, сейчас сделаем!', inline=False)
    
    emb.add_field(name='{}clear'.format(c.PREFIX),
                  value='[Администратор и Мастер] Опять они там словоблудят! Эх, снова нужно чистить чат...', inline=False)

    await ctx.send(author.mention, embed=emb)


# Clears last 9999 messages
@bot.command(pass_content=True)
@commands.has_any_role(c.EXCROLE['admin'], c.ROLES['🧙'])
async def clear(ctx, amount=9999):
    await ctx.channel.purge(limit=amount)


# Bans user on server
@bot.command(pass_context=True)
@commands.has_role(c.EXCROLE['admin'])
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)


# Unbans user on server
@bot.command(pass_context=True)
@commands.has_role(c.EXCROLE['admin'])
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user_id

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')

            return


# Kicks user from server
@bot.command(pass_context=True)
@commands.has_role(c.EXCROLE['admin'])
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


# Joins voice channel
@bot.command(pass_context=True)
@commands.has_any_role(c.EXCROLE['admin'], c.ROLES['🧙'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


# leaves voice channel
@bot.command(pass_context=True)
@commands.has_any_role(c.EXCROLE['admin'], c.ROLES['🧙'])
async def leave(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()


# Plays thematic music
@bot.command(pass_context=True)
@commands.has_any_role(c.EXCROLE['admin'], c.ROLES['🧙'])
async def play(ctx, music_theme):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.stop()

    os.chdir(os.path.join(ROOT_DIR, 'music', music_theme))
    track_number = randint(1, f.sum_files())

    voice.play(discord.FFmpegPCMAudio(f'{track_number}.mp3'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.25


# Celebrate success of the battle!
@bot.command(pass_context=True)
@commands.has_any_role(c.EXCROLE['admin'], c.ROLES['🧙'])
async def fanfare(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.stop()

    os.chdir(os.path.join(ROOT_DIR, 'music'))

    voice.play(discord.FFmpegPCMAudio('Fanfare.mp3'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.25


# Pauses music
@bot.command(pass_context=True)
@commands.has_any_role(c.EXCROLE['admin'], c.ROLES['🧙'])
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.pause()


# Resumes music
@bot.command(pass_context=True)
@commands.has_any_role(c.EXCROLE['admin'], c.ROLES['🧙'])
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        voice.resume()


# Stops music
@bot.command(pass_context=True)
@commands.has_any_role(c.EXCROLE['admin'], c.ROLES['🧙'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.stop()


# Rolls dices in xdy format
@bot.command(pass_context=True)
@commands.has_any_role(c.EXCROLE['admin'], c.ROLES['🧙'], c.ROLES['🧝'])
async def roll(ctx, arg):
    author = ctx.message.author
    result = f.show_score(arg)
    await ctx.send(f'{result} {author.mention}')


# Rolls dices with advantage
@bot.command(pass_context=True)
@commands.has_any_role(c.EXCROLE['admin'], c.ROLES['🧙'], c.ROLES['🧝'])
async def advRoll(ctx, arg):
    author = ctx.message.author
    result = f.advantage_roll(arg)
    await ctx.send(f'{result} {author.mention}')


# Rolls dices with disadvantage
@bot.command(pass_context=True)
@commands.has_any_role(c.EXCROLE['admin'], c.ROLES['🧙'], c.ROLES['🧝'])
async def dadvRoll(ctx, arg):
    author = ctx.message.author
    result = f.disadvantage_roll(arg)
    await ctx.send(f'{result} {author.mention}')


# Rolls dices to make a death check
@bot.command(pass_context=True)
@commands.has_any_role(c.EXCROLE['admin'], c.ROLES['🧙'], c.ROLES['🧝'])
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
@bot.command(pass_context=True)
@commands.has_any_role(c.EXCROLE['admin'], c.ROLES['🧙'], c.ROLES['🧝'])
async def flipCoin(ctx):
    author = ctx.message.author
    result = f.flip_coin()
    await ctx.send(f'{result} {author.mention}')


# Creates a random name for character
@bot.command(pass_context=True)
async def randName(ctx, race):
    author = ctx.message.author
    await ctx.send(f'{f.rand_name(race)} {author.mention}')


# Generates random parameters for character
@bot.command(pass_context=True)
async def randParams(ctx):
    author = ctx.message.author
    result = f.rand_params()
    await ctx.send(f'{result} {author.mention}')


# Creates character using your stats
@bot.command(pass_context=True)
@commands.has_any_role(c.EXCROLE['admin'], c.ROLES['🧙'], c.ROLES['🧝'])
async def createCharacter(ctx, *args):
    author = ctx.message.author
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
        try:
            output = ch.create_character(*args)
        except WrongCharacterRace:
            allowed_races = [i for i in json.load(open('race_features.json', 'r', encoding='utf-8'))]
            allowed_races = ', '.join(allowed_races)
            await ctx.send(f'Задана недопустимая раса\n'
                           f'Доступные расы\n'
                           f'{allowed_races} {author.mention}')
        except WrongCharacterClass:
            allowed_classes = [i for i in json.load(open('class_features.json', 'r', encoding='utf-8'))]
            allowed_classes = ', '.join(allowed_classes)
            await ctx.send(f'Задан недопустимый класс\n'
                           f'Доступные классы:\n'
                           f'{allowed_classes} {author.mention}')
        else:
            await author.send(output)


# And here magic begins)
TOKEN = open('token.txt', 'r').readline()
bot.run(TOKEN)

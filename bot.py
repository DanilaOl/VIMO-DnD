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
        try:
            role = get(message.guild.roles, id=c.ROLES[emoji])

            if len([i for i in member.roles if i.id not in c.EXROLES]) <= c.MAX_ROLES_PER_USER:
                await member.add_roles(role)
                print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
            else:
                await message.remove_reaction(ctx.emoji, member)
                print('[ERROR] Too many roles for user {0.display_name}'.format(member))

        except KeyError:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))


# Removes a role from user
@bot.event
async def on_raw_reaction_remove(ctx):
    channel = bot.get_channel(ctx.channel_id)
    message = await channel.fetch_message(ctx.message_id)
    member = get(message.guild.members, id=ctx.user_id)
    emoji = str(ctx.emoji)
    try:
        role = get(message.guild.roles, id=c.ROLES[emoji])

        await member.remove_roles(role)
        print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))

    except KeyError:
        print('[ERROR] KeyError, no role found for ' + emoji)
    except Exception as e:
        print(repr(e))


# List of bot's commands
@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    emb = discord.Embed(
        title='Список команд',
        colour=discord.Colour.from_rgb(114, 137, 218)
    )

    emb.add_field(name='{}play [battle, civil, journey, mystic]'.format(c.PREFIX),
                  value="[Мастер] Включу тематическую музыку для атмосферы", inline=False)
    emb.add_field(name='{}leave'.format(c.PREFIX),
                  value='[Мастер] Оставлю игроков наедине в голосовом канале', inline=False)
    emb.add_field(name='{}roll [dy or xdy]'.format(c.PREFIX),
                  value='[Мастер и игроки] Брошу кубик, дабы вершить ваши судьбы!', inline=False)
    emb.add_field(name='{}advRoll [dy or xdy]'.format(c.PREFIX),
                  value='[Мастер и игроки] Сделаю бросок с преимуществом', inline=False)
    emb.add_field(name='{}dadvRoll [dy or xdy]'.format(c.PREFIX),
                  value='[Мастер и игроки] Сделаю бросок с помехой', inline=False)
    emb.add_field(name='{}deathRoll'.format(c.PREFIX),
                  value='[Мастер и игроки] Пройдите испытание смерти и узнайте судьбу Вашего персонажа!', inline=False)
    emb.add_field(name='{}flipCoin'.format(c.PREFIX),
                  value='[Мастер и игроки] Подбрасывает монетку', inline=False)
    emb.add_field(name='{}randParams'.format(c.PREFIX),
                  value='[Мастер и игроки] Генерирует параметры для персонажа', inline=False)
    emb.add_field(name='{}clear'.format(c.PREFIX),
                  value='[Администратор и Мастер] Очищает тектовый канал от сообщений', inline=False)
    emb.add_field(name="{}ban [user's name]".format(c.PREFIX),
                  value='[Администратор] Казнить, нельзя помиловать!', inline=False)
    emb.add_field(name="{}unban [user's name]".format(c.PREFIX),
                  value='[Администратор] Казнить нельзя, помиловать!', inline=False)
    emb.add_field(name="{}kick [user's name]".format(c.PREFIX),
                  value='[Администратор] Отправлю игрока в одиноное путешествие...', inline=False)

    await ctx.send(author.mention, embed=emb)


# Clears last 100 messages
@bot.command(pass_content=True)
@commands.has_any_role(724400934729416726, 724331608441749656)
async def clear(ctx, amount=9999):
    await ctx.channel.purge(limit=amount)


# Kicks user
@bot.command(pass_content=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User kicked {member.mention}')


# Bans user
@bot.command(pass_content=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User banned {member.mention}')


# Unbans user
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        await ctx.guild.unban(user)
        await ctx.send(f'User unbanned {user.mention}')

        return

    # Plays thematic music


@bot.command(pass_context=True)
@commands.has_any_role(724400934729416726, 724331608441749656)
async def play(ctx, music_theme):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    if music_theme == 'battle':
        if os.getcwd() != 'music/battle':
            os.chdir(f'music/{music_theme}')

        track_number = randint(1, f.sum_files())
        voice.play(discord.FFmpegPCMAudio(f'{track_number}.mp3'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07


@bot.command(pass_context=True)
@commands.has_any_role(724400934729416726, 724331608441749656)
async def stop(ctx):
    channel = ctx.meassage.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)


# Leaves voice chat
@bot.command(pass_context=True)
@commands.has_any_role(724400934729416726, 724331608441749656)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()


# Rolls dices in xdy format
@bot.command(pass_context=True)
@commands.has_any_role(724331608441749656, 724331644944646244)
async def roll(ctx, arg):
    author = ctx.message.author
    result = f.show_score(arg)
    await ctx.send(f'{result} {author.mention}')


# Rolls dices with advantage
@bot.command(pass_context=True)
@commands.has_any_role(724331608441749656, 724331644944646244)
async def advRoll(ctx, arg):
    author = ctx.message.author
    result = f.advantage_roll(arg)
    await ctx.send(f'{result} {author.mention}')


# Rolls dices with disadvantage
@bot.command(pass_context=True)
@commands.has_any_role(724331608441749656, 724331644944646244)
async def dadvRoll(ctx, arg):
    author = ctx.message.author
    result = f.disadvantage_roll(arg)
    await ctx.send(f'{result} {author.mention}')


# Rolls dices to make a death check
@bot.command(pass_context=True)
@commands.has_any_role(724331608441749656, 724331644944646244)
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
@commands.has_any_role(724331608441749656, 724331644944646244)
async def flipCoin(ctx):
    author = ctx.message.author
    result = f.flip_coin()
    await ctx.send(f'{result} {author.mention}')


# Generates random parameters for character
@bot.command(pass_context=True)
@commands.has_any_role(724331608441749656, 724331644944646244)
async def randParams(ctx):
    author = ctx.message.author
    result = f.rand_params()
    await ctx.send(f'{result} {author.mention}')


# Creates character using your stats
@bot.command()
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


@bot.command()
async def randomName(ctx, race):
    author = ctx.message.author
    await ctx.send(f'{f.rand_name(race)} {author.mention}')

bot.run(c.TOKEN)

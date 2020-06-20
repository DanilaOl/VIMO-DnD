import discord
from functions import roll
from discord.ext import commands

bot = commands.Bot(command_prefix = '+')
# client.remove_command('help')

@bot.event
async def on_ready():
    print('BOT connected')

@bot.command()
async def rollDice(ctx, arg):
    author = ctx.message.author
    await ctx.send(f'{arg}, {author.mention}')

bot.run('NzIzNjI1MzQyOTQ1ODUzNTAw.Xu0Www.gjfWD5EIDQT5Eaiv_qXqqf-czfc')
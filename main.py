import discord
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

token = open('token.txt', 'r').readline()
bot.run(token)
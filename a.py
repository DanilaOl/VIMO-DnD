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
#       TODO: delete character from file

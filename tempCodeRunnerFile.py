
async def clear(ctx, amount=9999):
    await ctx.channel.purge(limit=amount)
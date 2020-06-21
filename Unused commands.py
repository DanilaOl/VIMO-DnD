@bot.command()
async def play(ctx, url: str):
    song_there = os.path.isfile('song.mp3')

    try:
        if song_there:
            os.remove('song.mp3')
            print('[log] Olf dile deleted')
    except PermissionError:
        print('[log] Failure to download file')
    
    await ctx.send('Please, standby')

    voice = get(bot.voice_clients, guild = ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3', 
            'preferredquality': '192'
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('[log] Downloading music...')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print('[log] Renaming file: {file}')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, music ended'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    song_name = name.rsplit('-', 2)
    await ctx.send(f'Now playing: {song_name[0]}')
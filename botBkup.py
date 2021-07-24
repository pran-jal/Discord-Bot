#Discord Voice Assistent 
#Permissions = 36715520

import os
import random
import discord
from discord.ext import commands
import key

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '', intents=intents)

textchannel = 0
voicechannel = 0

@client.event
async def on_ready():
    global textchannel, voicechannel
    a=1
    b=1
    print(f'We have logged in as {client.user.name}')
    for guild in client.guilds:
        for channel in guild.channels:
            if str(channel.type) == 'text' and a:
                textchannel = channel.id
                a=0
            elif str(channel.type) == 'voice' and b:
                voicechannel = channel.id
                b=0
    channel = client.get_channel(textchannel)
    await channel.send('Bot Online', tts=True)

@client.event
async def on_member_join(member):
    channel = client.get_channel(textchannel)
    await channel.send(f'Hello!, {member.name} welcome', tts=True)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('hi') :
        await message.channel.send(f'Hello! {message.author.name}', tts=True)
    else :
        await client.process_commands(message)

@client.event
async def on_voice_state_update(member, before, after):
    channel = client.get_channel(textchannel)
    if before.channel is not None and after.channel is None:
        msg = 'left'
    elif before.channel is None and after.channel is not None:
        msg = 'joined'
    await channel.send(f'{member.name} has {msg} the voice', tts=True)


@client.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        vc=await ctx.message.author.voice.channel.connect()
        print(list(vc))
    elif voicechannel:
        channel = client.get_channel(voicechannel)
        await channel.connect()
    else:
        await ctx.send('Failed to Join. Join a voice channel and try again')

@client.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send('I am not in voice')

@client.command(pass_context=True)
async def song(ctx):
    i=random.randrange(1,18)
    if ctx.message.author.voice.channel != None:
        vc = await ctx.message.author.voice.channel.connect()
    elif ctx.author.voice:
        vc = discord.voice_client.VoiceClient
    
    if vc:
        source=f"C:\\Users\\Pranjal\\Documents\\VS Code\\Python\\Discord Bot\\{i}.mp3"
        i.clear()
        executable="C:/ffmpeg/ffmpeg.exe"
        vc.play(discord.FFmpegPCMAudio(executable=executable,source=source, after=None))
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")

 


client.run(key.token)

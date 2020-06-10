import discord
import os
from configparser import ConfigParser
from discord.ext import commands, tasks
from itertools import cycle



config = ConfigParser()
config.read('config.ini', encoding="utf8")
prefix = config["setting"]["prefix"]
owners = config["setting"]["owners"]
sangte = config["setting"]["sangte"]



colour = discord.Colour.blue()
status = cycle([f'{prefix}도움', sangte])


client = commands.Bot(command_prefix=prefix)
client.remove_command('help')



@client.command(name="로드")
async def load(ctx, extension):
    if not ctx.author.id == int(owners):
        return
    else:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f":white_check_mark: {extension}을(를) 로드했습니다!")

@client.command(name="언로드")
async def unload(ctx, extension):
    if not ctx.author.id == int(owners):
        return
    else:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f":white_check_mark: {extension}을(를) 언로드했습니다!")

@client.command(name="리로드")
async def reload_commands(ctx, extension=None):
    if not ctx.author.id == int(owners):
        return
    else:
        if extension is None: # extension이 None이면 (그냥 !리로드 라고 썼을 때)
            for filename in os.listdir("cogs"):
                if filename.endswith(".py"):
                    client.unload_extension(f"cogs.{filename[:-3]}")
                    client.load_extension(f"cogs.{filename[:-3]}")
                    await ctx.send(":white_check_mark: 모든 명령어를 다시 불러왔습니다!")
        else:
            client.unload_extension(f"cogs.{extension}")
            client.load_extension(f"cogs.{extension}")
            await ctx.send(f":white_check_mark: {extension}을(를) 다시 불러왔습니다!")


for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

 
@client.event
async def on_ready():
    print("다음으로 로그인합니다")
    print(client.user.name)
    print(client.user.id)
    print('Discord.py 버전 : ' + discord.__version__)
    print("bot starting..")#봇 시작이라고 뜨게하기
    print("==========")
    guilds_count = len(client.guilds)
    members_count = 0

    for guild in client.guilds:
        members_count += len(guild.members)
    print("서버 수: " + str(guilds_count))
    print("멤버 수: " + str(members_count))
    change_status.start()

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))






access_token = os.environ["BOT_TOKEN"]
client.run(access_token)

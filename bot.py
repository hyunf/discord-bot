import asyncio  # 임포트할 모듈 임포트
import discord
import os
import datetime
from discord.ext import commands



colour = discord.Colour.blue()



client = commands.Bot(command_prefix='!')



async def bt(games):
    await client.wait_until_ready()

    while not client.is_closed():
        for g in games:
            await client.change_presence(status = discord.Status.online, activity = discord.Game(g))
            await asyncio.sleep(10)


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
    await bt(['!도움', '많이 이용해주세요', '문의는 한동준#7109'])




@client.command(name="도움", pass_context=True)
async def help(ctx):
    embed = discord.Embed(title='명령어 모음집', colour=colour)
    embed.set_thumbnail(url="http://file3.instiz.net/data/file3/2018/03/14/6/5/0/650677eed1348016f364df5e563fd378.jpg")
    embed.set_author(name="한동준이 만듬")
    embed.add_field(name="!헬프", value="봇이 할수있는것을 보여줍니다.", inline=False)
    embed.add_field(name="!핑", value="핑을 보여줍니다.", inline=False)
    embed.add_field(name="!정보", value="자신의 정보를 보여줍니다.", inline=False)
    embed.add_field(name="!서버정보", value="서버정보를 보여줍니다.", inline=False)
    embed.add_field(name="!시간", value="호스팅 지역의 년, 월, 일, 시간, 분, 초를 알려줍니다.", inline=False)
    embed.add_field(name='!코로나', value='한국의 코로나 바이러스 현황을 알려줍니다.', inline=False)
    embed.add_field(name='!영화순위', value='영화를 1~20순위로 나눈 영화순위를 보여줍니다.', inline=False)
    embed.add_field(name='!검색', value='네이버에서 블로그를 목록을 검색합니다.', inline=False)
    embed.add_field(name='!한영번역', value='한국어를 영어로 번역합니다.', inline=False)
    embed.add_field(name='!영한번역', value='영어를 한국어로 번역합니다.', inline=False)
    embed.add_field(name='!롤전적', value='롤전적을 보여줍니다.', inline=False)
    embed.add_field(name='!노래순위', value='멜론차트를 모여줍니다.', inline=False)
    embed.add_field(name='!실검', value='네이버 실검을보여줍니다 \n 연관성에 따라 다르게 나올수있습니다', inline=False)
    embed.add_field(name='!인증', value='사람임을 인증합니다. 재미용', inline=False)
    embed.add_field(name='!청소', value='메시지를 청소합니다. (관리자)', inline=False)
    embed.add_field(name='!킥', value='맨션한 사람을 추방시킵니다. (관리자)', inline=False)
    embed.add_field(name='!밴', value='맨션한 사람을 밴시킵니다. (관리자)', inline=False)
    embed.add_field(name='!언밴', value='이름#아이디를 하시면 언밴 시킵니다. (관리자)', inline=False)
    embed.add_field(name='!뮤트', value='유저를 뮤트시킵니다. Muted라는 역할이 있서야 작동합니다. \n Muted역할은 뮤트의 기능을 추가해주세요 (관리자)', inline=False)
    embed.add_field(name='!언뮤트', value='유저를 언뮤트 시킵니다. (관리자)', inline=False)
    embed.add_field(name='봇 개발자 : 한동준#7109',
                    value='초대링크 : https://discord.com/oauth2/authorize?client_id=695546577263132674&scope=bot&permissions=1945201982',
                    inline=False)
    embed.set_footer(text="저작권은 한동준에게 있음")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.author.send(embed=embed)
    embed = discord.Embed(title='도움말이 DM 으로 전송되었습니다.', colour=colour)
    await ctx.send(embed=embed)




access_token = os.environ["BOT_TOKEN"]
client.run(access_token)

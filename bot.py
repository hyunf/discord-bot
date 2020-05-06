import asyncio  # 임포트할 모듈 임포트
import discord
import bs4
import os
import datetime
import re
import urllib
import urllib.request
import warnings
import json
import requests
import requests as rq
import youtube_dl
from captcha.image import ImageCaptcha
import random
from discord.ext import commands
from urllib.request import HTTPError
from discord.utils import get
from urllib.parse import quote
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs




#Naver Open API application ID
access_id = os.environ["ID"]
client_id = access_id
#Naver Open API application token
access_secret = os.environ["SECRET"]
client_secret = access_secret
colour = discord.Colour.blue()



client = commands.Bot(command_prefix='!')


# for lolplayersearch
tierScore = {
    'default' : 0,
    'iron' : 1,
    'bronze' : 2,
    'silver' : 3,
    'gold' : 4,
    'platinum' : 5,
    'diamond' : 6,
    'master' : 7,
    'grandmaster' : 8,
    'challenger' : 9
}
def tierCompare(solorank,flexrank):
    if tierScore[solorank] > tierScore[flexrank]:
        return 0
    elif tierScore[solorank] < tierScore[flexrank]:
        return 1
    else:
        return 2
warnings.filterwarnings(action='ignore')
bot = commands.Bot(command_prefix='!')

opggsummonersearch = 'https://www.op.gg/summoner/userName='


def deleteTags(htmls):
    for a in range(len(htmls)):
        htmls[a] = re.sub('<.+?>','',str(htmls[a]),0).strip()
    return htmls

async def bt(games):
    await client.wait_until_ready()

    while not client.is_closed():
        for g in games:
            await client.change_presence(status = discord.Status.online, activity = discord.Game(g))
            await asyncio.sleep(10)




@client.event
async def on_ready():
    print("다음으로 로그인합니다")
    print(client.user.name)
    print(client.user.id)
    print('Discord.py 버전 : ' + discord.__version__)
    print("bot starting..")#봇 시작이라고 뜨게하기
    print("==========")
    await bt(['!헬프', '많이 이용해주세요', '문의는 한동준#7109'])





@client.command(name="헬프", pass_context=True)
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
    embed.add_field(name='!실검', value='네이버 실검을보여줍니다 \n 연관성에 따라  다르게 나올수있습니다', inline=False)
    embed.add_field(name='!인증', value='사람임을 인증합니다. 재미용', inline=False)
    embed.add_field(name='!인벤', value='인벤의 주요뉴스를 보여줍니다.', inline=False)
    embed.add_field(name='!청소', value='메시지를 청소합니다. (관리자)', inline=False)
    embed.add_field(name='!킥', value='맨션한 사람을 추방시킵니다. (관리자)', inline=False)
    embed.add_field(name='!밴', value='맨션한 사람을 밴시킵니다. (관리자)', inline=False)
    embed.add_field(name='!언밴', value='이름#아이디를 하시면 언밴 시킵니다. (관리자)', inline=False)
    embed.add_field(name='!뮤트', value='유저를 뮤트시킵니다. Muted라는 역할이 있서야 작동합니다. \n Muted역할은 뮤트의 기능을 추가해주세요 (관리자)', inline=False)
    embed.add_field(name='!언뮤트', value='유저를 언뮤트 시킵니다. (관리자)', inline=False)
    embed.add_field(name='봇 개발자 : 한동준#7109', value='초대링크 : https://discord.com/oauth2/authorize?client_id=695546577263132674&scope=bot&permissions=1945201982', inline=False)
    embed.set_footer(text="저작권은 한동준에게 있음")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.author.send(embed=embed)
    embed = discord.Embed(title='도움말이 DM 으로 전송되었습니다.', colour=colour)
    await ctx.send(embed=embed)
    

@client.command(name="인증", pass_context=True)
async def certification(ctx):
    Image_captcha = ImageCaptcha()
    a = ""
    for i in range(6):
        a += str(random.randint(0, 9))

    name = str(ctx.author.id) + ".png"
    Image_captcha.write(a, name)

    await ctx.send(file=discord.File(name))

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        msg = await client.wait_for("message", timeout=60, check=check)
    except:
        await ctx.send("시간초과입니다.")
        return

    if msg.content == a:
        await ctx.send("정답입니다.")
    else:
        await ctx.send("오답입니다.")


@client.command(name="인벤", pass_context=True)
async def inven(ctx):
    embed = discord.Embed(
        title="인벤 주요뉴스",
        colour=colour
    )
    targetSite = 'http://www.inven.co.kr/webzine/news/?hotnews=1'

    header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    melonrqRetry = rq.get(targetSite, headers=header)
    melonht = melonrqRetry.text
    melonsp = bs(melonht, 'html.parser')
    artists = melonsp.findAll('span', {'class': 'title'})
    titles = melonsp.findAll('span', {'class': 'summary'})
    for i in range(len(titles)):
        artist = artists[i].text.strip()
        title = titles[i].text.strip()
        embed.add_field(name="{0:3d}".format(i+1), value='제목:{0} - 내용:{1}'.format(artist,title), inline=False)
        embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@client.command(name="노래순위", pass_context=True)
async def music(ctx):
    embed = discord.Embed(
        title="노래순위",
        description="노래순위입니다.",
        colour=colour
    )
    targetSite = 'https://www.melon.com/chart/index.htm'

    header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    melonrqRetry = rq.get(targetSite, headers=header)
    melonht = melonrqRetry.text
    melonsp = bs(melonht, 'html.parser')
    artists = melonsp.findAll('span', {'class': 'checkEllipsis'})
    titles = melonsp.findAll('div', {'class': 'ellipsis rank01'})
    for i in range(len(titles)):
        artist = artists[i].text.strip()
        title = titles[i].text.strip()
        embed.add_field(name="{0:3d}위".format(i+1), value='{0} - {1}'.format(artist,title), inline=False)
        embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)
    
    
@client.command(name="실검", pass_context=True)
async def sc(ctx):
    embed = discord.Embed(
        title="실시간 검색어",
        description="실시간 검색어입니다.",
        colour=colour
    )
    targetSite = 'https://datalab.naver.com/keyword/realtimeList.naver?groupingLevel=3&where=main'
    header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    source = rq.get(targetSite, headers=header).text
    soup = BeautifulSoup(source, "html.parser")
    hotKeys = soup.select("span.item_title")
    index = 0
    for key in hotKeys:
        index += 1
        embed.add_field(name="{}위".format(index), value=key.text, inline=False)
    await ctx.send(embed=embed)





@client.command(name="롤전적", pass_context=True)
async def displayembed(ctx, *, playerNickname):
    checkURLBool = urlopen(opggsummonersearch + quote(playerNickname))
    bs = BeautifulSoup(checkURLBool, 'html.parser')

    # 자유랭크 언랭은 뒤에 '?image=q_auto&v=1'표현이없다
    RankMedal = bs.findAll('img', {
        'src': re.compile('\/\/[a-z]*\-[A-Za-z]*\.[A-Za-z]*\.[A-Za-z]*\/[A-Za-z]*\/[A-Za-z]*\/[a-z0-9_]*\.png')})
    # index 0 : Solo Rank
    # index 1 : Flexible 5v5 rank

    # for mostUsedChampion
    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})

    # 솔랭, 자랭 둘다 배치가 안되어있는경우 -> 사용된 챔피언 자체가 없다. 즉 모스트 챔피언 메뉴를 넣을 필요가 없다.

    if len(playerNickname) == 1:
        embed = discord.Embed(title="소환사 이름이 입력되지 않았습니다!", description="", color=colour)
        embed.add_field(name="Summoner name not entered",
                        value="To use command !롤전적 : !롤전적 (Summoner Nickname)", inline=False)
        await ctx.send("Error : Incorrect command usage ", embed=embed)

    elif len(deleteTags(bs.findAll('h2', {'class': 'Title'}))) != 0:
        embed = discord.Embed(title="존재하지 않는 소환사", description="", color=colour)
        embed.add_field(name="해당 닉네임의 소환사가 존재하지 않습니다.", value="소환사 이름을 확인해주세요", inline=False)
        await ctx.send("Error : Non existing Summoner ", embed=embed)
    else:
        try:
            # Scrape Summoner's Rank information
            # [Solorank,Solorank Tier]
            solorank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {'class': {'RankType', 'TierRank'}}))
            # [Solorank LeaguePoint, Solorank W, Solorank L, Solorank Winratio]
            solorank_Point_and_winratio = deleteTags(
                bs.findAll('span', {'class': {'LeaguePoints', 'wins', 'losses', 'winratio'}}))
            # [Flex 5:5 Rank,Flexrank Tier,Flextier leaguepoint + W/L,Flextier win ratio]
            flexrank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {
                'class': {'sub-tier__rank-type', 'sub-tier__rank-tier', 'sub-tier__league-point',
                          'sub-tier__gray-text'}}))
            # ['Flextier W/L]
            flexrank_Point_and_winratio = deleteTags(bs.findAll('span', {'class': {'sub-tier__gray-text'}}))

            # embed.set_imag()는 하나만 들어갈수 있다.

            # 솔랭, 자랭 둘다 배치 안되어있는 경우 -> 모스트 챔피언 출력 X
            if len(solorank_Point_and_winratio) == 0 and len(flexrank_Point_and_winratio) == 0:
                embed = discord.Embed(title="소환사 전적검색", description="", color=colour)
                embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                inline=False)
                embed.add_field(name="Ranked Solo : Unranked", value="Unranked", inline=False)
                embed.add_field(name="Flex 5:5 Rank : Unranked", value="Unranked", inline=False)
                embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                await ctx.send("소환사 " + playerNickname + "님의 전적", embed=embed)

            # 솔로랭크 기록이 없는경우
            elif len(solorank_Point_and_winratio) == 0:

                # most Used Champion Information : Champion Name, KDA, Win Rate
                mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                mostUsedChampion = mostUsedChampion.a.text.strip()
                mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]
                embed = discord.Embed(title="소환사 전적검색", description="", color=colour)
                embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                inline=False)
                embed.add_field(name="Ranked Solo : Unranked", value="Unranked", inline=False)
                embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                value="KDA : " + mostUsedChampionKDA + " / " + " WinRate : " + mostUsedChampionWinRate,
                                inline=False)
                embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
                await ctx.send("소환사 " + playerNickname + "님의 전적", embed=embed)

            # 자유랭크 기록이 없는경우
            elif len(flexrank_Point_and_winratio) == 0:

                # most Used Champion Information : Champion Name, KDA, Win Rate
                mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                mostUsedChampion = mostUsedChampion.a.text.strip()
                mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                    1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                embed = discord.Embed(title="소환사 전적검색", description="", color=colour)
                embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                inline=False)
                embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                embed.add_field(name="Flex 5:5 Rank : Unranked", value="Unranked", inline=False)
                embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                value="KDA : " + mostUsedChampionKDA + " / " + "WinRate : " + mostUsedChampionWinRate,
                                inline=False)
                embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                await ctx.send("소환사 " + playerNickname + "님의 전적", embed=embed)
            # 두가지 유형의 랭크 모두 완료된사람
            else:
                # 더 높은 티어를 thumbnail에 안착
                solorankmedal = RankMedal[0]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')
                flexrankmedal = RankMedal[1]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')

                # Make State
                SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                    1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]

                # most Used Champion Information : Champion Name, KDA, Win Rate
                mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                mostUsedChampion = mostUsedChampion.a.text.strip()
                mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                cmpTier = tierCompare(solorankmedal[0], flexrankmedal[0])
                embed = discord.Embed(title="소환사 전적검색", description="", color=colour)
                embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                inline=False)
                embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                value="KDA : " + mostUsedChampionKDA + " / " + " WinRate : " + mostUsedChampionWinRate,
                                inline=False)
                if cmpTier == 0:
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                elif cmpTier == 1:
                    embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
                else:
                    if solorankmedal[1] > flexrankmedal[1]:
                        embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    elif solorankmedal[1] < flexrankmedal[1]:
                        embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    else:
                        embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                await ctx.send("소환사 " + playerNickname + "님의 전적", embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="소환사 전적검색 실패", description="", color=colour)
            embed.add_field(name="", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
            await ctx.send("Wrong Summoner Nickname")

        except UnicodeEncodeError as e:
            embed = discord.Embed(title="소환사 전적검색 실패", description="", color=colour)
            embed.add_field(name="???", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
            await ctx.send("Wrong Summoner Nickname", embed=embed)


@client.command(name="한영번역", pass_context=True)
async def translation(ctx, *, trsText):
    baseurl = "https://openapi.naver.com/v1/papago/n2mt"
    try:
        if len(trsText) == 1:
            await ctx.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
        else:
            combineword = ""
            for word in trsText:
                combineword += "" + word
            # if entered value is sentence, assemble again and strip blank at both side
            savedCombineword = combineword.strip()
            combineword = quote(savedCombineword)
            print(combineword)
            # Make Query String.
            dataParmas = "source=ko&target=en&text=" + combineword
            # Make a Request Instance
            request = Request(baseurl)
            # add header to packet
            request.add_header("X-Naver-Client-Id", client_id)
            request.add_header("X-Naver-Client-Secret", client_secret)
            response = urlopen(request, data=dataParmas.encode("utf-8"))

            responsedCode = response.getcode()
            if (responsedCode == 200):
                response_body = response.read()
                # response_body -> byte string : decode to utf-8
                api_callResult = response_body.decode('utf-8')
                # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                api_callResult = json.loads(api_callResult)
                # Final Result
                translatedText = api_callResult['message']['result']["translatedText"]
                embed = discord.Embed(title="한국어 -> 영어", description="", color=colour)
                embed.add_field(name="한국어", value=savedCombineword, inline=False)
                embed.add_field(name="영어", value=translatedText, inline=False)
                embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                await ctx.send("번역 완료", embed=embed)
            else:
                await ctx.send("Error Code : " + responsedCode)
    except HTTPError as e:
        await ctx.send("Translate Failed. HTTPError Occured.")

@client.command(name="영한번역", pass_context=True)
async def displayembed(ctx, *, trsText):
    baseurl = "https://openapi.naver.com/v1/papago/n2mt"
    try:
        if len(trsText) == 1:
            await ctx.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
        else:
            combineword = ""
            for word in trsText:
                combineword += "" + word
            # if entered value is sentence, assemble again and strip blank at both side
            savedCombineword = combineword.strip()
            combineword = quote(savedCombineword)
            # Make Query String.
            dataParmas = "source=en&target=ko&text=" + combineword
            # Make a Request Instance
            request = Request(baseurl)
            # add header to packet
            request.add_header("X-Naver-Client-Id", client_id)
            request.add_header("X-Naver-Client-Secret", client_secret)
            response = urlopen(request, data=dataParmas.encode("utf-8"))

            responsedCode = response.getcode()
            if (responsedCode == 200):
                response_body = response.read()
                # response_body -> byte string : decode to utf-8
                api_callResult = response_body.decode('utf-8')

                # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                api_callResult = json.loads(api_callResult)
                # Final Result
                translatedText = api_callResult['message']['result']["translatedText"]
                embed = discord.Embed(title="영어 -> 한국어", description="", color=colour)
                embed.add_field(name="영어", value=savedCombineword, inline=False)
                embed.add_field(name="한국어", value=translatedText, inline=False)
                embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")
                await ctx.send("번역 완료", embed=embed)
            else:
                await ctx.send("Error Code : " + responsedCode)
    except HTTPError as e:
        await ctx.send("Translate Failed. HTTPError Occured.")




@client.command(name="핑", pass_context=True)
async def ping(ctx):
    embed = discord.Embed(title="핑(ms)", colour=discord.Colour.blue())
    embed.add_field(name="퐁", value="{0}ms".format(client.latency * 1000), inline=False)
    await ctx.send(embed=embed)

@client.command(name="정보", pass_context=True)
async def information(ctx):
    date = datetime.datetime.utcfromtimestamp(((int(ctx.author.id) >> 22) + 1420070400000) / 1000)
    embed = discord.Embed(color=colour)
    embed.add_field(name="이름", value=ctx.author.name, inline=False)
    embed.add_field(name="서버닉네임", value=ctx.author.display_name, inline=False)
    embed.add_field(name="가입일", value=str(date.year) + "년" + str(date.month) + "월" + str(date.day) + "일", inline=False)
    embed.add_field(name="아이디", value=ctx.author.id, inline=False)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@client.command(name="시간", pass_context=True)
async def time(ctx):
    embed = discord.Embed(color=colour)
    a = datetime.datetime.today().year
    b = datetime.datetime.today().month
    c = datetime.datetime.today().day
    d = datetime.datetime.today().hour
    e = datetime.datetime.today().minute
    f = datetime.datetime.today().second
    embed.add_field(name="년", value=str(a) + "년", inline=True)
    embed.add_field(name="월", value=str(b) + "월", inline=True)
    embed.add_field(name="일", value=str(c) + "일", inline=True)
    embed.add_field(name="시간", value=str(d) + "시간", inline=True)
    embed.add_field(name="분", value=str(e) + "분", inline=True)
    embed.add_field(name="초", value=str(f) + "초", inline=True)
    await ctx.send(embed=embed)

@client.command(name="서버정보", pass_context=True)
async def serverinformation(ctx):
    embed = discord.Embed(colour=colour)
    embed.add_field(name="서버 이름", value=ctx.guild.name, inline=False)
    embed.add_field(name="서버 아이디", value=ctx.guild.id, inline=False)
    embed.add_field(name="서버 지역", value=str(ctx.guild.region).title(), inline=False)
    embed.add_field(name="서버 주인", value=ctx.guild.owner.display_name, inline=False)
    embed.add_field(name="서버 만들어진 날짜", value=ctx.guild.created_at.strftime("%y/%m/%d %H:%M:%S"), inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)



@client.command(name="영화순위", pass_context=True)
async def movie(ctx):
    # http://ticket2.movie.daum.net/movie/movieranklist.aspx
    i1 = 0  # 랭킹 string값
    embed = discord.Embed(
        title="영화순위",
        description="영화순위입니다.",
        colour=colour
    )
    hdr = {'User-Agent': 'Mozilla/5.0'}
    url = 'http://ticket2.movie.daum.net/movie/movieranklist.aspx'
    req = Request(url, headers=hdr)
    html = urllib.request.urlopen(req)
    bsObj = bs4.BeautifulSoup(html, "html.parser")
    moviechartBase = bsObj.find('div', {'class': 'main_detail'})
    moviechart1 = moviechartBase.find('ul', {'class': 'list_boxthumb'})
    moviechart2 = moviechart1.find_all('li')
    for i in range(0, 20):
        i1 = i1 + 1
        stri1 = str(i1)  # i1은 영화랭킹을 나타내는데 사용됩니다
        moviechartLi1 = moviechart2[i]  # ------------------------- 1등랭킹 영화---------------------------
        moviechartLi1Div = moviechartLi1.find('div', {'class': 'desc_boxthumb'})  # 영화박스 나타내는 Div
        moviechartLi1MovieName1 = moviechartLi1Div.find('strong', {'class': 'tit_join'})
        moviechartLi1MovieName = moviechartLi1MovieName1.text.strip()  # 영화 제목
        moviechartLi1Ratting1 = moviechartLi1Div.find('div', {'class': 'raking_grade'})
        moviechartLi1Ratting2 = moviechartLi1Ratting1.find('em', {'class': 'emph_grade'})
        moviechartLi1Ratting = moviechartLi1Ratting2.text.strip()  # 영화 평점
        moviechartLi1openDay1 = moviechartLi1Div.find('dl', {'class': 'list_state'})
        moviechartLi1openDay2 = moviechartLi1openDay1.find_all('dd')  # 개봉날짜, 예매율 두개포함한 dd임
        moviechartLi1openDay3 = moviechartLi1openDay2[0]
        moviechartLi1Yerating1 = moviechartLi1openDay2[1]
        moviechartLi1openDay = moviechartLi1openDay3.text.strip()  # 개봉날짜
        moviechartLi1Yerating = moviechartLi1Yerating1.text.strip()  # 예매율 ,랭킹변동
        embed.add_field(name='---------------랭킹' + stri1 + '위---------------',
                        value='\n영화제목 : ' + moviechartLi1MovieName + '\n영화평점 : ' + moviechartLi1Ratting + '점' + '\n개봉날짜 : ' + moviechartLi1openDay + '\n예매율,랭킹변동 : ' + moviechartLi1Yerating,
                        inline=False)  # 영화랭킹
        embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)


@client.command(name="코로나", pass_context=True)
async def corona19(ctx):
    # 보건복지부 코로나 바이러스 정보사이트"
    covidSite = "http://ncov.mohw.go.kr/index.jsp"
    covidNotice = "http://ncov.mohw.go.kr"
    html = urlopen(covidSite)
    bs = BeautifulSoup(html, 'html.parser')
    latestupdateTime = bs.find('span', {'class': "livedate"}).text.split(',')[0][1:].split('.')
    statisticalNumbers = bs.findAll('span', {'class': 'num'})
    beforedayNumbers = bs.findAll('span', {'class': 'before'})

    # 주요 브리핑 및 뉴스링크
    briefTasks = []
    mainbrief = bs.findAll('a', {'href': re.compile('\/tcmBoardView\.do\?contSeq=[0-9]*')})
    for brf in mainbrief:
        container = []
        container.append(brf.text)
        container.append(covidNotice + brf['href'])
        briefTasks.append(container)

    # 통계수치
    statNum = []
    # 전일대비 수치
    beforeNum = []
    for num in range(7):
        statNum.append(statisticalNumbers[num].text)
    for num in range(4):
        beforeNum.append(beforedayNumbers[num].text.split('(')[-1].split(')')[0])

    totalPeopletoInt = statNum[0].split(')')[-1].split(',')
    tpInt = ''.join(totalPeopletoInt)
    lethatRate = round((int(statNum[3]) / int(tpInt)) * 100, 2)
    embed = discord.Embed(title="Covid-19 Virus Korea Status", description="", color=colour)
    embed.add_field(name="Data source : Ministry of Health and Welfare of Korea",
                    value="http://ncov.mohw.go.kr/index.jsp", inline=False)
    embed.add_field(name="Latest data refred time",
                    value="해당 자료는 " + latestupdateTime[0] + "월 " + latestupdateTime[1] + "일 " + latestupdateTime[
                        2] + " 자료입니다.", inline=False)
    embed.add_field(name="확진환자(누적)", value=statNum[0].split(')')[-1] + "(" + beforeNum[0] + ")", inline=True)
    embed.add_field(name="완치환자(격리해제)", value=statNum[1] + "(" + beforeNum[1] + ")", inline=True)
    embed.add_field(name="치료중(격리 중)", value=statNum[2] + "(" + beforeNum[2] + ")", inline=True)
    embed.add_field(name="사망", value=statNum[3] + "(" + beforeNum[3] + ")", inline=True)
    embed.add_field(name="누적확진률", value=statNum[6], inline=True)
    embed.add_field(name="치사율", value=str(lethatRate) + " %", inline=True)
    embed.add_field(name="- 최신 브리핑 1 : " + briefTasks[0][0], value="Link : " + briefTasks[0][1], inline=False)
    embed.add_field(name="- 최신 브리핑 2 : " + briefTasks[1][0], value="Link : " + briefTasks[1][1], inline=False)
    embed.set_thumbnail(url="https://wikis.krsocsci.org/images/7/79/%EB%8C%80%ED%95%9C%EC%99%95%EA%B5%AD_%ED%83%9C%EA%B7%B9%EA%B8%B0.jpg")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send("Covid-19 Virus Korea Status", embed=embed)


@client.command(name="검색")
async def _search_blog(ctx, *, search_query):
    temp = 0
    url_base = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query="
    url = url_base + urllib.parse.quote(search_query)
    title = ["", "", ""] # 더 많은 검색 : 빈칸("")을 늘리셔야 합니다.
    link = ["", "", ""] # 더 많은 검색 : 빈칸("")을 늘리셔야 합니다.
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
    result = soup.find_all('a', "sh_blog_title _sp_each_url _sp_each_title")
    embed = discord.Embed(title="검색 결과", description=" ", color=colour)
    for n in result:
        if temp == 3: # 더 많은 검색 : 숫자(3)를 늘리셔야 합니다.
            break
        title[temp] = n.get("title")
        link[temp] = n.get("href")
        embed.add_field(name=title[temp], value=link[temp], inline=False)
        temp+=1
    embed.set_footer(text="검색 완료!")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)





@client.command(name="청소")
@commands.has_permissions(administrator=True)
async def _clear(ctx, number):
    number = int(number) # Converting the amount of messages to delete to an integer
    await ctx.channel.purge(limit=number + 1)
    embed = discord.Embed(title="{}개를 삭제하였습니다.".format(number), colour=colour)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)




@_clear.error
async def _clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author), colour=colour)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


@client.command(name="킥")
@commands.has_permissions(kick_members=True)
async def _kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(title=str(member)+"을(를) 킥하였습니다.", colour=colour)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)
    




@_kick.error
async def _kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author), colour=colour)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@client.command(name="밴")
@commands.has_permissions(ban_members=True)
async def _ban(ctx, member : discord.Member):
    await member.ban()
    embed = discord.Embed(title=str(member) + "을(를) 밴시켰습니다.", colour=colour)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@_ban.error
async def _ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author), colour=colour)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@client.command(name="언밴", pass_context=True)
@commands.has_permissions(ban_members=True)
async def _unban(ctx, *, user_name):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = user_name.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed = discord.Embed(title=f"{user.mention}을(를) 언밴시켰습니다.", colour=colour)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            return


@_unban.error
async def _unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author), colour=colour)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


@client.command(name="뮤트", pass_context=True)
@commands.has_permissions(administrator=True)
async def _mute(ctx, member: discord.Member=None):
    member = member or ctx.message.author
    await member.add_roles(get(ctx.guild.roles, name="Muted"))
    await ctx.send(member.mention + "를 뮤트 했습니다")


@_mute.error
async def _mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author), colour=colour)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)






@client.command(name="언뮤트", pass_context=True)
@commands.has_permissions(administrator=True)
async def _unmute(ctx, member: discord.Member=None):
    member = member or ctx.message.author
    await member.remove_roles(get(ctx.guild.roles, name='Muted'))
    await ctx.send(member.mention + "를 언뮤트 했습니다.")


@_unmute.error
async def _unmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author), colour=colour)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)





access_token = os.environ["BOT_TOKEN"]
client.run(access_token)

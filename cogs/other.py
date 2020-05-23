import discord
import datetime
import json
import dbl
import urllib.request
import aiohttp
from discord.ext import commands
from urllib.parse import quote
from urllib.request import urlopen, Request, HTTPError

#Naver Open API application ID
client_id = "YeOVJk0bK59ryYiRDIiY"
#Naver Open API application token
client_secret = "ZBHDeMCaMe"
colour = discord.Colour.blue()

class 기타(commands.Cog):
    """기타등등의 기능들을 보여줍니다"""

    def __init__(self, client):
        self.client = client
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY5NTU0NjU3NzI2MzEzMjY3NCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTkwMDI0Njg1fQ.rW5IA2Dikv5Xbo6tskmWTqHZiQauEngrdKhzP54Pp0A'  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.client, self.token)
        self.CBSList = "http://m.safekorea.go.kr/idsiSFK/neo/ext/json/disasterDataList/disasterDataList.json"

    @commands.command(name="한영번역", pass_context=True)
    async def translation(self, ctx, *, trsText):
        """한국어를 영어로 번역합니다."""
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
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.send("번역 완료", embed=embed)
                else:
                    await ctx.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await ctx.send("Translate Failed. HTTPError Occured.")

    @commands.command(name="영한번역", pass_context=True)
    async def displayembed(self, ctx, *, trsText):
        """영어를 한국어로 번역합니다."""
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
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.send("번역 완료", embed=embed)
                else:
                    await ctx.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await ctx.send("Translate Failed. HTTPError Occured.")

    @commands.command(name="인증", pass_context=True)
    async def certification(self, ctx):
        """사람임을 인증합니다.재미용"""
        code = "0"
        url = "https://openapi.naver.com/v1/captcha/nkey?code=" + code
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            key = response_body.decode('utf-8')
            key = json.loads(key)
            key = key['key']
            url = "https://openapi.naver.com/v1/captcha/ncaptcha.bin?key=" + key
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", client_id)
            request.add_header("X-Naver-Client-Secret", client_secret)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
            if (rescode == 200):
                print("캡차 이미지 저장")
                response_body = response.read()
                name = str(ctx.author.id) + '.png'
                with open(name, 'wb') as f:
                    f.write(response_body)
                await ctx.send(file=discord.File(str(ctx.author.id) + '.png'))

                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel

                try:
                    msg = await self.client.wait_for("message", timeout=60, check=check)
                except:
                    await ctx.send("시간초과입니다.")
                    return

                code = "1"
                value = msg.content
                url = "https://openapi.naver.com/v1/captcha/nkey?code=" + code + "&key=" + key + "&value=" + str(quote(value))
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urllib.request.urlopen(request)
                rescode = response.getcode()
                if (rescode == 200):
                    response_body = response.read()
                    sid = response_body.decode('utf-8')
                    answer = json.loads(sid)
                    answer = answer['result']
                    time = json.loads(sid)
                    time = time['responseTime']
                    if str(answer) == 'True':
                        await ctx.send("정답입니다. 걸린시간:" + str(time) + '초')
                    if str(answer) == 'False':
                        await ctx.send("틀리셨습니다. 걸린시간:" + str(time) + '초')
                else:
                    print("Error Code:" + rescode)
            else:
                print("Error Code:" + rescode)
        else:
            print("Error Code:" + rescode)
        
    @commands.command(name="봇초대", pass_context=True)
    async def invite(self, ctx):
        """봇초대 주소를 보여줍니다"""
        await ctx.send("https://discord.com/oauth2/authorize?client_id=695546577263132674&scope=bot&permissions=1945201982")

    @commands.command(name="온라인")
    async def servernumber(self, ctx):
        """햔재 들어가있는 서버수를 보여줍니다"""
        embed = discord.Embed(color=colour)
        embed.add_field(name="들어가있는 서버수", value=f"{self.dblpy.guild_count()}개")
        await ctx.send(embed=embed)

    @commands.command(name="재난문자")
    async def get_cbs(self, ctx):
        """최근에 발생한 재난문자를 보여줍니다"""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.CBSList) as r:
                data = await r.json()

        embed = discord.Embed(
            title="📢 재난문자",
            description="최근 발송된 3개의 재난문자를 보여줘요.",
            color=0xE71212
        )

        for i in data[:3]:
            embed.add_field(name=i["SJ"], value=i["CONT"], inline=False)
        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(기타(client))
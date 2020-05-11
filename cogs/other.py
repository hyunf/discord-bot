import discord
import random
import datetime
import json
from captcha.image import ImageCaptcha
from discord.ext import commands
from urllib.parse import quote
from urllib.request import urlopen, Request, HTTPError

#Naver Open API application ID
client_id = "YeOVJk0bK59ryYiRDIiY"
#Naver Open API application token
client_secret = "ZBHDeMCaMe"
colour = discord.Colour.blue()

class 기타(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="인증", pass_context=True)
    async def certification(self, ctx):
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
            msg = await self.client.wait_for("message", timeout=60, check=check)
        except:
            await ctx.send("시간초과입니다.")
            return

        if msg.content == a:
            await ctx.send("정답입니다.")
        else:
            await ctx.send("오답입니다.")

    @commands.command(name="한영번역", pass_context=True)
    async def translation(self, ctx, *, trsText):
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

def setup(client):
    client.add_cog(기타(client))
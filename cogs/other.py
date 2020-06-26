import discord
import datetime
import json
import dbl
import urllib.request
import aiohttp
from discord.ext import commands
from urllib.parse import quote
import pokepy
from email.mime.text import MIMEText

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
        members_count = 0

        for guild in self.client.guilds:
            members_count += len(guild.members)
        embed = discord.Embed(color=colour)
        embed.add_field(name="들어가있는 서버수", value=f"{self.dblpy.guild_count()}개", inline=False)
        embed.add_field(name="사용중인 인원수", value=f"{members_count}명", inline=False)
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

    @commands.command(name="포켓검색")
    async def sc(self, ctx, *, poke):
        """포켓몬들의 스텟을 보여줍니다 이름은 영어로 넣어주세요"""
        pokemon = pokepy.V2Client().get_pokemon(str(poke))
        embed = discord.Embed(title=pokemon.name, colour=colour)
        embed.set_image(url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon.id}.png")
        embed.add_field(name="채력", value=str(pokemon.stats[0].base_stat), inline=True)
        embed.add_field(name="공격력", value=str(pokemon.stats[1].base_stat), inline=True)
        embed.add_field(name="방어력", value=str(pokemon.stats[2].base_stat), inline=True)
        embed.add_field(name="특수 공격", value=str(pokemon.stats[3].base_stat), inline=True)
        embed.add_field(name="특수 방어", value=str(pokemon.stats[4].base_stat), inline=True)
        embed.add_field(name="스피드", value=str(pokemon.stats[5].base_stat), inline=True)
        embed.add_field(name="타입", value=", ".join(ty.type.name for ty in pokemon.types), inline=True)
        await ctx.send(embed=embed)




def setup(client):
    client.add_cog(기타(client))
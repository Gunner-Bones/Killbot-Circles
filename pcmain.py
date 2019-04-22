import discord, asyncio, sys, os, urllib.request, json, math, random, ast, datetime, base64, time
from discord.ext import commands
from common import *

Client = discord.Client()
bot_prefix= "??"
client = commands.Bot(command_prefix=bot_prefix)

s = None
try: s = open("pass.txt","r")
except: sys.exit("[Error] pass.txt needed for Secret")
sl = []
for l in s: sl.append(l.replace("\n",""))
SECRET = sl[0]

# https://discordapp.com/oauth2/authorize?client_id=501942021615779850&scope=bot

CHAR_SUCCESS = "✅"
CHAR_FAILED = "❌"
CHAR_SENT = "📨"

DEMONSLIST = []

def DEMONSLISTREFRESH():
    global DEMONSLIST
    url1 = "https://pointercrate.com/api/v1/demons?limit=100"
    url2 = "https://pointercrate.com/api/v1/demons?position__gt=101"
    rq1 = urllib.request.Request(url1); rq2 = urllib.request.Request(url2)
    try: rt1 = str(urllib.request.urlopen(rq1).read()); rt2 = str(urllib.request.urlopen(rq2).read())
    except:
        print("[Demons List] Could not access the Demons List!")
        return
    rt1 = rt1[2:len(rt1) - 1]; rt2 = rt2[2:len(rt2) - 1]
    rt1 = rt1.replace("\\n", ""); rt2 = rt2.replace("\\n", "")
    rt1 = rt1.replace("  ", ""); rt2 = rt2.replace("  ", "")
    rj1 = json.loads(rt1); rj2 = json.loads(rt2)
    DEMONSLIST = []
    for d1 in rj1: DEMONSLIST.append(d1)
    for d2 in rj2: DEMONSLIST.append(d2)
    print("[Demons List] Top 100 Demons refreshed")

def BotHasPermissions(ctx):
    if not ctx.message.guild: return True
    for member in ctx.guild.members:
        if str(member.id) == str(client.user.id):
            for role in member.roles:
                if role.permissions.administrator: return True
    return False

def AuthorHasPermissions(ctx):
    if not ctx.message.guild: return True
    if ctx.author.guild.owner: return True
    for role in ctx.author.roles:
        if role.permissions.administrator: return True
    return False

async def ResponseMessage(ctx,response,messagereaction,preset=""):
    if preset != "":
        pi = {"authorlacksperms":"You do not have Permission to perform this!",
              "botlacksperms":client.user.name + " does not have Permissions to perform this!",
              "invalidparams":"Invalid parameters!"}
        response = pi[preset]
    await ctx.message.channel.send("**" + ctx.author.name + "**, " + response)
    mri = {"success":CHAR_SUCCESS,"failed":CHAR_FAILED}
    await ctx.message.add_reaction(mri[messagereaction])

@client.event
async def on_ready():
    print("Bot Ready!!!!")
    print("Name: " + client.user.name + ", ID: " + str(client.user.id))
    sl = ""
    DEMONSLISTREFRESH()
    for server in client.guilds:
        if server is not None: sl += server.name + ", "
    print("Connected Guilds: " + sl[:len(sl) - 2])
    await client.change_presence(activity=discord.Game(name=(DEMONSLIST[random.randint(0, 99)])['name']))

@client.command(pass_context=True)
async def setmoderator(ctx,moderator):
    if AuthorHasPermissions(ctx):
        if BotHasPermissions(ctx):
            smmoderator = getrole(ctx.guild,moderator)
            if smmoderator is not None:
                if datasettings(file="pcmods.txt", method="get", line="MODERATOR" + str(ctx.guild.id)) is None:
                    datasettings(file="pcmods.txt", method="add", newkey="MODERATOR" + str(ctx.guild.id), newvalue=str(smmoderator.id))
                    await ResponseMessage(ctx,smmoderator.name + " set as MODERATOR role.","success")
                else:
                    datasettings(file="pcmods.txt", method="change", line="MODERATOR" + str(ctx.guild.id), newvalue=str(smmoderator.id))
                    await ResponseMessage(ctx, smmoderator.name + " set as MODERATOR role.", "success")
            else:
                await ResponseMessage(ctx,"","failed","invalidparams")
        else:
            await ResponseMessage(ctx,"","failed","botlacksperms")
    else:
        await ResponseMessage(ctx,"","failed","authorlacksperms")



client.run(SECRET)
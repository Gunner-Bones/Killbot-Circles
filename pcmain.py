import discord, asyncio, sys, os, urllib.request, json, math, random, ast, datetime, base64, time
from discord.ext import commands
from common import *
from constants import *

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
    mri = {RM_RESPONSE_SUCCESS:CHAR_SUCCESS,RM_RESPONSE_FAILED:CHAR_FAILED}
    await ctx.message.add_reaction(mri[messagereaction])

@client.event
async def on_ready():
    print("Bot Ready!")
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
            sm_moderator = getrole(ctx.guild,moderator)
            if smmoderator is not None:
                if datasettings(file=FILE_PCMODS, method=DS_METHOD_GET, line=KEY_MODERATOR + str(ctx.guild.id)) is None:
                    datasettings(file=FILE_PCMODS, method=DS_METHOD_ADD, newkey=KEY_MODERATOR + str(ctx.guild.id),
                                 newvalue=str(sm_moderator.id))
                    await ResponseMessage(ctx,sm_moderator.name + RM_MESSAGE_SETMODERATOR_SET,RM_RESPONSE_SUCCESS)
                else:
                    datasettings(file=FILE_PCMODS, method=DS_METHOD_CHANGE, line=KEY_MODERATOR + str(ctx.guild.id),
                                 newvalue=str(sm_moderator.id))
                    await ResponseMessage(ctx, sm_moderator.name + RM_MESSAGE_SETMODERATOR_SET,RM_RESPONSE_SUCCESS)
            else:
                await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_INVALIDPARAMS)
        else:
            await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_BOTLACKSPERMS)
    else:
        await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_AUTHORLACKSPERMS)

@client.command(pass_context=True)
async def addpointsrole(ctx,role_name,points_req):
    if AuthorHasPermissions(ctx):
        if BotHasPermissions(ctx):
            apr_role = getrole(ctx.guild,role_name)
            if apr_role is not None:
                if isnumber(points_req):
                    if datasettings(file=FILE_PCPROLES,method=DS_METHOD_GET,line=str(apr_role.id)) is None:
                        datasettings(file=FILE_PCPROLES,method=DS_METHOD_ADD,newkey=str(apr_role.id),
                                     newvalue=str(points_req))
                        await ResponseMessage(ctx,RM_MESSAGE_GENERAL_STARTING_SET + apr_role.name +
                                              RM_MESSAGE_ADDPOINTSROLE_SET + str(points_req),RM_RESPONSE_SUCCESS)
                    else:
                        await ResponseMessage(ctx,RM_MESSAGE_POINTSROLE_FAILEDEXISTS + apr_role.name +
                                              RM_MESSAGE_GENERAL_ENDING_IE,RM_RESPONSE_FAILED)
                else:
                    await ResponseMessage(ctx,RM_MESSAGE_GENERAL_INVALIDPOINTSNUMBER,RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx,RM_MESSAGE_GENERAL_INVALIDROLE,RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_BOTLACKSPERMS)
    else:
        await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_AUTHORLACKSPERMS)

@client.command(pass_context=True)
async def removepointsrole(ctx,role_name):
    if AuthorHasPermissions(ctx):
        if BotHasPermissions(ctx):
            rpr_role = getrole(ctx.guild,role_name)
            if rpr_role is not None:
                if datasettings(file=FILE_PCPROLES,method=DS_METHOD_GET,line=str(rpr_role.id)) is not None:
                    datasettings(file=FILE_PCPROLES,method=DS_METHOD_CHANGE,line=str(rpr_role.id),newvalue=VALUE_REMOVED)
                    await ResponseMessage(ctx, RM_MESSAGE_GENERAL_STARTING_REMOVE + rpr_role.name +
                                          RM_MESSAGE_REMOVEPOINTSROLE_REMOVE,RM_RESPONSE_SUCCESS)
                else:
                    await ResponseMessage(ctx, RM_MESSAGE_POINTSROLE_FAILEDDOESNTEXIST + apr_role.name +
                                          RM_MESSAGE_GENERAL_ENDING_IE, RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDROLE, RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx, RM_BLANK, RM_RESPONSE_FAILED, RM_PRESET_BOTLACKSPERMS)
    else:
        await ResponseMessage(ctx, RM_BLANK, RM_RESPONSE_FAILED, RM_PRESET_AUTHORLACKSPERMS)

@client.command(pass_context=True)
async def editpointsrole(ctx,role_name,points_req):
    if AuthorHasPermissions(ctx):
        if BotHasPermissions(ctx):
            epr_role = getrole(ctx.guild,role_name)
            if epr_role is not None:
                if isnumber(points_req):
                    if datasettings(file=FILE_PCPROLES,method=DS_METHOD_GET,line=str(epr_role.id)) is not None:
                        datasettings(file=FILE_PCPROLES,method=DS_METHOD_CHANGE,line=str(epr_role.id),
                                     newvalue=str(points_req))
                        await ResponseMessage(ctx,RM_MESSAGE_GENERAL_STARTING_SET + epr_role.name +
                                              RM_MESSAGE_EDITPOINTSROLE_SET + str(points_req),RM_RESPONSE_SUCCESS)
                    else:
                        await ResponseMessage(ctx,RM_MESSAGE_POINTSROLE_FAILEDEXISTS + epr_role.name +
                                              RM_MESSAGE_GENERAL_ENDING_IE,RM_RESPONSE_FAILED)
                else:
                    await ResponseMessage(ctx,RM_MESSAGE_GENERAL_INVALIDPOINTSNUMBER,RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx,RM_MESSAGE_GENERAL_INVALIDROLE,RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_BOTLACKSPERMS)
    else:
        await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_AUTHORLACKSPERMS)

@client.command(pass_context=True)
async def adddemonsrole(ctx,role_name,demons):
    global DEMONSLIST
    if AuthorHasPermissions(ctx):
        if BotHasPermissions(ctx):
            adr_role = getrole(ctx.guild,role_name)
            if adr_role is not None:
                adr_demons = []
                adr_valid = False
                if "," not in demons:
                    adr_demons = [demons]
                    adr_valid = True
                else:
                    demons_split = demons.split(",")
                    for demon in demons_split:
                        for list_demon in DEMONSLIST:
                            if list_demon['name'].lower() == demon.lower(): adr_demons.append(demon)
                    if adr_demons == demons_split: adr_valid = True
                if adr_valid:
                    adr_demons_str = ""
                    for demon in adr_demons: adr_demons_str += demon + ";"
                    adr_demons_str = adr_demons_str[:len(adr_demons_str) - 1]
                    if datasettings(file=FILE_PCDROLES, method=DS_METHOD_GET, line=str(adr_role.id)) is None:
                        datasettings(file=FILE_PCDROLES, method=DS_METHOD_ADD, newkey=str(adr_role.id), newline=adr_demons_str)
                        await ResponseMessage(ctx, RM_MESSAGE_GENERAL_STARTING_SET + adr_role.name +
                                              RM_MESSAGE_DEMONSROLE_SET + adr_demons_str,RM_RESPONSE_SUCCESS)
                    else:
                        await ResponseMessage(ctx, RM_MESSAGE_DEMONSROLE_FAILEDEXISTS + adr_role.name +
                                              RM_MESSAGE_GENERAL_ENDING_IE, RM_RESPONSE_FAILED)
                else:
                    await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDDEMONS, RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx,RM_MESSAGE_GENERAL_INVALIDROLE,RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_BOTLACKSPERMS)
    else:
        await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_AUTHORLACKSPERMS)

@client.command(pass_context=True)
async def removedemonsrole(ctx,role_name):
    global DEMONSLIST
    if AuthorHasPermissions(ctx):
        if BotHasPermissions(ctx):
            rdr_role = getrole(ctx.guild,role_name)
            if rdr_role is not None:
                if datasettings(file=FILE_PCDROLES, method=DS_METHOD_GET, line=str(rdr_role.id)) is not None:
                    datasettings(file=FILE_PCDROLES, method=DS_METHOD_CHANGE, line=str(rdr_role.id), newvalue=VALUE_REMOVED)
                    await ResponseMessage(ctx, RM_MESSAGE_GENERAL_STARTING_REMOVE + rdr_role.name +
                                          RM_MESSAGE_REMOVEDEMONSROLE_REMOVE ,RM_RESPONSE_SUCCESS)
                else:
                    await ResponseMessage(ctx, RM_MESSAGE_DEMONSROLE_FAILEDDOESNTEXIST + rdr_role.name +
                                          RM_MESSAGE_GENERAL_ENDING_IE, RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx,RM_MESSAGE_GENERAL_INVALIDROLE,RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_BOTLACKSPERMS)
    else:
        await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_AUTHORLACKSPERMS)

@client.command(pass_context=True)
async def editdemonsrole(ctx,role_name,demons):
    global DEMONSLIST
    if AuthorHasPermissions(ctx):
        if BotHasPermissions(ctx):
            edr_role = getrole(ctx.guild,role_name)
            if edr_role is not None:
                adr_demons = []
                adr_valid = False
                if "," not in demons:
                    adr_demons = [demons]
                    adr_valid = True
                else:
                    demons_split = demons.split(",")
                    for demon in demons_split:
                        for list_demon in DEMONSLIST:
                            if list_demon['name'].lower() == demon.lower(): adr_demons.append(demon)
                    if adr_demons == demons_split: adr_valid = True
                if adr_valid:
                    adr_demons_str = ""
                    for demon in adr_demons: adr_demons_str += demon + ";"
                    adr_demons_str = adr_demons_str[:len(adr_demons_str) - 1]
                    if datasettings(file=FILE_PCDROLES, method=DS_METHOD_GET, line=str(edr_role.id)) is not None:
                        datasettings(file=FILE_PCDROLES, method=DS_METHOD_CHANGE, newkey=str(edr_role.id), newline=adr_demons_str)
                        await ResponseMessage(ctx, RM_MESSAGE_GENERAL_STARTING_SET + edr_role.name +
                                              RM_MESSAGE_DEMONSROLE_SET + adr_demons_str,RM_RESPONSE_SUCCESS)
                    else:
                        await ResponseMessage(ctx, RM_MESSAGE_DEMONSROLE_FAILEDDOESNTEXIST + edr_role.name +
                                              RM_MESSAGE_GENERAL_ENDING_IE, RM_RESPONSE_FAILED)
                else:
                    await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDDEMONS, RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx,RM_MESSAGE_GENERAL_INVALIDROLE,RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_BOTLACKSPERMS)
    else:
        await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_AUTHORLACKSPERMS)

client.run(SECRET)
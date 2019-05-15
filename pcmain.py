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

def membermoderator(member):
    m = datasettings(FILE_PCMODS,DS_METHOD_GET,KEY_MODERATOR + str(member.guild.id))
    if m is None: return memberadmin(member)
    m = getrole(member.guild,m)
    if m in member.roles: return True
    else: return memberadmin(member)

def linkedplayer(uid):
    uid = str(uid)
    if alldatakeys(FILE_PCDATA):
        for lp in alldatakeys(FILE_PCDATA):
            if lp == uid: return datasettings(file=FILE_PCDATA,method=DS_METHOD_GET,line=lp)
    return None

async def reportfeedback(guild_name,user_name,demon,feedback):
    feedback_channel = getchannel(getguild(SPECIFIC_GUILD_POINTERCRATE),
                                  datasettings(file=FILE_PCVARS,method=DS_METHOD_GET,line=KEY_FEEDBACKCHANNEL))
    if feedback_channel is not None:
        await feedback_channel.send(NM_MESSAGE_FEEDBACK + guild_name + NM_LINE_USER + user_name + NM_LINE_DEMON +
                                    demon + NM_LINE_FEEDBACK + feedback)

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
    if membermoderator(ctx.author):
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
    if membermoderator(ctx.author):
        if BotHasPermissions(ctx):
            rpr_role = getrole(ctx.guild,role_name)
            if rpr_role is not None:
                if datasettings(file=FILE_PCPROLES,method=DS_METHOD_GET,line=str(rpr_role.id)) is not None:
                    datasettings(file=FILE_PCPROLES,method=DS_METHOD_CHANGE,line=str(rpr_role.id),newvalue=VALUE_REMOVED)
                    await ResponseMessage(ctx, RM_MESSAGE_GENERAL_STARTING_REMOVE + rpr_role.name +
                                          RM_MESSAGE_REMOVEPOINTSROLE_REMOVE,RM_RESPONSE_SUCCESS)
                else:
                    await ResponseMessage(ctx, RM_MESSAGE_POINTSROLE_FAILEDDOESNTEXIST + rpr_role.name +
                                          RM_MESSAGE_GENERAL_ENDING_IE, RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDROLE, RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx, RM_BLANK, RM_RESPONSE_FAILED, RM_PRESET_BOTLACKSPERMS)
    else:
        await ResponseMessage(ctx, RM_BLANK, RM_RESPONSE_FAILED, RM_PRESET_AUTHORLACKSPERMS)

@client.command(pass_context=True)
async def editpointsrole(ctx,role_name,points_req):
    if membermoderator(ctx.author):
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
    if membermoderator(ctx.author):
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
    if membermoderator(ctx.author):
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
    if membermoderator(ctx.author):
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


@client.command(pass_context=True)
async def playerlink(ctx,user_name,player_id):
    if inallowedguild(ctx.guild,ctx.author):
        if membermoderator(ctx.author):
            if BotHasPermissions(ctx):
                link_user = getmember(ctx.guild,user_name)
                if link_user is not None:
                    if isnumber(player_id):
                        link_user_data = PLAYERDATA(player_id)
                        if link_user_data is not None:
                            player_has_points = True
                            try: link_user_data['records']
                            except KeyError: player_has_points = False
                            if player_has_points:
                                if datasettings(file=FILE_PCDATA,method=DS_METHOD_GET,line=str(link_user.id)) is None:
                                    datasettings(file=FILE_PCDATA,method=DS_METHOD_ADD,newkey=str(link_user.id),newvalue=str(player_id))
                                    await ResponseMessage(ctx, RM_MESSAGE_PLAYERLINK_SET + link_user.name +
                                                          RM_MESSAGE_GENERAL_MIDDLE_TO + str(player_id) +
                                                          RM_MESSAGE_GENERAL_MIDDLE_PARENTHESESOPEN + link_user_data['name'] +
                                                          RM_MESSAGE_GENERAL_MIDDLE_PARENTHESESCLOSE, RM_RESPONSE_SUCCESS)
                                else:
                                    await ResponseMessage(ctx, RM_MESSAGE_PLAYERLINK_FAILEDEXISTS, RM_RESPONSE_FAILED)
                            else:
                                await ResponseMessage(ctx, RM_MESSAGE_GENERAL_PLAYERNOPOINTS, RM_RESPONSE_FAILED)
                        else:
                            await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDPID, RM_RESPONSE_FAILED)
                    else:
                        await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDPID, RM_RESPONSE_FAILED)
                else:
                    await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDUSER, RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_BOTLACKSPERMS)
        else:
            await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_AUTHORLACKSPERMS)

@client.command(pass_context=True)
async def playerunlink(ctx,user_name):
    if inallowedguild(ctx.guild, ctx.author):
        if membermoderator(ctx.author):
            if BotHasPermissions(ctx):
                link_user = getmember(ctx.guild,user_name)
                if link_user is not None:
                    if datasettings(file=FILE_PCDATA, method=DS_METHOD_GET, line=str(link_user.id)) is not None:
                        link_id = datasettings(file=FILE_PCDATA, method=DS_METHOD_GET, line=str(link_user.id))
                        link_data = PLAYERDATA(link_id)
                        link_name = "No Name"
                        try: link_name = link_data['name']
                        except: pass
                        datasettings(file=FILE_PCDATA,method=DS_METHOD_CHANGE, line=str(link_user.id), newvalue=VALUE_REMOVED)
                        await ResponseMessage(ctx, RM_MESSAGE_PLAYERUNLINK_SET + link_user.name +
                                              RM_MESSAGE_GENERAL_MIDDLE_FROM + link_id +
                                              RM_MESSAGE_GENERAL_MIDDLE_PARENTHESESOPEN + link_name +
                                              RM_MESSAGE_GENERAL_MIDDLE_PARENTHESESCLOSE, RM_RESPONSE_SUCCESS)
                    else:
                        await ResponseMessage(ctx, RM_MESSAGE_PLAYERLINK_FAILEDDOESNTEXIST, RM_RESPONSE_FAILED)
                else:
                    await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDUSER, RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_BOTLACKSPERMS)
        else:
            await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_AUTHORLACKSPERMS)

@client.command(pass_context=True)
async def addpositionalrole(ctx,role_name,base,range):
    if membermoderator(ctx.author):
        if BotHasPermissions(ctx):
            pos_role = getrole(ctx.guild,role_name)
            if pos_role is not None:
                if isnumber(base) and isnumber(range):
                    pos_base = int(base)
                    pos_range = int(range)
                    if 1 <= pos_base <= 100:
                        if 1 <= pos_range <= pos_base:
                            if datasettings(file=FILE_PCPOSROLES,method=DS_METHOD_GET,line=str(pos_role.id)) is None:
                                datasettings(file=FILE_PCPOSROLES,method=DS_METHOD_ADD,newkey=str(pos_role.id),
                                             newvalue=str(pos_base) + VALUE_DASH + str(pos_range))
                                await ResponseMessage(ctx, pos_role.name + RM_MESSAGE_ADDPOSITIONALROLE_SET1 +
                                                      str(pos_base) + RM_MESSAGE_ADDPOSITIONALROLE_SET2 +
                                                      str(pos_range), RM_RESPONSE_SUCCESS)
                            else:
                                await ResponseMessage(ctx, RM_MESSAGE_POSITIONALROLE_FAILEDEXISTS + pos_role.name +
                                                      RM_MESSAGE_GENERAL_ENDING_IE, RM_RESPONSE_FAILED)
                        else:
                            await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDRANGEBASE, RM_RESPONSE_FAILED)
                    else:
                        await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDRANGEBASE, RM_RESPONSE_FAILED)
                else:
                    await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDRANGEBASE, RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDROLE, RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_BOTLACKSPERMS)
    else:
        await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_AUTHORLACKSPERMS)

@client.command(pass_context=True)
async def removepositionalrole(ctx,role_name):
    if membermoderator(ctx.author):
        if BotHasPermissions(ctx):
            pos_role = getrole(ctx.guild, role_name)
            if pos_role is not None:
                if datasettings(file=FILE_PCPOSROLES,method=DS_METHOD_GET,line=str(pos_role.id)) is not None:
                    datasettings(file=FILE_PCPOSROLES,method=DS_METHOD_CHANGE,line=str(pos_role.id),newvalue=VALUE_REMOVED)
                    await ResponseMessage(ctx, RM_MESSAGE_GENERAL_STARTING_REMOVE + pos_role.name +
                                          RM_MESSAGE_REMOVEPOSITIONALROLE_REMOVE, RM_RESPONSE_SUCCESS)
                else:
                    await ResponseMessage(ctx, RM_MESSAGE_POSITIONALROLE_FAILEDDOESNTEXIST + pos_role.name +
                                          RM_MESSAGE_GENERAL_ENDING_IE, RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDROLE, RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_BOTLACKSPERMS)
    else:
        await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_AUTHORLACKSPERMS)

@client.command(pass_context=True)
async def editpositionalrole(ctx,role_name,base,range):
    if membermoderator(ctx.author):
        if BotHasPermissions(ctx):
            pos_role = getrole(ctx.guild,role_name)
            if pos_role is not None:
                if isnumber(base) and isnumber(range):
                    pos_base = int(base)
                    pos_range = int(range)
                    if 1 <= pos_base <= 100:
                        if 1 <= pos_range <= pos_base:
                            if datasettings(file=FILE_PCPOSROLES,method=DS_METHOD_GET,line=str(pos_role.id)) is not None:
                                datasettings(file=FILE_PCPOSROLES,method=DS_METHOD_CHANGE,line=str(pos_role.id),
                                             newvalue=str(pos_base) + VALUE_DASH + str(pos_range))
                                await ResponseMessage(ctx, RM_MESSAGE_GENERAL_STARTING_SET + pos_role.name +
                                                      RM_MESSAGE_EDITPOSITIONALROLE_SET +
                                                      str(pos_base) + RM_MESSAGE_ADDPOSITIONALROLE_SET2 +
                                                      str(pos_range), RM_RESPONSE_SUCCESS)
                            else:
                                await ResponseMessage(ctx, RM_MESSAGE_POSITIONALROLE_FAILEDDOESNTEXIST + pos_role.name +
                                                      RM_MESSAGE_GENERAL_ENDING_IE, RM_RESPONSE_FAILED)
                        else:
                            await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDRANGEBASE, RM_RESPONSE_FAILED)
                    else:
                        await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDRANGEBASE, RM_RESPONSE_FAILED)
                else:
                    await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDRANGEBASE, RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDROLE, RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_BOTLACKSPERMS)
    else:
        await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_AUTHORLACKSPERMS)

client.command(pass_context=True)
async def feedback(ctx,demon_position,feedback_message):
    global DEMONSLIST
    if isnumber(demon_position):
        if 1 <= demon_position <= len(DEMONSLIST):
            if linkedplayer(str(ctx.author.id)) is not None:
                link_data = PLAYERDATA(linkedplayer(str(ctx.author.id)))
                if link_data is not None:
                    feedback_demon_beaten = False
                    feedback_demon = ""
                    for demon in DEMONSLIST:
                        if demon['position'] == demon_position: feedback_demon = demon['name']
                    for beaten_demon in link_data['records']:
                        if feedback_demon.lower() == beaten_demon['demon']['name'].lower(): feedback_demon_beaten = True
                    if feedback_demon_beaten:
                        if len(feedback_message) >= 1:
                            wrote_feedback = False
                            for feedback in alldatakeys(FILE_PCFEED):
                                feedback_data = datasettings(file=FILE_PCFEED,method=DS_METHOD_GET,line=feedback).split(";")
                                if feedback_data[0] == linkedplayer(str(ctx.author.id)) and feedback_data[1].lower() == feedback_demon.lower():
                                    wrote_feedback = True
                            if not wrote_feedback:
                                await reportfeedback(ctx.guild.name,ctx.author.name,feedback_demon,feedback_message)
                                datasettings(file=FILE_PCFEED,method=DS_METHOD_ADD,
                                             newkey=KEY_FEEDBACK + str(random.randint(10000,99999)),
                                             newline=linkedplayer(str(ctx.author.id)) + VALUE_SEMICOLON + feedback_demon)
                                await ResponseMessage(ctx, RM_MESSAGE_FEEDBACK_SENT + feedback_demon +
                                                      RM_MESSAGE_GENERAL_ENDING_SENT, RM_RESPONSE_SUCCESS)
                            else:
                                await ResponseMessage(ctx, RM_MESSAGE_FEEDBACK_ALREADYWRITTEN + feedback_demon +
                                                      RM_MESSAGE_GENERAL_ENDING_IE, RM_RESPONSE_FAILED)
                        else:
                            await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDMESSAGE, RM_RESPONSE_FAILED)
                    else:
                        await ResponseMessage(ctx, RM_MESSAGE_FEEDBACK_NOTBEATEN + feedback_demon +
                                              RM_MESSAGE_GENERAL_ENDING_IE, RM_RESPONSE_FAILED)
                else:
                    await ResponseMessage(ctx, RM_MESSAGE_GENERAL_PLAYERNOPOINTS, RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx, RM_MESSAGE_GENERAL_NOTLINKED, RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDDEMONPOSITION, RM_RESPONSE_FAILED)
    else:
        await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDDEMONPOSITION, RM_RESPONSE_FAILED)


client.run(SECRET)
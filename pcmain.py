import discord, asyncio, sys, os, urllib.request, json, math, random, ast, datetime, base64, time
from discord.ext import commands
from common import *
from constants import *

Client = discord.Client()
bot_prefix= "??"
client = commands.Bot(command_prefix=bot_prefix)
client.remove_command("help")

s = None
try: s = open("pass.txt","r")
except: sys.exit("[Error] pass.txt needed for Secret")
sl = []
for l in s: sl.append(l.replace(NM_KEY_INDENT,""))
SECRET = sl[0]

# https://discordapp.com/oauth2/authorize?client_id=501942021615779850&scope=bot

DEMONSLIST = []
REFRESH_ACTIVE = False
SPOT_REFRESH = False
SPOT_SERVER = None

NEW_DEMONS_ALLOWED = ["Hard Demon","Insane Demon","Extreme Demon"]

def DEMONSLISTREFRESH():
    global DEMONSLIST
    url1 = "https://pointercrate.com/api/v1/demons?limit=100"
    url2 = "https://pointercrate.com/api/v1/demons?after=100"
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

async def kc_presence():
    await client.change_presence(activity=discord.Game(name=(DEMONSLIST[random.randint(0, 99)])[POINTERCRATE_KEY_NAME]))

def logpoints(pid,np):
    lpp = datasettings(file=FILE_PCPOINTS,method=DS_METHOD_GET,line=str(pid) + KEY_PID)
    if lpp is None: datasettings(file=FILE_PCPOINTS,method=DS_METHOD_ADD,newkey=str(pid) + KEY_PID,newvalue=str([{VALUE_ID:1,VALUE_POINTS:np}]))
    else:
        lpp = strtolod(lpp)
        lplid = 0
        for l in lpp:
            if int(l[VALUE_ID]) >= lplid: lplid = int(l[VALUE_ID])
        for l in lpp:
            if int(l[VALUE_ID]) == lplid:
                if str(l[VALUE_POINTS]) == str(np): return
        lpp.append({VALUE_ID:lplid + 1,VALUE_POINTS:np})
        datasettings(file=FILE_PCPOINTS,method=DS_METHOD_CHANGE,line=str(pid) + KEY_PID,newvalue=str(lpp))

def loggedpointschange(pid,mn=0):
    lpp = datasettings(file=FILE_PCPOINTS, method=DS_METHOD_GET, line=str(pid) + KEY_PID)
    if lpp is None: return None
    lpp = strtolod(lpp)
    lplid = 0
    for l in lpp:
        if int(l[VALUE_ID]) >= lplid: lplid = int(l[VALUE_ID])
    lplid -= mn
    if lplid == 1: return {VALUE_ID:1,VALUE_OLD:lpp[0][VALUE_POINTS],VALUE_DIF:lpp[0][VALUE_POINTS]}
    lpnew = 0; lpold = 0
    for l in lpp:
        if l[VALUE_ID] == lplid: lpnew = l[VALUE_POINTS]
        if l[VALUE_ID] == lplid - 1: lpold = l[VALUE_POINTS]
    lpdif = lpnew - lpold
    return {VALUE_ID:lplid,VALUE_OLD:lpold,VALUE_DIF:lpdif}

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
    feedback_channel_id = datasettings(file=FILE_PCVARS,method=DS_METHOD_GET,line=KEY_FEEDBACKCHANNEL)
    feedback_channel = None
    for guild in client.guilds:
        for channel in guild.channels:
            if str(channel.id) == feedback_channel_id:
                feedback_channel = channel
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
    await kc_presence()

NOTIFY_KEYWORDS = [client.command_prefix + POINTERCRATE_COMMAND_ACCEPT,
                   client.command_prefix + POINTERCRATE_COMMAND_REJECT,
                   client.command_prefix + POINTERCRATE_COMMAND_ADD,
                   ALIAS_POINTERCRATE_ACCEPT, ALIAS_POINTERCRATE_REJECT]

NOTIFY_RECORD = None

@client.event
async def on_message(message):
    global REFRESH_ACTIVE
    global NOTIFY_KEYWORDS
    global NOTIFY_RECORD
    # Reactions
    reaction_adds = []
    if message.channel.id in LIST_CHANNELS_UDQ: reaction_adds = [CHAR_HAND_UP,CHAR_HAND_DOWN,CHAR_QUESTION]
    elif message.channel.id in LIST_CHANNELS_UD: reaction_adds = [CHAR_HAND_UP,CHAR_HAND_DOWN]
    for a_reaction in reaction_adds: await message.add_reaction(a_reaction)
    # Refresh
    if message.content.startswith(KC_OVERRIDE_REFRESH) and message.author.id == SPECIFIC_USER_GB:
        REFRESH_ACTIVE = False
        await message.channel.send(RM_MESSAGE_REFRSH_OVERRIDE)
        await message.add_reaction(CHAR_SUCCESS)
    if REFRESH_ACTIVE and not message.author.bot and message.content.startswith(client.command_prefix):
        await message.channel.send(RM_MESSAGE_REFRESH_ACTIVE)
        await message.add_reaction(CHAR_FAILED)
    # Notify
    if message.content.startswith(tuple(NOTIFY_KEYWORDS)): NOTIFY_RECORD = message.author.name
    if message.author.id == SPECIFIC_USER_DLB and message.guild.id == SPECIFIC_GUILD_POINTERCRATE and NOTIFY_RECORD:
        notify_message_works = True
        notify_message_embeds = None
        try: notify_message_embeds = message.embeds[0].to_dict()
        except: notify_message_works = False
        if notify_message_works:
            notify_message_fields = None
            try: notify_message_fields = notify_message_embeds[DISCORD_KEY_FIELDS]
            except: notify_message_works = False
            if notify_message_works:
                player_pid = notify_message_fields[1][DISCORD_KEY_VALUE].split(NM_KEY_INDENT)
                player_pid = player_pid[1].replace(DLB_KEY_PID,VALUE_BLANK)
                notify_exempt = False
                for pid in alldatakeys(FILE_PCN):
                    if datasettings(file=FILE_PCN,method=DS_METHOD_GET,line=pid) == player_pid: notify_exempt = True
                if not notify_exempt:
                    user_id = None
                    for uid in alldatakeys(FILE_PCDATA):
                        if datasettings(file=FILE_PCDATA,method=DS_METHOD_GET,line=uid) == player_pid: user_id = uid
                    if user_id:
                        user_player = getglobalmember(user_id,client)
                        if user_player is not None:
                            notify_demon_name = None
                            notify_demon_progress = None
                            notify_demon_status = None
                            try:
                                notify_demon_name = notify_message_fields[0][DISCORD_KEY_VALUE].split(NM_KEY_INDENT)
                                notify_demon_name = notify_demon_name[0].replace(DLB_KEY_DEMON,VALUE_BLANK)
                                notify_description = notify_message_embeds[DLB_KEY_DESCRIPTION].split(NM_KEY_INDENT)
                                notify_demon_progress = notify_description[1].replace(DLB_KEY_PROGRESS,VALUE_BLANK)
                                notify_demon_status = notify_description[3].replace(DLB_KEY_STATUS,VALUE_BLANK)
                            except: notify_message_works = False
                            if notify_message_works:
                                notify_message = "__**Notification from the Demons List Team!**__\n"
                                notify_message += "**" + user_player.name + "**, your record *" + notify_demon_progress + \
                                "* on __" + notify_demon_name + "__ has been " + notify_demon_status.upper() + "!\n"
                                notify_message += "`[Record " + notify_demon_status + " by " + NOTIFY_RECORD + "]`\n"
                                notify_message += "*If you don\'t want to be notified, type ??getnotified*"
                                await user_player.send(notify_message)
                                await message.add_reaction(CHAR_SENT)

    else: await client.process_commands(message)

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
                    adr_demons = [demons.replace("\"","")]
                    adr_valid = True
                else:
                    demons_split = demons.replace("\"","")
                    demons_split = demons_split.split(",")
                    for demon in demons_split:
                        for list_demon in DEMONSLIST:
                            if list_demon[POINTERCRATE_KEY_NAME].lower() == demon.lower():
                                adr_demons.append(demon)
                    if adr_demons.sort() == demons_split.sort(): adr_valid = True
                if adr_valid:
                    adr_demons_str = ""
                    for demon in adr_demons: adr_demons_str += demon + ";"
                    adr_demons_str = adr_demons_str[:len(adr_demons_str) - 1]
                    if datasettings(file=FILE_PCDROLES, method=DS_METHOD_GET, line=str(adr_role.id)) is None:
                        datasettings(file=FILE_PCDROLES, method=DS_METHOD_ADD, newkey=str(adr_role.id), newvalue=adr_demons_str)
                        await ResponseMessage(ctx, RM_MESSAGE_GENERAL_STARTING_SET + adr_role.name +
                                              RM_MESSAGE_ADDDEMONSROLE_SET + adr_demons_str,RM_RESPONSE_SUCCESS)
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
                            if list_demon[POINTERCRATE_KEY_NAME].lower() == demon.lower(): adr_demons.append(demon)
                    if adr_demons == demons_split: adr_valid = True
                if adr_valid:
                    adr_demons_str = ""
                    for demon in adr_demons: adr_demons_str += demon + ";"
                    adr_demons_str = adr_demons_str[:len(adr_demons_str) - 1]
                    if datasettings(file=FILE_PCDROLES, method=DS_METHOD_GET, line=str(edr_role.id)) is not None:
                        datasettings(file=FILE_PCDROLES, method=DS_METHOD_CHANGE, newkey=str(edr_role.id), newvalue=adr_demons_str)
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
                        link_user_data = await get_player_data(player_id)
                        if link_user_data is not None:
                            player_has_points = True
                            try: link_user_data[POINTERCRATE_KEY_RECORDS]
                            except KeyError: player_has_points = False
                            if player_has_points:
                                if datasettings(file=FILE_PCDATA,method=DS_METHOD_GET,line=str(link_user.id)) is None:
                                    datasettings(file=FILE_PCDATA,method=DS_METHOD_ADD,newkey=str(link_user.id),newvalue=str(player_id))
                                    await ResponseMessage(ctx, RM_MESSAGE_PLAYERLINK_SET + link_user.name +
                                                          RM_MESSAGE_GENERAL_MIDDLE_TO + str(player_id) +
                                                          RM_MESSAGE_GENERAL_MIDDLE_PARENTHESESOPEN + link_user_data[POINTERCRATE_KEY_NAME] +
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
                        link_data = await get_player_data(link_id)
                        link_name = "No Name"
                        try: link_name = link_data[POINTERCRATE_KEY_NAME]
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

@client.command(pass_context=True)
async def feedback(ctx,demon_position : int,feedback_message):
    global DEMONSLIST
    if isnumber(demon_position):
        if 1 <= demon_position <= len(DEMONSLIST):
            if linkedplayer(str(ctx.author.id)) is not None:
                link_data = await get_player_data(linkedplayer(str(ctx.author.id)))
                if link_data is not None:
                    if datasettings(file=FILE_PCFB,method=DS_METHOD_GET,line=str(ctx.author.id)) is None:
                        feedback_demon_beaten = False
                        feedback_demon = VALUE_BLANK
                        for demon in DEMONSLIST:
                            if demon[POINTERCRATE_KEY_POSITION] == demon_position: feedback_demon = demon[POINTERCRATE_KEY_NAME]
                        for beaten_demon in link_data[POINTERCRATE_KEY_RECORDS]:
                            if feedback_demon.lower() == beaten_demon[POINTERCRATE_KEY_DEMON][POINTERCRATE_KEY_NAME].lower(): feedback_demon_beaten = True
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
                                                 newvalue=linkedplayer(str(ctx.author.id)) + VALUE_SEMICOLON + feedback_demon)
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
                        await ResponseMessage(ctx, RM_MESSAGE_FEEDBACK_BANNED, RM_RESPONSE_FAILED)
                else:
                    await ResponseMessage(ctx, RM_MESSAGE_GENERAL_PLAYERNOPOINTS, RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx, RM_MESSAGE_GENERAL_NOTLINKED, RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDDEMONPOSITION, RM_RESPONSE_FAILED)
    else:
        await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDDEMONPOSITION, RM_RESPONSE_FAILED)

@client.command(pass_context=True)
async def feedbackban(ctx,user_name):
    if inallowedguild(ctx.guild, ctx.author):
        if membermoderator(ctx.author):
            if BotHasPermissions(ctx):
                ban_user = getmember(ctx.guild,user_name)
                if ban_user is not None:
                    if datasettings(file=FILE_PCFB,method=DS_METHOD_GET,line=str(ban_user.id)) is None:
                        datasettings(file=FILE_PCFB,method=DS_METHOD_ADD,newkey=str(ban_user.id),newvalue=VALUE_BANNED)
                        await ResponseMessage(ctx, ban_user.name + RM_MESSAGE_FEEDBACKBAN_BAN, RM_RESPONSE_SUCCESS)
                    else:
                        datasettings(file=FILE_PCFB,method=DS_METHOD_REMOVE,line=str(ban_user.id))
                        await ResponseMessage(ctx, ban_user.name + RM_MESSAGE_FEEDBACKBAN_UNBAN, RM_RESPONSE_SUCCESS)
                else:
                    await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDUSER, RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx, RM_BLANK, RM_RESPONSE_FAILED, RM_PRESET_BOTLACKSPERMS)
        else:
            await ResponseMessage(ctx, RM_BLANK, RM_RESPONSE_FAILED, RM_PRESET_AUTHORLACKSPERMS)

@client.command(pass_context=True)
async def info(ctx,user_name):
    info_user = getmember(ctx.guild,user_name)
    if info_user is not None:
        if linkedplayer(info_user.id) is not None:
            link_data = await get_player_data(linkedplayer(info_user.id))
            if link_data is not None:
                info_demon_hardest = 999
                info_roles_point = []
                info_roles_demon = []
                info_roles_positional = []
                info_points = str(POINTSFORMULA(link_data))
                info_completed = []
                info_verified = []
                info_banned = link_data[POINTERCRATE_KEY_BANNED]
                # info_completed and info_verified: [Name(str),Type(main|extended|legacy),Progress(int)]
                for beaten_demon in link_data[POINTERCRATE_KEY_RECORDS]:
                    if beaten_demon[POINTERCRATE_KEY_DEMON][POINTERCRATE_KEY_POSITION] < info_demon_hardest:
                        if beaten_demon[POINTERCRATE_KEY_STATUS] == POINTERCRATE_VALUE_APPROVED and beaten_demon[POINTERCRATE_KEY_PROGRESS] == 100:
                            info_demon_hardest = beaten_demon[POINTERCRATE_KEY_DEMON][POINTERCRATE_KEY_POSITION]
                    beaten_demon_type = POINTERCRATE_VALUE_LEGACY
                    if beaten_demon[POINTERCRATE_KEY_DEMON][POINTERCRATE_KEY_POSITION] < 151: beaten_demon_type = POINTERCRATE_VALUE_EXTENDED
                    if beaten_demon[POINTERCRATE_KEY_DEMON][POINTERCRATE_KEY_POSITION] < 76: beaten_demon_type = POINTERCRATE_VALUE_MAIN
                    info_completed.append([beaten_demon[POINTERCRATE_KEY_DEMON][POINTERCRATE_KEY_NAME],beaten_demon_type,beaten_demon[POINTERCRATE_KEY_PROGRESS]])
                for verified_demon in link_data[POINTERCRATE_KEY_VERIFIED]:
                    if verified_demon[POINTERCRATE_KEY_POSITION] < info_demon_hardest:
                        info_demon_hardest = verified_demon[POINTERCRATE_KEY_POSITION]
                    verified_demon_type = POINTERCRATE_VALUE_LEGACY
                    if verified_demon[POINTERCRATE_KEY_POSITION] < 151: verified_demon_type = POINTERCRATE_VALUE_EXTENDED
                    if verified_demon[POINTERCRATE_KEY_POSITION] < 76: verified_demon_type = POINTERCRATE_VALUE_MAIN
                    info_verified.append([verified_demon[POINTERCRATE_KEY_NAME],verified_demon_type,100])
                for demon in DEMONSLIST:
                    if demon[POINTERCRATE_KEY_POSITION] == info_demon_hardest:
                        info_demon_hardest = demon[POINTERCRATE_KEY_NAME]
                        break
                info_text_completed = ""
                info_text_verified = ""
                for demon in info_completed:
                    if demon[2] == 100:
                        if demon[1] == POINTERCRATE_VALUE_LEGACY: info_text_completed += "*" + demon[0] + "*, "
                        elif demon[1] == POINTERCRATE_VALUE_EXTENDED: info_text_completed += demon[0] + ", "
                        elif demon[1] == POINTERCRATE_VALUE_MAIN: info_text_completed += "__" + demon[0] + "__, "
                for demon in info_verified:
                    info_text_verified += demon[0] + ", "
                if len(info_text_completed) > 0:
                    info_text_completed = info_text_completed[:len(info_text_completed) - 2]
                if len(info_text_verified) > 0:
                    info_text_verified = info_text_verified[:len(info_text_verified) - 2]
                if isnumber(info_demon_hardest): info_demon_hardest = VALUE_NONE
                for role_point_id in alldatakeys(FILE_PCPROLES):
                    for user_role in info_user.roles:
                        if str(user_role.id) == role_point_id: info_roles_point.append(user_role.name)
                for role_demon_id in alldatakeys(FILE_PCDROLES):
                    for user_role in info_user.roles:
                        if str(user_role.id) == role_demon_id: info_roles_demon.append(user_role.name)
                for role_positional_id in alldatakeys(FILE_PCPOSROLES):
                    for user_role in info_user.roles:
                        if str(user_role.id) == role_positional_id: info_roles_positional.append(user_role.name)
                info_text_point = ""
                info_text_demon = ""
                info_text_positional = ""
                if not info_roles_point: info_text_point = VALUE_NONE
                else:
                    for kc_role in info_roles_point: info_text_point += kc_role + ", "
                    info_text_point = info_text_point[:len(info_text_point) - 2]
                if not info_roles_demon: info_text_demon = VALUE_NONE
                else:
                    for kc_role in info_roles_demon: info_text_demon += kc_role + ", "
                    info_text_demon = info_text_demon[:len(info_text_demon) - 2]
                if not info_roles_positional: info_text_positional = VALUE_NONE
                else:
                    for kc_role in info_roles_positional: info_text_positional += kc_role + ", "
                    info_text_positional = info_text_positional[:len(info_text_positional) - 2]
                info_text1 = "\n__User Information for *" + link_data[POINTERCRATE_KEY_NAME] + "*__\n"
                info_text1 += NM_NI_LINE_USER + str(info_user.id) + NM_KEY_INDENT
                info_text1 += "**Linked Pointercrate Account**: " + info_user.name + " (ID: " + linkedplayer(info_user.id) + ")\n"
                info_text1 += "__Pointercrate Stats__\n"
                info_text1 += NM_NI_LINE_POINTS + info_points + NM_KEY_INDENT
                info_text1 += NM_NI_LINE_COMPLETED + info_text_completed + NM_KEY_INDENT
                info_text1 += NM_NI_LINE_VERIFIED + info_text_verified + NM_KEY_INDENT
                info_text1 += NM_NI_LINE_HARDEST + info_demon_hardest + NM_KEY_INDENT
                info_text1 += NM_NI_LINE_BANNED + str(info_banned) + NM_KEY_INDENT
                info_text2 = "__Server Perks__\n"
                info_text2 += NM_NI_LINE_ROLES_POINTS + info_text_point + NM_KEY_INDENT
                info_text2 += NM_NI_LINE_ROLES_DEMONS + info_text_demon + NM_KEY_INDENT
                info_text2 += NM_NI_LINE_ROLES_POSITIONAL + info_text_positional + NM_KEY_INDENT
                await ResponseMessage(ctx, info_text1, RM_RESPONSE_SUCCESS)
                await ctx.message.channel.send(info_text2)
            else:
                await ResponseMessage(ctx, RM_MESSAGE_GENERAL_PLAYERNOPOINTS, RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx, RM_MESSAGE_GENERAL_NOTLINKED, RM_RESPONSE_FAILED)
    else:
        await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDUSER, RM_RESPONSE_FAILED)

@client.command(pass_context=True)
async def setnewdemonschannel(ctx,channel_name):
    if membermoderator(ctx.author):
        if BotHasPermissions(ctx):
            new_demons_channel = getchannel(ctx.guild,channel_name)
            if new_demons_channel is not None:
                if datasettings(file=FILE_PCVARS,method=DS_METHOD_GET,line=KEY_NEWDEMONSCHANNEL) is None:
                    datasettings(file=FILE_PCVARS,method=DS_METHOD_ADD,newkey=str([KEY_NEWDEMONSCHANNEL]),
                                 newvalue=str(new_demons_channel.id))
                else:
                    new_demons_channel_list = strtolist(datasettings(file=FILE_PCVARS,method=DS_METHOD_GET,line=KEY_NEWDEMONSCHANNEL))
                    if new_demons_channel.id not in new_demons_channel_list:
                        new_demons_channel_list.append(new_demons_channel.id)
                        datasettings(file=FILE_PCVARS, method=DS_METHOD_CHANGE, line=KEY_NEWDEMONSCHANNEL,
                                     newvalue=str(new_demons_channel_list))
                await ResponseMessage(ctx, RM_MESSAGE_NEWDEMONSCHANNEL_SET + new_demons_channel.name +
                                      RM_MESSAGE_GENERAL_ENDING_IE, RM_RESPONSE_SUCCESS)
            else:
                await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDCHANNEL, RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_BOTLACKSPERMS)
    else:
        await ResponseMessage(ctx,RM_BLANK,RM_RESPONSE_FAILED,RM_PRESET_AUTHORLACKSPERMS)

async def auto_refresh():
    global REFRESH_ACTIVE
    global SPOT_REFRESH
    global SPOT_SERVER
    while True:
        if (datetime.datetime.now().minute == 0 and datetime.datetime.now().hour % 2 < 0) or SPOT_REFRESH:
            print("[Refresh] Refresh Started.")
            REFRESH_ACTIVE = True
            await client.change_presence(activity=discord.Game(name=PRESENCE_REFRESH_START))
            DEMONSLISTREFRESH()
            guild_count = 0
            for guild in client.guilds: guild_count += 1
            if SPOT_REFRESH: guild_count = 1
            guild_iterator = 0
            for guild in client.guilds:
                if not SPOT_REFRESH or (SPOT_REFRESH and SPOT_SERVER == guild):

                    await client.change_presence(activity=discord.Game(name=PRESENCE_REFRESH_CYCLE1 + str(guild_iterator) +
                                                                            VALUE_SLASH + str(guild_count) + PRESENCE_REFRESH_CYCLE2))
                    count_points_add = 0
                    count_points_remove = 0
                    count_demons_add = 0
                    count_demons_remove = 0
                    count_positional_add = 0
                    count_positional_remove = 0
                    count_new_remove = 0
                    if alldatakeys(FILE_PCDATA):
                        for player_id in alldatakeys(FILE_PCDATA):
                            player = getmember(guild,player_id)
                            if player is None: continue
                            player_pid = datasettings(file=FILE_PCDATA,method=DS_METHOD_GET,line=player_id)
                            player_data = await get_player_data(player_pid)
                            if player_data is None: continue
                            # Points Roles & Log Points
                            for role_points_id in alldatakeys(FILE_PCPROLES):
                                role_points = getrole(guild,role_points_id)
                                if role_points is not None:
                                    role_points_req = datasettings(file=FILE_PCPROLES,method=DS_METHOD_GET,line=role_points_id)
                                    if role_points_req == VALUE_REMOVED:
                                        for member in guild.members:
                                            if role_points in member.roles:
                                                try: await player.remove_roles(role_points)
                                                except discord.errors.Forbidden: continue
                                                count_points_remove += 1
                                        datasettings(file=FILE_PCPROLES,method=DS_METHOD_REMOVE,line=role_points_id)
                                    else:
                                        if role_points_id is not None:
                                            role_points_req = int(role_points_req)
                                            player_points = int(POINTSFORMULA(player_data))
                                            logpoints(player_pid,player_points)
                                            if player_points >= role_points_req:
                                                if role_points not in player.roles:
                                                    try: await player.add_roles(role_points)
                                                    except discord.errors.Forbidden: continue
                                                    count_points_add += 1
                                            else:
                                                if role_points in player.roles:
                                                    try: await player.remove_roles(role_points)
                                                    except discord.errors.Forbidden: continue
                                                    count_points_remove += 1
                            # Demons Roles
                            for role_demons_id in alldatakeys(FILE_PCDROLES):
                                role_demons = getrole(guild,role_demons_id)
                                if role_demons is not None:
                                    role_demons_list = datasettings(file=FILE_PCDROLES,method=DS_METHOD_GET,line=role_demons_id)
                                    if role_demons_list == VALUE_REMOVED:
                                        for member in guild.members:
                                            if role_demons in member.roles:
                                                try: await member.remove_roles(role_demons)
                                                except discord.errors.Forbidden: continue
                                                count_demons_remove += 1
                                        datasettings(file=FILE_PCDROLES, method=DS_METHOD_REMOVE, line=role_demons_id)
                                    else:
                                        if role_demons_list is not None:
                                            role_demons_list = role_demons_list.split(VALUE_SEMICOLON)
                                            demons_found = True
                                            for required_demon in role_demons_list:
                                                if not demons_found: break
                                                for beaten_demon in player_data[POINTERCRATE_KEY_RECORDS]:
                                                    if beaten_demon[POINTERCRATE_KEY_DEMON][POINTERCRATE_KEY_NAME].lower() == required_demon.lower() \
                                                            and beaten_demon[POINTERCRATE_KEY_PROGRESS] == 100:
                                                        demons_found = True
                                                        break
                                                    demons_found = False
                                            if not demons_found and len(player_data[POINTERCRATE_KEY_VERIFIED]) >= 1:
                                                demons_found = True
                                                for required_demon in role_demons_list:
                                                    if not demons_found: break
                                                    for verified_demon in player_data[POINTERCRATE_KEY_VERIFIED]:
                                                        if verified_demon[POINTERCRATE_KEY_NAME].lower() == required_demon.lower():
                                                            demons_found = True
                                                            break
                                                        demons_found = False
                                            if demons_found:
                                                if role_demons not in player.roles:
                                                    try: await player.add_roles(role_demons)
                                                    except discord.errors.Forbidden: continue
                                                    count_demons_add += 1
                                            else:
                                                if role_demons in player.roles:
                                                    try: await player.remove_roles(role_demons)
                                                    except discord.errors.Forbidden: continue
                                                    count_demons_remove += 1
                            # Positonal Roles
                            for role_pos_id in alldatakeys(FILE_PCPOSROLES):
                                role_pos = getrole(guild,role_pos_id)
                                if role_pos is not None:
                                    role_pos_data = datasettings(file=FILE_PCPOSROLES,method=DS_METHOD_GET,line=role_pos_id)
                                    if role_pos_data == VALUE_REMOVED:
                                        for member in guild.members:
                                            if role_pos in member.roles:
                                                try: await member.remove_roles(role_pos)
                                                except discord.errors.Forbidden: continue
                                                count_positional_remove += 1
                                        datasettings(file=FILE_PCPOSROLES, method=DS_METHOD_REMOVE, line=role_pos_id)
                                    else:
                                        role_pos_data = role_pos_data.split(VALUE_DASH)
                                        pos_requirement = int(role_pos_data[0])
                                        pos_number = int(role_pos_data[1])
                                        demons_found = 0
                                        for beaten_demon in player_data[POINTERCRATE_KEY_RECORDS]:
                                            if int(beaten_demon[POINTERCRATE_KEY_DEMON][POINTERCRATE_KEY_POSITION]) \
                                                    <= pos_requirement and beaten_demon[POINTERCRATE_KEY_PROGRESS] == 100: demons_found += 1
                                        for verified_demon in player_data[POINTERCRATE_KEY_VERIFIED]:
                                            if int(verified_demon[POINTERCRATE_KEY_POSITION]) <= pos_requirement: demons_found += 1
                                        if demons_found >= pos_number:
                                            if role_pos not in player.roles:
                                                try: await player.add_roles(role_pos)
                                                except discord.errors.Forbidden: continue
                                                count_positional_add += 1
                                        else:
                                            if role_pos in player.roles:
                                                try: await player.remove_roles(role_pos)
                                                except discord.errors.Forbidden: continue
                                                count_positional_remove += 1
                            # New Demons Channels
                            new_channel_list = strtolist(datasettings(file=FILE_PCVARS,method=DS_METHOD_GET,line=KEY_NEWDEMONSCHANNEL))
                            if len(new_channel_list) > 0:
                                for new_channel_id in new_channel_list:
                                    for channel in guild.channels:
                                        if channel.id == new_channel_id:
                                            delete_message = []
                                            async for message in channel.history(limit=50):
                                                if message.author.id == SPECIFIC_USER_UGB and message.created_at > \
                                                    (datetime.datetime.now() - datetime.timedelta(days=13)):
                                                    try: message_embed = message.embeds[0].to_dict()
                                                    except: continue
                                                    for embed_field in message_embed[DISCORD_KEY_FIELDS]:
                                                        if UGB_KEY_LEVEL in embed_field[DISCORD_KEY_VALUE]:
                                                            level_id = embed_field[DISCORD_KEY_VALUE].replace(UGB_KEY_LEVEL,VALUE_BLANK)
                                                            level_data = getanylevel(level_id)
                                                            if level_data:
                                                                if level_data[GAL_KEY_DIFFICULTY] not in NEW_DEMONS_ALLOWED:
                                                                    delete_message.append(message)
                                                                    count_new_remove += 1
                                            await channel.delete_messages(delete_message)
                    guild_iterator += 1
            await client.change_presence(activity=discord.Game(name=PRESENCE_REFRESH_FINISH))
            print("[Refresh] Refresh Finished.")
            if not SPOT_REFRESH: await asyncio.sleep(60)
            else: await asyncio.sleep(10)
            REFRESH_ACTIVE = False
            SPOT_REFRESH = False
            await kc_presence()
        await asyncio.sleep(10)

@client.command(pass_context=True)
async def refresh(ctx):
    global SPOT_REFRESH
    global SPOT_SERVER
    if inallowedguild(ctx.guild, ctx.author):
        if membermoderator(ctx.author):
            if BotHasPermissions(ctx):
                SPOT_REFRESH = True
                SPOT_SERVER = ctx.guild
                await ResponseMessage(ctx, RM_MESSAGE_REFRESH_SPOT, RM_RESPONSE_SUCCESS)
            else:
                await ResponseMessage(ctx, RM_BLANK, RM_RESPONSE_FAILED, RM_PRESET_BOTLACKSPERMS)
        else:
            await ResponseMessage(ctx, RM_BLANK, RM_RESPONSE_FAILED, RM_PRESET_AUTHORLACKSPERMS)

@client.command(pass_context=True)
async def kcroles(ctx):
    kc_message = "\n__Killbot Circles Roles for **" + ctx.guild.name + "**:__\n"
    kc_message += NM_LINE_ROLES_POINTS
    for role_points_id in alldatakeys(FILE_PCPROLES):
        role_points = getrole(ctx.guild,role_points_id)
        count_role_points = 0
        role_points_req = datasettings(file=FILE_PCPROLES,method=DS_METHOD_GET,line=role_points_id)
        if role_points is not None:
            for member in ctx.guild.members:
                if role_points in member.roles: count_role_points += 1
            kc_message += VALUE_BRACKET_OPEN + str(count_role_points) + VALUE_BRACKET_CLOSE + role_points.name + \
                          VALUE_COLON + role_points_req + NM_KEY_INDENT
    kc_message += NM_LINE_ROLES_DEMONS
    for role_demons_id in alldatakeys(FILE_PCDROLES):
        role_demons = getrole(ctx.guild,role_demons_id)
        count_role_demons = 0
        role_demons_req = datasettings(file=FILE_PCDROLES,method=DS_METHOD_GET,line=role_demons_id)
        if role_demons is not None:
            for member in ctx.guild.members:
                if role_demons in member.roles: count_role_demons += 1
            kc_message += VALUE_BRACKET_OPEN + str(count_role_demons) + VALUE_BRACKET_CLOSE + role_demons.name + \
                          VALUE_COLON + role_demons_req + NM_KEY_INDENT
    kc_message += NM_LINE_ROLES_POSITIONAL
    for role_pos_id in alldatakeys(FILE_PCPOSROLES):
        role_pos = getrole(ctx.guild,role_pos_id)
        count_role_pos = 0
        role_pos_req = datasettings(file=FILE_PCPOSROLES,method=DS_METHOD_GET,line=role_pos_id).split(VALUE_DASH)
        role_pos_text = NM_NI_LINE_INFO_POSITIONAL_POSITION + role_pos_req[0] + NM_NI_LINE_INFO_POSITIONAL_REQUIRED + \
                        role_pos_req[1]
        if role_pos is not None:
            for member in ctx.guild.members:
                if role_pos in member.roles: count_role_pos += 1
            kc_message += VALUE_BRACKET_OPEN + str(count_role_pos) + VALUE_BRACKET_CLOSE + role_pos.name + \
                          VALUE_COLON + role_pos_text + NM_KEY_INDENT
    await ResponseMessage(ctx, kc_message, RM_RESPONSE_SUCCESS)

@client.command(pass_context=True)
async def whohas(ctx,role_name):
    if membermoderator(ctx.author):
        if BotHasPermissions(ctx):
            wh_role = getrole(ctx.guild, role_name)
            if wh_role is not None:
                wh_type = None
                wh_data = None
                for role_points_id in alldatakeys(FILE_PCPROLES):
                    if role_points_id == str(wh_role.id):
                        wh_type = NM_NI_TYPE_POINTS
                        wh_data = datasettings(file=FILE_PCPROLES,method=DS_METHOD_GET,line=role_points_id)
                for role_demons_id in alldatakeys(FILE_PCDROLES):
                    if role_demons_id == str(wh_role.id):
                        wh_type = NM_NI_TYPE_DEMONS
                        wh_data = datasettings(file=FILE_PCDROLES,method=DS_METHOD_GET,line=role_demons_id)
                for role_pos_id in alldatakeys(FILE_PCPOSROLES):
                    if role_pos_id == str(wh_role.id):
                        wh_type = NM_NI_TYPE_POSITIONAL
                        pos_data = datasettings(file=FILE_PCPOSROLES,method=DS_METHOD_GET,line=role_pos_id).split(VALUE_DASH)
                        wh_data = NM_NI_LINE_INFO_POSITIONAL_POSITION + pos_data[0] + \
                                  NM_NI_LINE_INFO_POSITIONAL_REQUIRED + pos_data[1]
                wh_users = VALUE_BLANK
                wh_count = 0
                for member in ctx.guild.members:
                    if wh_role in member.roles:
                        wh_users += member.name + ", "
                        wh_count += 1
                if wh_count == 0:  wh_message = RM_MESSAGE_WHOHAS_NONE
                else:
                    wh_users = wh_users[:len(wh_users) - 2]
                    wh_message = RM_MESSAGE_WHOHAS_SHOW1 + str(wh_count) + RM_MESSAGE_WHOHAS_SHOW2 + wh_role.name + \
                    VALUE_COLON + NM_KEY_INDENT
                    if wh_type is not None and wh_data is not None:
                        wh_message += RM_MESSAGE_WHOHAS_KC1 + wh_type + RM_MESSAGE_WHOHAS_KC2 + wh_data + NM_KEY_INDENT
                    wh_message += wh_users
                await ResponseMessage(ctx, wh_message, RM_RESPONSE_SUCCESS)
            else:
                await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDROLE, RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx, RM_BLANK, RM_RESPONSE_FAILED, RM_PRESET_BOTLACKSPERMS)
    else:
        await ResponseMessage(ctx, RM_BLANK, RM_RESPONSE_FAILED, RM_PRESET_AUTHORLACKSPERMS)

@client.command(pass_context=True)
async def pointschanges(ctx,user_name):
    pc_user = getmember(ctx.guild,user_name)
    if pc_user is not None:
        pc_pid = linkedplayer(pc_user)
        if pc_pid is not None:
            pc_data = await get_player_data(pc_pid)
            if pc_data is not None:
                pc_change = loggedpointschange(pc_data)
                if pc_change is not None:
                    if int(pc_change[VALUE_ID]) != 1:
                        pc_difference = pc_change[VALUE_DIF]
                        pc_old = int(pc_change[VALUE_OLD])
                        pc_new = POINTSFORMULA(pc_data)
                        if pc_old != 0:
                            await ResponseMessage(ctx, RM_MESSAGE_POINTSCHANGE_OLD + pc_difference +
                                                  RM_MESSAGE_POINTSCHANGE_NEW + pc_new, RM_RESPONSE_SUCCESS)
                        else:
                            await ResponseMessage(ctx, RM_MESSAGE_POINTSCHANGE_NONEW, RM_RESPONSE_FAILED)
                    else:
                        await ResponseMessage(ctx, RM_MESSAGE_POINTSCHANGE_NONEW, RM_RESPONSE_FAILED)
                else:
                    await ResponseMessage(ctx, RM_MESSAGE_POINTSCHANGE_NONEW, RM_RESPONSE_FAILED)
            else:
                await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDPLAYER, RM_RESPONSE_FAILED)
        else:
            await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDPLAYER, RM_RESPONSE_FAILED)
    else:
        await ResponseMessage(ctx, RM_MESSAGE_GENERAL_INVALIDUSER, RM_RESPONSE_FAILED)

@client.command(pass_context=True)
async def kchelp(ctx):
    kc_message1 = VALUE_BLANK
    kc_message2 = VALUE_BLANK
    kc_file = open(FILE_PCHELP,F_METHOD_READ)
    kc_list1 = []
    kc_stopper1 = 25
    kc_list2 = []
    for line in kc_file:
        kc_stopper1 -= 1
        if kc_stopper1 <= 0: kc_list2.append(line)
        else: kc_list1.append(line)
    for line in kc_list1: kc_message1 += line
    for line in kc_list2: kc_message2 += line
    await ctx.author.send(kc_message1)
    await ctx.author.send(kc_message2)
    await ctx.message.add_reaction(CHAR_SUCCESS)


client.loop.create_task(auto_refresh())
client.run(SECRET)
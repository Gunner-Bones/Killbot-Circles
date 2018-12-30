import discord, asyncio, sys, os, urllib.request, json, math, random, ast, datetime, base64, time
from discord.ext import commands


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


def memberadmin(member):
    for r in member.roles:
       if r.permissions.administrator: return True
    return False

def membermoderator(member):
    m = datasettings("pcmods.txt","get","MODERATOR" + str(member.guild.id))
    if m is None: return memberadmin(member)
    m = getrole(member.guild,m)
    if m in member.roles: return True
    else: return memberadmin(member)

def botself(g):
    for m in g.members:
        if m.id == 501942021615779850: return m

def bothasperms(g):
    trp = botself(g).top_role.permissions
    if trp.administrator or trp.manage_roles: return True
    return False

def inallowedguild(g,m):
    # 0=No Admin needed,1=Admin needed
    allowedguilds = [[162862229065039872,0],[395654171422097420,1],[503422247927808010,0]]
    for ag in allowedguilds:
        if ag[0] == g.id:
            if ag[1] == 1: return memberadmin(m)
            return True
    return False

def getanylevel(levelname):
    """
    :param levelname: (str) Level ID or Name
    :return: Data about the Level
    LIST DATA:
    1 - Level ID
    3 - Level name
    54 - Author
    13 - Downloads
    19 - Likes
    35 - Description (Requires decode)
    39 - Original
    37 - Length (0:Tiny,1:Short,2:Medium,3:Long,4:XL)
    27 - Pass

    11 - Difficulty:
        if 11 is 50:
            if 21 is 1: Extreme Demon
            or if 25 is 1: Auto
            else: Insane
        if 11 is 40:
            if 27 is 10: Insane Demon
            else: Harder
        if 11 is 30:
            if 27 is 10: Hard Demon
            else: Hard
        if 11 is 20:
            if 27 is 10: Medium Demon
            else: Normal
        if 11 is 10:
            if 27 is 10: Easy Demon
            else: Easy
        if 11 is 0: N/A
    """
    url = "http://www.boomlings.com/database/getGJLevels21.php"
    p = "gameVersion=21&binaryVersion=35&gdw=0&type=0&str=" + levelname + \
        "&diff=-&len=-&page=0&total=0&uncompleted=0&onlyCompleted=0&featured=0&original=0&twoPlayer=0&coins=0&epic=0" \
        "&secret=Wmfd2893gb7"
    p = p.encode()
    data = urllib.request.urlopen(url, p).read().decode()
    data = data.split(":")

    if data[0] == "-1": return []

    levelHasOriginal = True
    if data[39] == "0":
        levelHasOriginal = False
    levelLength = "Tiny"
    if data[37] == "1":
        levelLength = "Short"
    elif data[37] == "2":
        levelLength = "Medium"
    elif data[37] == "3":
        levelLength = "Long"
    elif data[37] == "4":
        levelLength = "XL"
    levelDiff = "N/A"
    if data[11] == "50":
        if data[21] == "1": levelDiff = "Extreme Demon"
        elif data[25] == "1": levelDiff = "Auto"
        else: levelDiff = "Insane"
    elif data[11] == "40":
        if data[27] == "10": levelDiff = "Insane Demon"
        else: levelDiff = "Harder"
    elif data[11] == "30":
        if data[27] == "10": levelDiff = "Hard Demon"
        else: levelDiff = "Hard"
    elif data[11] == "20":
        if data[27] == "10": levelDiff = "Medium Demon"
        else: levelDiff = "Normal"
    elif data[11] == "10":
        if data[27] == "10": levelDiff = "Easy Demon"
        else: levelDiff = "Easy"
    try:
        leveldesc = base64.b64decode(str(data[35])).decode()
    except:
        leveldesc = ""
    dl = {"ID":data[1],"Name":data[3],"Author":data[54],"Downloads":data[13],"Likes":data[19],"Description":leveldesc,"Copied":str(levelHasOriginal),"Length":levelLength,"Difficulty":levelDiff}
    return dl

def getrole(s,rn):
    try:
        rid = int(rn)
        return discord.utils.find(lambda r: str(rid) in str(r.id), s.roles)
    except: return discord.utils.find(lambda r: rn.lower() in r.name.lower(), s.roles)

def getmember(s,mn):
    if str(mn).startswith("<@"):
        mid = mn.replace("<@",""); mid = mid.replace(">","")
        return discord.utils.find(lambda m: str(mid) in str(m.id), s.members)
    try:
        mid = int(mn)
        return discord.utils.find(lambda m: str(mid) in str(m.id), s.members)
    except: return discord.utils.find(lambda m: mn.lower() in m.name.lower(), s.members)

def getglobalmember(m):
    for s in client.guilds:
        if str(m).startswith("<@"):
            mid = m.replace("<@",""); mid = mid.replace(">","")
            mt = discord.utils.find(lambda m: str(mid) in str(m.id), s.members)
            if mt is not None: return mt
        try:
            mid = int(m)
            mt = discord.utils.find(lambda m: str(mid) in str(m.id), s.members)
            if mt is not None: return mt
        except:
            mt = discord.utils.find(lambda m: m.lower() in m.name.lower(), s.members)
            if mt is not None: return mt
    return None

def getchannel(s,cn):
    if str(cn).startswith("<#"):
        cid = cn.replace("<#",""); cid = cid.replace(">","")
        return discord.utils.find(lambda m: str(cid) in str(m.id), s.channels)
    try:
        cid = int(cn)
        return discord.utils.find(lambda m: str(cid) in str(m.id), s.channels)
    except: return discord.utils.find(lambda m: cn.lower() in m.name.lower(), s.channels)

def getguild(sid):
    for guild in client.guilds:
        if str(guild.id) == str(sid): return guild
    return None

def isnumber(n):
    try: nn = int(n); return True
    except: return False

def strtolist(s):
    if str(s) == "[]" or str(s) == "['']": return []
    st = str(s).replace("[",""); st = st.replace("]",""); st = st.replace("'",""); st = st.split(",")
    for t in st:
        if t.startswith(" "): st[st.index(t)] = t[1:]
    return st

def strtolod(s) -> list:
    global DEMONSLIST
    # [{'n':d,'p':d},{'n':d,'p':d}]
    if s[0] != "[": st = str(s).split("="); st = st[1]
    else: st = s
    st = st.replace("[",""); st = st.replace("]",""); st = st.split("},")
    for t in st:
        sti = t + "}"
        if sti.startswith(" "): sti = sti[1:]
        if sti[len(sti) - 2:] == "}}": sti = sti[:len(sti) - 1]
        sti = ast.literal_eval(sti)
        try: sti['position'] = int(sti['position'])
        except: pass
        try: sti['old pos'] = int(sti['old pos'])
        except: pass
        try: sti['new pos'] = int(sti['new pos'])
        except: pass
        try: sti['dif'] = int(sti['dif'])
        except: pass
        try: sti['points'] = int(sti['points'])
        except: pass
        try: sti['id'] = int(sti['id'])
        except: pass
        st[st.index(t)] = sti
    return st

def paramquotationlist(p):
    params = []
    while True:
        try:
            p1 = p.index("\""); p = p[:p1] + p[p1 + 1:]
            p2 = p.index("\""); p = p[:p2] + p[p2 + 1:]
            params.append(p[p1:p2])
        except ValueError:
            if params == []: return None
            return params

def paramnumberlist(p):
    params = []; i = -1; tempparam = [""]; inquotations = False; addingdone = True
    while True:
        try:
            i += 1
            tp = int(p[i])
            if not inquotations:
                addingdone = False
                tempparam[0] += str(tp)
        except ValueError:
            if p[i] == "\"":
                if inquotations: inquotations = False
                elif not inquotations: inquotations = True
            if p[i] == " " and not inquotations and not addingdone:
                params.append(int(tempparam[0]))
                tempparam[0] = ""
                addingdone = True
        except IndexError:
            if not addingdone:
                params.append(int(tempparam[0]))
                tempparam[0] = ""
            if params == []: return None
            return params

def paramlistlist(p,i):
    params = paramquotationlist(p)
    if params is None: return None
    if len(params) == 0: return None
    params = params[i]; params = params.split(",")
    for n in params:
        if str(n).startswith(" "): params[params.index(n)] = n[1:]
        if n[len(n) - 1] == " ": params[params.index(n)] = n[:len(n) - 1]
    return params

def datasettings(file,method,line="",newvalue="",newkey=""):
    """
    :param file: (str).txt
    :param method: (str) get,change,remove,add
    :param line: (str)
    :param newvalue: (str)
    :param newkey: (str)
    """
    s = None
    try: s = open(file,"r")
    except: return None
    sl = []
    for l in s: sl.append(l.replace("\n",""))
    for nl in sl:
        if str(nl).startswith(line):
            if method == "get": s.close(); return str(nl).replace(line + "=","")
            elif method == "change": sl[sl.index(nl)] = line + "=" + newvalue; break
            elif method == "remove": sl[sl.index(nl)] = None; break
    if method == "add": sl.append(newkey + "=" + newvalue)
    if method == "get": return None
    s.close()
    s = open(file,"w")
    s.truncate()
    slt = ""
    for nl in sl:
        if nl is not None:
            slt += nl + "\n"
    s.write(slt); s.close(); return None

def alldatakeys(file) -> list:
    s = None
    try: s = open(file,"r")
    except: return []
    sl = []
    for l in s: sl.append(l.replace("\n", ""))
    for nl in sl:
        nla = str(nl).split("=")
        sl[sl.index(nl)] = nla[0]
    s.close()
    for nl in sl:
        if nl == "": sl.remove(nl)
    return sl

DEMONSLIST = []

def linkedplayer(uid):
    uid = str(uid)
    if alldatakeys("pcdata.txt") != []:
        for lp in alldatakeys("pcdata.txt"):
            if lp == uid: return datasettings(file="pcdata.txt",method="get",line=lp)
    return None

def playersfix():
    if len(alldatakeys("pcdata.txt")) == 1:
        pd = alldatakeys("pcdata.txt")[0] + "=" + datasettings(file="pcdata.txt",method="get",
                                                               line=alldatakeys("pcdata.txt")[0])
        pdf = []
        pd = pd.split("=")
        c = 0
        for d in pd:
            if c > 1:
                bdif = len(pd[c - 1]) - 18
                fd = (pd[c - 1])[bdif:] + "="
                edif = len(pd[c]) - 18
                fd += (pd[c])[:edif]
                pdf.append(fd)
            elif c == 1:
                fd = pd[0]
                dif = len(pd[c]) - 18
                fd += "=" + (pd[c])[:dif]
                pdf.append(fd)
            c += 1
        return pdf


def logpoints(pid,np):
    lpp = datasettings(file="pcpoints.txt",method="get",line=str(pid) + "PID")
    if lpp is None: datasettings(file="pcpoints.txt",method="add",newkey=str(pid) + "PID",newvalue=str([{'id':1,'points':np}]))
    else:
        lpp = strtolod(lpp)
        lplid = 0
        for l in lpp:
            if int(l['id']) >= lplid: lplid = int(l['id'])
        for l in lpp:
            if int(l['id']) == lplid:
                if str(l['points']) == str(np): return
        lpp.append({'id':lplid + 1,'points':np})
        datasettings(file="pcpoints.txt",method="change",line=str(pid) + "PID",newvalue=str(lpp))

def loggedpointschange(pid,mn=0):
    lpp = datasettings(file="pcpoints.txt", method="get", line=str(pid) + "PID")
    if lpp is None: return None
    lpp = strtolod(lpp)
    lplid = 0
    for l in lpp:
        if int(l['id']) >= lplid: lplid = int(l['id'])
    lplid -= mn
    if lplid == 1: return {'id':1,'old':lpp[0]['points'],'dif':lpp[0]['points']}
    lpnew = 0; lpold = 0
    for l in lpp:
        if l['id'] == lplid: lpnew = l['points']
        if l['id'] == lplid - 1: lpold = l['points']
    lpdif = lpnew - lpold
    return {'id':lplid,'old':lpold,'dif':lpdif}



def PLAYERDATA(id):
    if id is None: return None
    url = "https://pointercrate.com/api/v1/players/" + str(id)
    rq = urllib.request.Request(url)
    try: rt = str(urllib.request.urlopen(rq).read())
    except: return None
    rt = rt[2:len(rt) - 1]; rt = rt.replace("\\n",""); rt = rt.replace("  ","")
    rj = json.loads(rt)
    return rj['data']

def POINTSFORMULA(data):
    if data is None: return None
    # requires data from PLAYERDATA()
    s = 0
    for d in data['beaten']:
        if int(d['position']) <= 100:
            s += (100 / ((100/5) + ((-100/5) + 1) * math.exp(-0.008*int(d['position']))))
    for d in data['verified']:
        if int(d['position']) <= 100:
            s += (100 / ((100/5) + ((-100/5) + 1) * math.exp(-0.008*int(d['position']))))
    return s

def DEMONSLISTREFRESH():
    global DEMONSLIST
    url1 = "https://pointercrate.com/api/v1/demons?limit=100"
    url2 = "https://pointercrate.com/api/v1/demons?position__gt=101"
    rq1 = urllib.request.Request(url1); rq2 = urllib.request.Request(url2)
    try: rt1 = str(urllib.request.urlopen(rq1).read()); rt2 = str(urllib.request.urlopen(rq2).read())
    except:
        print("[Demons List] Could not access the Demons List!")
        return
    rt1 = rt1[2:len(rt1) - 3]; rt2 = rt2[2:len(rt2) - 3]
    rt1 = rt1.replace("\\n", ""); rt2 = rt2.replace("\\n", "")
    rt1 = rt1.replace("  ", ""); rt2 = rt2.replace("  ", "")
    rj1 = json.loads(rt1); rj2 = json.loads(rt2)
    DEMONSLIST = []
    for d1 in rj1: DEMONSLIST.append(d1)
    for d2 in rj2: DEMONSLIST.append(d2)
    print("[Demons List] Top 100 Demons refreshed")



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


@client.event
async def on_guild_join(guild):
    print("[" + client.user.name + "] Server List updated")
    sl = ""
    for server in client.guilds:
        if server is not None: sl += server.name + ", "
    if sl != "": print("Connected Servers: " + sl[:len(sl) - 2])

@client.event
async def on_reaction_add(reaction, user):
    if inallowedguild(reaction.message.guild,user):
        smrv = True; smre = None; m = reaction.message
        try: smre = m.embeds[0].to_dict()
        except: smrv = False
        if smrv:
            smr = None
            try: smr = smre['fields']
            except: smrv = False
            if smrv:
                smrh = smr[1]['value'].split("\n")
                smrh = smrh[1].replace("**ID**: ", "")
                smf = False
                for h in alldatakeys("pcn.txt"):
                    if datasettings(file="pcn.txt", method="get", line=h) == smrh:
                        smf = True
                if not smf:
                    smf = None
                    for ph in alldatakeys("pcdata.txt"):
                        if datasettings(file="pcdata.txt", method="get", line=ph) == smrh:
                            smf = ph
                    if smf is not None:
                        hu = getglobalmember(smf)
                        if hu is not None:
                            smf = False
                            try:
                                smrd = smr[0]['value'].split("\n")
                                smrd = smrd[0].replace("**Name**: ", "")
                                smrdes = smre['description'].split("\n")
                                smrp = smrdes[1].replace("**Progress**: ", "")
                            except:
                                smf = True
                            if not smf:
                                global NRREVIEWRM
                                smrm = None; smnr = None; smnc = None
                                for r in NRREVIEWRM:
                                    if r[1] == user: smrm = r[0]; smnr = r; smnc = r[2]
                                if smrm is not None:
                                    if reaction.emoji == CHAR_SENT:
                                        smrmr = "*Notification from the Pointercrate Team*\n"
                                        smrmr += hu.name + ", your record **" + smrp + "** on **" + smrd + "** has been"
                                        smrmr += "\n REJECTED for the following reason(s): " + smrm + "\n"
                                        smrmr += "[Reason written by " + user.name + "]"
                                        await hu.send(smrmr)
                                        await smnc.send("**" + user.name + "**, Rejection Reason sent!")
                                        NRREVIEWRM.remove(smnr)



REFRESHACTIVE = False
REFRESHIN = None


async def oldsettingsalgorithm():
    # don't use this don't use this don't use this don't use this don't use this don't use this
    global REFRESHACTIVE
    await client.wait_until_ready()
    while not client.is_closed() and not REFRESHACTIVE:
        print("[Auto Refresh] Roles Refresh started")
        REFRESHACTIVE = True
        for channel in client.get_all_channels():
            # Points Roles
            if alldatakeys("pcproles.txt") != [] and alldatakeys("pcdata.txt") != []:
                for proleid in alldatakeys("pcproles.txt"):
                    prole = getrole(channel.guild, proleid)
                    if prole is not None:
                        prolepoints = datasettings(file="pcproles.txt", method="get", line=proleid)
                        if prolepoints is not None:
                            prolepoints = int(prolepoints)
                            for playerid in alldatakeys("pcdata.txt"):
                                player = getmember(channel.guild, playerid)
                                if player is not None:
                                    playerpoints = POINTSFORMULA(
                                        PLAYERDATA(datasettings(file="pcdata.txt", method="get",
                                                                line=playerid)))
                                    if playerpoints is not None:
                                        playerpoints = int(playerpoints)
                                        if playerpoints >= prolepoints:
                                            if prole not in player.roles:
                                                await player.add_roles(prole)
                                                print("[Points Roles] " + player.name + " was given " + prole.name +
                                                      " (required points:" + str(prolepoints) + ",has:" +
                                                      str(playerpoints) + ")")
                                        elif playerpoints < prolepoints:
                                            if prole in player.roles:
                                                await player.remove_roles(prole)
                                                print("[Points Roles] " + player.name + " had " + prole.name +
                                                      " removed (required points:" + str(prolepoints) + ",has:" +
                                                      str(playerpoints) + ")")
            # Demons Roles
            if alldatakeys("pcdroles.txt") != [] and alldatakeys("pcdata.txt") != []:
                for droleid in alldatakeys("pcdroles.txt"):
                    drole = getrole(channel.guild, droleid)
                    if drole is not None:
                        droledemons = datasettings(file="pcdroles.txt", method="get", line=droleid)
                        if droledemons is not None:
                            droledemons = droledemons.split(";")
                            for playerid in alldatakeys("pcdata.txt"):
                                player = getmember(channel.guild, playerid)
                                if player is not None:
                                    playerdata = PLAYERDATA(
                                        datasettings(file="pcdata.txt", method="get", line=playerid))
                                    if playerdata is not None:
                                        drolestatus = []
                                        for d in droledemons: drolestatus.append({'n': d, 'f': False})
                                        for dr in droledemons:
                                            for pd in playerdata['beaten']:
                                                if pd['name'].lower() == dr.lower():
                                                    for drs in drolestatus:
                                                        if drs['n'].lower() == pd['name'].lower(): drs['f'] = True
                                            for pv in playerdata['verified']:
                                                if pv['name'].lower() == dr.lower():
                                                    for drs in drolestatus:
                                                        if drs['n'].lower() == pv['name'].lower(): drs['f'] = True
                                        droledemonsfound = True
                                        for dr in drolestatus:
                                            if dr['f'] is False: droledemonsfound = False
                                        droletext = ""
                                        for d in droledemons: droletext += d + ", "
                                        droletext = droletext[:len(droletext) - 2]
                                        if droledemonsfound:
                                            if drole not in player.roles:
                                                await player.add_roles(drole)
                                                print("[Demons Roles] " + player.name + " was given " + drole.name +
                                                      " (required demons:" + str(droletext) + ")")
                                        elif not droledemonsfound:
                                            if drole in player.roles:
                                                await player.remove_roles(drole)
                                                print("[Demons Roles] " + player.name + " had " + drole.name +
                                                      " removed (required demons:" + str(droletext) + ")")
        print("[Auto Refresh] Roles Refresh finished")
        REFRESHACTIVE = False
        await asyncio.sleep(1800)

NRREVIEWRECORD = None

NRREVIEWRM = []

@client.event
async def on_message(message):
    global NRREVIEWRECORD
    if str(message.content).startswith("??setmoderator "):
        print("Recieved " + message.author.name + " " + message.content)
        if not memberadmin(message.author):
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not an Administrator!")
        else:
            smm = str(message.content).replace("??setmoderator ",""); smm = smm.replace("\"","")
            smmod = getrole(message.guild,smm)
            if smmod is None:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid role!")
            else:
                if datasettings(file="pcmods.txt",method="get",line="MODERATOR" + str(message.guild.id)) is None:
                    datasettings(file="pcmods.txt",method="add",newkey="MODERATOR" + str(message.guild.id),
                                 newvalue=str(smmod.id))
                    await message.add_reaction(emoji=CHAR_SUCCESS)
                    await message.channel.send(
                    "**" + message.author.name + "**: Set MODERATOR role to *" + smmod.name + "*")
                else:
                    datasettings(file="pcmods.txt", method="change", line="MODERATOR" + str(message.guild.id),
                                 newvalue=str(smmod.id))
                    await message.add_reaction(emoji=CHAR_SUCCESS)
                    await message.channel.send(
                    "**" + message.author.name + "**: Changed MODERATOR role to *" + smmod.name + "*")
    if str(message.content).startswith("??addpointsrole "):
        print("Recieved " + message.author.name + " " + message.content)
        if not membermoderator(message.author):
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not a Moderator!")
        else:
            prm = str(message.content).replace("??addpointsrole ","")
            prp = paramnumberlist(prm); prr = paramquotationlist(prm)
            if prr is None:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid role!")
            else:
                prr = getrole(message.guild,prr[0])
                if prr is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid role!")
                else:
                    if prp is None:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send(
                        "**Error**: Invalid points number!")
                    else:
                        prp = prp[0]
                        if datasettings(file="pcproles.txt",method="get",line=str(prr.id)) is not None:
                            await message.add_reaction(emoji=CHAR_FAILED)
                            await message.channel.send("**Error**: Points Role already exists for *" + prr.name +
                                                              "*!")
                        else:
                            datasettings(file="pcproles.txt",method="add",newkey=str(prr.id),newvalue=str(prp))
                            await message.add_reaction(emoji=CHAR_SUCCESS)
                            await message.channel.send("**" + message.author.name +
                            "**: Set *" + prr.name + "* to be a POINTS ROLE, points requirement: " + str(prp))
    if str(message.content).startswith("??removepointsrole "):
        print("Recieved " + message.author.name + " " + message.content)
        if not membermoderator(message.author):
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not a Moderator!")
        else:
            prm = str(message.content).replace("??removepointsrole ","")
            prr = paramquotationlist(prm)
            if prr is None:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid role!")
            else:
                prr = getrole(message.guild,prr[0])
                if prr is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid role!")
                else:
                    if datasettings(file="pcproles.txt",method="get",line=str(prr.id)) is None:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: Points Role doesn't exist for *" + prr.name +
                                                          "*!")
                    else:
                        datasettings(file="pcproles.txt",method="change",line=str(prr.id),newvalue="$REMOVED$")
                        await message.add_reaction(emoji=CHAR_SUCCESS)
                        await message.channel.send("**" + message.author.name +
                        "**: Removed *" + prr.name + "* as a POINTS ROLE")
    if str(message.content).startswith("??editpointsrole "):
        if not membermoderator(message.author):
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not a Moderator!")
        else:
            pem = str(message.content).replace("??editpointsrole ", ""); per = paramquotationlist(pem)
            if per is None:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid role!")
            else:
                prr = getrole(message.guild,per[0])
                if per is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid role!")
                else:
                    if datasettings(file="pcproles.txt",method="get",line=str(prr.id)) is None:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: Points Role doesn't exist for *" + prr.name +
                                                          "*!")
                    else:
                        pep = paramnumberlist(pem)
                        if pep is None:
                            await message.add_reaction(emoji=CHAR_FAILED)
                            await message.channel.send("**Error**: Invalid points number!")
                        else:
                            pep = pep[0]
                            if not isnumber(pep):
                                await message.add_reaction(emoji=CHAR_FAILED)
                                await message.channel.send("**Error**: Invalid points number!")
                            else:
                                datasettings(file="pcproles.txt", method="change", line=str(prr.id),
                                            newvalue=str(pep))
                                await message.add_reaction(emoji=CHAR_SUCCESS)
                                await message.channel.send("**" + message.author.name +
                                                           "**: Set *" + prr.name + "* POINTS ROLE number: " + str(pep))
    if str(message.content).startswith("??adddemonsrole "):
        print("Recieved " + message.author.name + " " + message.content)
        if not membermoderator(message.author):
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not a Moderator!")
        else:
            drm = str(message.content).replace("??adddemonsrole ","")
            drr = paramquotationlist(drm); drd = paramlistlist(drm,1)
            if drr is None:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid role!")
            else:
                drr = getrole(message.guild,drr[0])
                if drr is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid role!")
                else:
                    if drd is None:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: Invalid demons!")
                    else:
                        global DEMONSLIST
                        drdv = True; drdid = ""
                        for d in drd:
                            drdf = False
                            for ld in DEMONSLIST:
                                if str(d).lower() == ld['name'].lower(): drdf = True; break
                            if not drdf: drdid = d; drdv = False; break
                        if not drdv:
                            await message.add_reaction(emoji=CHAR_FAILED)
                            await message.channel.send("**Error**: Invalid demon *" + str(drdid) + "*")
                        else:
                            if datasettings(file="pcdroles.txt", method="get", line=str(drr.id)) is not None:
                                await message.add_reaction(emoji=CHAR_FAILED)
                                await message.channel.send("**Error**: Demons Role already exists for *" + drr.name + "*")
                            else:
                                drdt = ""
                                for d in drd: drdt += d + ";"
                                drdt = drdt[:len(drdt) - 1]
                                datasettings(file="pcdroles.txt",method="add",newkey=str(drr.id),newvalue=drdt)
                                await message.add_reaction(emoji=CHAR_SUCCESS)
                                await message.channel.send("**" + message.author.name + "**: Set *" + drr.name +
                                                           "* to be a DEMONS ROLE, demons requirement(s): " + drdt)
    if str(message.content).startswith("??removedemonsrole "):
        print("Recieved " + message.author.name + " " + message.content)
        if not membermoderator(message.author):
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not a Moderator!")
        else:
            drm = str(message.content).replace("??removedemonsrole ","")
            drr = paramquotationlist(drm)
            if drr is None:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid role!")
            else:
                drr = getrole(message.guild,drr[0])
                if drr is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid role!")
                else:
                    if datasettings(file="pcdroles.txt",method="get",line=str(drr.id)) is None:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: Demons Role doesn't exist for *" + drr.name +
                                                          "*!")
                    else:
                        datasettings(file="pcdroles.txt",method="change",line=str(drr.id),newvalue="$REMOVED$")
                        await message.add_reaction(emoji=CHAR_SUCCESS)
                        await message.channel.send("**" + message.author.name +
                        "**: Removed *" + drr.name + "* as a DEMONS ROLE")
    if str(message.content).startswith("??editdemonsrole "):
        print("Recieved " + message.author.name + " " + message.content)
        if not membermoderator(message.author):
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not a Moderator!")
        else:
            drm = str(message.content).replace("??editdemonsrole ","")
            drr = paramquotationlist(drm); drd = paramlistlist(drm,1)
            if drr is None:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid role!")
            else:
                drr = getrole(message.guild,drr[0])
                if drr is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid role!")
                else:
                    if drd is None:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: Invalid demons!")
                    else:
                        drdv = True; drdid = ""
                        for d in drd:
                            drdf = False
                            for ld in DEMONSLIST:
                                if str(d).lower() == ld['name'].lower(): drdf = True; break
                            if not drdf: drdid = d; drdv = False; break
                        if not drdv:
                            await message.add_reaction(emoji=CHAR_FAILED)
                            await message.channel.send("**Error**: Invalid demon *" + str(drdid) + "*")
                        else:
                            if datasettings(file="pcdroles.txt", method="get", line=str(drr.id)) is None:
                                await message.add_reaction(emoji=CHAR_FAILED)
                                await message.channel.send("**Error**: Demons Role doesn't exist for *" + drr.name + "*")
                            else:
                                drdt = ""
                                for d in drd: drdt += d + ";"
                                drdt = drdt[:len(drdt) - 1]
                                datasettings(file="pcdroles.txt",method="change",line=str(drr.id),newvalue=drdt)
                                await message.add_reaction(emoji=CHAR_SUCCESS)
                                await message.channel.send("**" + message.author.name + "**: Set *" + drr.name +
                                                           "* DEMONS ROLE demons requirement(s): " + drdt)
    if str(message.content).startswith("??playerlink "):
        if inallowedguild(message.guild,message.author):
            print("Recieved " + message.author.name + " " + message.content)
            if not membermoderator(message.author):
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: You are not a Moderator!")
            else:
                plm = str(message.content).replace("??playerlink ", "")
                plm = paramquotationlist(plm)
                if len(plm) != 2:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid parameters!")
                else:
                    plu = plm[0]
                    plp = plm[1]
                    if plu is None:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: Invalid member!")
                    else:
                        plu = getmember(message.guild,plu)
                        if plu is None:
                            await message.add_reaction(emoji=CHAR_FAILED)
                            await message.channel.send("**Error**: Invalid member!")
                        else:
                            if plp is None:
                                await message.add_reaction(emoji=CHAR_FAILED)
                                await message.channel.send(
                                "**Error**: Invalid player ID!")
                            else:
                                if not isnumber(plp):
                                    await message.add_reaction(emoji=CHAR_FAILED)
                                    await message.channel.send(
                                    "**Error**: Invalid player ID!")
                                else:
                                    plpd = PLAYERDATA(plp)
                                    if plpd is None:
                                        await message.add_reaction(emoji=CHAR_FAILED)
                                        await message.channel.send("**Error**: Invalid player ID!")
                                    else:
                                        plphp = True
                                        try: pt = plpd['beaten']
                                        except: plphp = False
                                        if not plphp:
                                            await message.add_reaction(emoji=CHAR_FAILED)
                                            await message.channel.send(
                                                "**Error**: User does not have any List Points!")
                                        else:
                                            if datasettings(file="pcdata.txt",method="get",line=str(plu.id)) is not None:
                                                await message.add_reaction(emoji=CHAR_FAILED)
                                                await message.channel.send("**Error**: User already linked to that Player ID")
                                            else:
                                                datasettings(file="pcdata.txt",method="add",newkey=str(plu.id),newvalue=plp)
                                                await message.add_reaction(emoji=CHAR_SUCCESS)
                                                await message.channel.send("**" +
                                                message.author.name + "**: Linked *" + plu.name + "* to *" + str(plp) + "* (" +
                                                                                                            plpd['name'] + ")")
    if str(message.content).startswith("??playerunlink "):
        if inallowedguild(message.guild,message.author):
            print("Recieved " + message.author.name + " " + message.content)
            if not membermoderator(message.author):
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: You are not a Moderator!")
            else:
                plm = str(message.content).replace("??playerunlink ", "")
                plm = paramquotationlist(plm)
                if len(plm) != 2:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid parameters!")
                else:
                    plu = plm[0]
                    plp = plm[1]
                    if plu is None:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: Invalid member!")
                    else:
                        plu = getmember(message.guild,plu)
                        if plu is None:
                            await message.add_reaction(emoji=CHAR_FAILED)
                            await message.channel.send("**Error**: Invalid member!")
                        else:
                            if plp is None:
                                await message.add_reaction(emoji=CHAR_FAILED)
                                await message.channel.send(
                                "**Error**: Invalid player ID!")
                            else:
                                if not isnumber(plp):
                                    await message.add_reaction(emoji=CHAR_FAILED)
                                    await message.channel.send(
                                    "**Error**: Invalid player ID!")
                                else:
                                    plpd = PLAYERDATA(plp)
                                    if plpd is None:
                                        await message.add_reaction(emoji=CHAR_FAILED)
                                        await message.channel.send("**Error**: Invalid player ID!")
                                    else:
                                        if datasettings(file="pcdata.txt",method="get",line=str(plu.id)) is None:
                                            await message.add_reaction(emoji=CHAR_FAILED)
                                            await message.channel.send("**Error**: User not already linked to that Player ID")
                                        else:
                                            datasettings(file="pcdata.txt",method="change",line=str(plu.id),newvalue="$REMOVED$")
                                            await message.add_reaction(emoji=CHAR_SUCCESS)
                                            await message.channel.send("**" +
                                            message.author.name + "**: Unlinked *" + plu.name + "* from *" + str(plp) +
                                                                                                          "* (" +
                                                                                                        plpd['name'] + ")")
    if str(message.content) == "??refresh":
        print("Recieved " + message.author.name + " " + message.content)
        if not membermoderator(message.author):
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not a Moderator!")
        else:
            global REFRESHACTIVE; global REFRESHIN
            if REFRESHACTIVE:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**" + message.author.name + "**: Refresh in Progress (" + REFRESHIN + ")")
            else:
                if not bothasperms(message.guild):
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Killbot Circles doesn\'t have permission to add Roles!")
                else:
                    REFRESHACTIVE = True
                    REFRESHIN = message.guild.name
                    await message.add_reaction(emoji=CHAR_SUCCESS)
                    await message.channel.send("**" + message.author.name + "**: Manual Refresh started")
                    pacount = 0; prcount = 0; dacount = 0; drcount = 0; ipcount = []; posacount = 0; posrcount = 0
                    nddcount = 0
                    roleconflict = False
                    print("[Manual Refresh] Roles Refresh started")
                    DEMONSLISTREFRESH()
                    if alldatakeys("pcdata.txt") != []:
                        for playerid in alldatakeys("pcdata.txt"):
                            player = getmember(message.channel.guild, playerid)
                            if player is None: continue
                            playerdata = PLAYERDATA(
                                datasettings(file="pcdata.txt", method="get", line=playerid))
                            # Points Roles & Log Points
                            for proleid in alldatakeys("pcproles.txt"):
                                prole = getrole(message.channel.guild, proleid)
                                if prole is not None:
                                    prolepoints = datasettings(file="pcproles.txt", method="get", line=proleid)
                                    if prolepoints == "$REMOVED$":
                                        for member in message.guild.members:
                                            if prole in member.roles:
                                                try: await player.remove_roles(prole)
                                                except discord.errors.Forbidden: roleconflict = True
                                                prcount += 1
                                                print("[Points Roles] " + player.name + " had " + prole.name +
                                                      " removed (Role removed")
                                                datasettings(file="pcproles.txt",method="remove",line=proleid)
                                    else:
                                        if prolepoints is not None:
                                            prolepoints = int(prolepoints)
                                            try: playerpoints = int(POINTSFORMULA(playerdata))
                                            except: continue
                                            logpoints(datasettings(file="pcdata.txt", method="get", line=playerid),
                                                      playerpoints)
                                            if playerpoints >= prolepoints:
                                                if prole not in player.roles:
                                                    try: await player.add_roles(prole)
                                                    except discord.errors.Forbidden:
                                                        roleconflict = True
                                                    pacount += 1
                                                    print("[Points Roles] " + player.name + " was given " + prole.name +
                                                          " (required points:" + str(prolepoints) + ",has:" +
                                                          str(playerpoints) + ")")
                                            elif playerpoints < prolepoints:
                                                if prole in player.roles:
                                                    try: await player.remove_roles(prole)
                                                    except discord.errors.Forbidden:
                                                        roleconflict = True
                                                    prcount += 1
                                                    print("[Points Roles] " + player.name + " had " + prole.name +
                                                          " removed (required points:" + str(prolepoints) + ",has:" +
                                                          str(playerpoints) + ")")
                            # Demons Roles
                            for droleid in alldatakeys("pcdroles.txt"):
                                drole = getrole(message.channel.guild, droleid)
                                if drole is not None:
                                    droledemons = datasettings(file="pcdroles.txt", method="get", line=droleid)
                                    if droledemons == "$REMOVED$":
                                        for member in message.guild.members:
                                            if drole in member.roles:
                                                try: await member.remove_roles(drole)
                                                except discord.errors.Forbidden:
                                                    roleconflict = True
                                                drcount += 1
                                                print("[Demons Roles] " + player.name + " had " + drole.name +
                                                      " removed (Role removed)")
                                                datasettings(file="pcdroles.txt",method="remove",line=droleid)
                                    else:
                                        if droledemons is not None:
                                            droledemons = droledemons.split(";")
                                            drolestatus = []
                                            for d in droledemons: drolestatus.append({'n': d, 'f': False})
                                            if playerdata is None: continue
                                            for dr in droledemons:
                                                for pd in playerdata['beaten']:
                                                    if pd['name'].lower() == dr.lower():
                                                        for drs in drolestatus:
                                                            if drs['n'].lower() == pd['name'].lower(): drs['f'] = True
                                                for pv in playerdata['verified']:
                                                    if pv['name'].lower() == dr.lower():
                                                        for drs in drolestatus:
                                                            if drs['n'].lower() == pv['name'].lower(): drs['f'] = True
                                            droledemonsfound = True
                                            for dr in drolestatus:
                                                if dr['f'] is False: droledemonsfound = False
                                            droletext = ""
                                            for d in droledemons: droletext += d + ", "
                                            droletext = droletext[:len(droletext) - 2]
                                            if droledemonsfound:
                                                if drole not in player.roles:
                                                    try: await player.add_roles(drole)
                                                    except discord.errors.Forbidden:
                                                        roleconflict = True
                                                    dacount += 1
                                                    print("[Demons Roles] " + player.name + " was given " + drole.name +
                                                          " (required demons:" + str(droletext) + ")")
                                            elif not droledemonsfound:
                                                if drole in player.roles:
                                                    try: await player.remove_roles(drole)
                                                    except discord.errors.Forbidden:
                                                        roleconflict = True
                                                    drcount += 1
                                                    print("[Demons Roles] " + player.name + " had " + drole.name +
                                                          " removed (required demons:" + str(droletext) + ")")
                            # Timed Bans
                            if alldatakeys("pctimedbans.txt") != []:
                                for ugv in alldatakeys("pctimedbans.txt"):
                                    ugid = str(ugv).split("+"); g = getguild(ugid[1]); u = getmember(g, ugid[0])
                                    if u is not None and g is not None:
                                        tbt = datasettings(file="pctimedbans.txt", method="get", line=ugv); tbt = tbt.split("-")
                                        tbt = datetime.datetime(day=int(tbt[2]), month=int(tbt[1]), year=int(tbt[0]))
                                        if tbt <= datetime.datetime.now():
                                            tbdc = None
                                            for guild in client.guilds:
                                                for channel in guild:
                                                    if str(channel.id) == datasettings(file="pcvars.txt", method="get",
                                                                                       line="FEEDBACKCHANNEL"):
                                                        tbdc = channel
                                            try: await g.unban(u)
                                            except: pass
                                            datasettings(file="pctimedbans.txt", method="remove", line=ugv)
                                            await tbdc.send(
                                                "A Timed Ban has expired!\n**Server**: " + g.name + "\n**User**: " + u.name)
                                            print("[Timed Ban] Unbanned " + u.name)
                            # Positional Roles
                            if alldatakeys("pcposroles.txt") != []:
                                for posroleid in alldatakeys("pcposroles.txt"):
                                    posrole = getrole(message.channel.guild,posroleid)
                                    if posrole is not None:
                                        posdata = datasettings(file="pcposroles.txt",method="get",line=str(posrole.id))
                                        if posdata == "$REMOVED$":
                                            for member in message.guild.members:
                                                if posrole in member.roles:
                                                    try: await player.remove_roles(posrole)
                                                    except discord.errors.Forbidden:
                                                        roleconflict = True
                                                    posrcount += 1
                                                    print("[Positonal Roles] " + player.name + " had " + posrole.name +
                                                          "removed (Role removed)")
                                                    datasettings(file="pcposroles.txt", method="remove", line=posroleid)
                                        else:
                                            posdata = posdata.split("-"); posreq = int(posdata[0]); posnum = int(posdata[1])
                                            pposfound = 0
                                            playerhasdemons = True
                                            try: pbt = playerdata['beaten']
                                            except:
                                                ipcount.append({'name': player, 'pid': datasettings(file="pcdata.txt",
                                                                                                    method="get", line=playerid)})
                                                playerhasdemons = False
                                            if playerhasdemons:
                                                for pb in playerdata['beaten']:
                                                    if int(pb['position']) <= posreq: pposfound += 1
                                                for pv in playerdata['verified']:
                                                    if int(pv['position']) <= posreq: pposfound += 1
                                                if pposfound >= posnum:
                                                    if posrole not in player.roles:
                                                        try: await player.add_roles(posrole)
                                                        except discord.errors.Forbidden:
                                                            roleconflict = True
                                                        posacount += 1
                                                        print("[Positonal Roles] " + player.name + " was given " + posrole.name +
                                                              " (base position:" + str(posreq) + ",number required:" + str(posnum) + ",has:"
                                                              + str(pposfound))
                                                elif pposfound < posnum:
                                                    if posrole in player.roles:
                                                        try: await player.remove_roles(posrole)
                                                        except discord.errors.Forbidden:
                                                            roleconflict = True
                                                        posrcount += 1
                                                        print("[Positonal Roles] " + player.name + " had " + posrole.name +
                                                              "removed (base position:" + str(posreq) + ",number required:" + str(posnum) +
                                                              ",has:" + str(pposfound))
                            # Invalid Players
                            if playerdata is None: ipcount.append({'name':player,'pid':datasettings(
                                file="pcdata.txt", method="get", line=playerid)})
                    # New Demon Channels
                    ndcl = strtolist(datasettings(file="pcvars.txt", method="get", line="NEWDEMONSCHANNELS"))
                    if len(ndcl) != 0:
                        for dc in ndcl:
                            for channel in message.guild.channels:
                                if str(channel.id) == dc:
                                    dmd = []
                                    async for dm in channel.history(limit=20):
                                        if dm.author.id == 358598636436979713 and dm.created_at > \
                                                (datetime.datetime.now() - datetime.timedelta(days=13)):
                                            try: dme = dm.embeds[0].to_dict()
                                            except: continue
                                            for dmef in dme['fields']:
                                                if "`u!level " in dmef['value']:
                                                    p1 = dmef['value'].index("`") + 1; p = dmef['value'][p1:]
                                                    p2 = p.index("`"); p = p[:p2]; p = p.replace("`","")
                                                    p = p.replace("u!level ","")
                                                    ldata = getanylevel(p)
                                                    if ldata != []:
                                                        ldifa = ["Hard Demon","Insane Demon","Extreme Demon"]
                                                        if ldata["Difficulty"] not in ldifa:
                                                            dmd.append(dm)
                                                            nddcount += 1
                                                            print("[NDCD] Deleted " + ldata["Name"] + " because it is "
                                                                  + ldata['Difficulty'] + " [Guild:" + message.guild.name
                                                                  + "]")
                                    await channel.delete_messages(dmd)
                    print("[Manual Refresh] Roles Refresh finished")
                    if roleconflict:
                        await message.channel.send("*(Some roles could not be added due to them having a higher "
                                                   "hierarchy than this Bot\'s Role)*")
                    await message.channel.send("**" + message.author.name +
                                               "**: Manual Refresh finished [Added " + str(pacount) + "/Removed " +
                                               str(prcount) + " Points Roles, Added " + str(dacount) + "/Removed " +
                                               str(drcount) + " Demons Roles, Added " + str(posacount) + "/Removed " +
                                               str(posrcount) + " Positional Roles, Removed " + str(nddcount) +
                                               " Non-Extreme/Insane/Hard Demons from New-Rated-Demons Channels]")
                    if len(ipcount) > 0:
                        ipn = ""
                        for i in ipcount:
                            ipn += i['name'].name + ": " + str(i['pid']) + ", "
                            datasettings(file="pcdata.txt",method="remove",line=str(i['name'].id))
                        ipn = ipn[:len(ipn) - 2]
                        await message.channel.send("**NOTE!** The following players were removed from the Player Link "
                                                   "database because they had Invalid IDs or haven't beaten List Demons:\n" + ipn)
                    REFRESHACTIVE = False
                    REFRESHIN = None
                    await client.change_presence(activity=discord.Game(name=(DEMONSLIST[random.randint(0,99)])['name']))
    if str(message.content).startswith("??feedback "):
        if str(message.author.id) in alldatakeys("pcfb.txt"):
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not allowed to send Feedbacks!")
        else:
            fbm = str(message.content).replace("??feedback ",""); fbm = paramquotationlist(fbm)
            if len(fbm) != 2:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid Parameters!")
            else:
                fbd = fbm[0]
                fbv = True
                try: fbd = int(fbd)
                except: fbv = False
                if not fbv:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid Demon!")
                else:
                    if fbd < 1 or fbd > len(DEMONSLIST):
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: Invalid Demon!")
                    else:
                        if linkedplayer(message.author.id) is None:
                            await message.add_reaction(emoji=CHAR_FAILED)
                            await message.channel.send("**Error**: You are not Linked to a Pointercrate Player!")
                        else:
                            fbpd = PLAYERDATA(linkedplayer(message.author.id))
                            if fbpd is None:
                                await message.add_reaction(emoji=CHAR_FAILED)
                                await message.channel.send("**Error**: You are linked to an Invalid Player!")
                            else:
                                fbdf = False
                                fbdn = "your meat"
                                for d in DEMONSLIST:
                                    if fbd == d['position']: fbdn = d['name']
                                for d in fbpd['beaten']:
                                    if d['position'] == fbd: fbdf = True
                                for d in fbpd['verified']:
                                    if d['position'] == fbd: fbdf = True
                                if not fbdf:
                                    await message.add_reaction(emoji=CHAR_FAILED)
                                    await message.channel.send("**Error**: You have not beaten " + fbdn + "!")
                                else:
                                    fbc = fbm[1]
                                    if fbc == "":
                                        await message.add_reaction(emoji=CHAR_FAILED)
                                        await message.channel.send("**Error**: Invalid message!")
                                    else:
                                        fbfw = False
                                        if alldatakeys("pcfeed.txt") != []:
                                            for gf in alldatakeys("pcfeed.txt"):
                                                fgf = datasettings(file="pcfeed.txt",method="get",line=gf)
                                                fgf = fgf.split(";")
                                                if fgf[0] == linkedplayer(message.author.id) and fgf[1] == str(fbd):
                                                    await message.add_reaction(emoji=CHAR_FAILED)
                                                    await message.channel.send("**Error**: You have already written Feedback for "
                                                                               + fbdn + "!")
                                                    fbfw = True; break
                                            if not fbfw:
                                                fbch = None
                                                for guild in client.guilds:
                                                    for channel in guild.channels:
                                                        if str(channel.id) == datasettings(file="pcvars.txt", method="get",
                                                                                      line="FEEDBACKCHANNEL"):
                                                            fbch = channel
                                                fbfm = "New Feedback from " + message.guild.name + "!\n**User**: " + \
                                                       message.author.name + "\n**Demon**: " + fbdn + "\n**Feedback**: " + fbc
                                                await fbch.send(fbfm)
                                                datasettings(file="pcfeed.txt", method="add",
                                                             newkey="feedback" + str(random.randint(10000, 99999)),
                                                             newvalue=linkedplayer(message.author.id) + ";" + str(fbd))
                                                await message.add_reaction(emoji=CHAR_SUCCESS)
                                                await message.channel.send("**" + message.author.name + "**: Feedback for "
                                                                           + fbdn + " sent!")
                                        else:
                                            fbch = None
                                            for guild in client.guilds:
                                                for channel in guild.channels:
                                                    if str(channel.id) == datasettings(file="pcvars.txt",method="get",
                                                                                  line="FEEDBACKCHANNEL"):
                                                        fbch = channel
                                            fbfm = "New Feedback from " + message.guild.name + "!\n**User**: " + \
                                                   message.author.name + "\n**Demon**: " + fbdn + "\n**Feedback**: " + fbc
                                            await fbch.send(fbfm)
                                            datasettings(file="pcfeed.txt",method="add",
                                                         newkey="feedback" + str(random.randint(10000,99999)),
                                                         newvalue=linkedplayer(message.author.id) + ";" + str(fbd))
                                            await message.add_reaction(emoji=CHAR_SUCCESS)
                                            await message.channel.send("**" + message.author.name + "**: Feedback for "
                                                                       + fbdn + " sent!")
    if str(message.content).startswith("??feedbackban "):
        if inallowedguild(message.guild,message.author):
            fbm = str(message.content).replace("??feedbackban ", ""); fbm = paramquotationlist(fbm)
            if not membermoderator(message.author):
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: You are not a Moderator!")
            else:
                if len(fbm) != 1:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid Parameters!")
                else:
                    fbp = fbm[0]
                    fbp = getmember(message.guild,fbp)
                    if fbp is None:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: Invalid Parameters!")
                    else:
                        if alldatakeys("pcfb.txt") != []:
                            if str(fbp.id) in alldatakeys("pcfb.txt"):
                                datasettings(file="pcfb.txt",method="remove",line=str(fbp.id))
                                await message.add_reaction(emoji=CHAR_SUCCESS)
                                await message.channel.send("**" + message.author.name + "**: " + fbp.name +
                                                           " has been unbanned from sending Feedbacks!")
                            else:
                                datasettings(file="pcfb.txt", method="add", newkey=str(fbp.id))
                                await message.add_reaction(emoji=CHAR_SUCCESS)
                                await message.channel.send("**" + message.author.name + "**: " + fbp.name +
                                                           " has been banned from sending Feedbacks!")
                        else:
                            datasettings(file="pcfb.txt", method="add", newkey=str(fbp.id))
                            await message.add_reaction(emoji=CHAR_SUCCESS)
                            await message.channel.send("**" + message.author.name + "**: " + fbp.name +
                                                       " has been banned from sending Feedbacks!")
    if str(message.content).startswith("??tempban "):
        print("Recieved " + message.author.name + " " + message.content)
        if not membermoderator(message.author):
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not a Moderator!")
        else:
            tbm = str(message.content).replace("??tempban ",""); tbp = paramquotationlist(tbm)
            tbd = paramnumberlist(tbm)
            if len(tbp) != 1:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send(
                    "**Error**: Invalid member!")
            else:
                tbp = tbp[0]
                tbp = getmember(message.guild,tbp)
                if tbp is not None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send(
                        "**Error**: Invalid member!")
                else:
                    if len(tbd) != 1:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send(
                            "**Error**: Invalid number of days!")
                    else:
                        tbdv = True
                        try: tbd = int(tbd)
                        except: tbdv = False
                        if not tbdv:
                            await message.add_reaction(emoji=CHAR_FAILED)
                            await message.channel.send(
                                "**Error**: Invalid number of days!")
                        else:
                            tbed = datetime.datetime.now() + datetime.timedelta(days=tbd)
                            tbed = str(tbed)[:str(tbed).index(" ")]
                            await message.guild.ban(tbp)
                            datasettings(file="pctimedbans.txt",method="add",newkey=str(tbp.id) + "+" +
                                                                                    str(message.guild.id),newvalue=tbed)
                            await message.add_reaction(emoji=CHAR_SUCCESS)
                            await message.channel.send("**" + message.author.name +
                                                       "**: *" + tbp.name + "* has been BANNED for " + str(tbd) +
                                                       " day(s)")
    if str(message.content).startswith("??info"):
        iplayer = message.author
        ipv = True
        if str(message.content).startswith("??info "):
            im = str(message.content).replace("??info ",""); imp = paramquotationlist(im)
            if imp is None:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send(
                    "**Error**: Invalid player!")
                ipv = False
            else:
                imp = getmember(message.guild,imp[0])
                if imp is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send(
                        "**Error**: This user is not Linked to a Pointercrate Player!")
                    ipv = False
                else: iplayer = imp
        if ipv:
            if str(iplayer.id) not in alldatakeys("pcdata.txt"):
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send(
                    "**Error**: This user is not Linked to a Pointercrate Player!")
            else:
                pid = PLAYERDATA(datasettings(file="pcdata.txt",method="get",line=str(iplayer.id)))
                if pid is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send(
                        "**Error**: You are linked to an Invalid Player!")
                else:
                    pihd = {'name':"None",'position':999}
                    for d in pid['beaten']:
                        if int(d['position']) < int(pihd['position']): pihd = d
                    for d in pid['verified']:
                        if int(d['position']) < int(pihd['position']): pihd = d
                    pipr = []
                    pidr = []
                    pipsr = []
                    for pr in alldatakeys("pcproles.txt"):
                        for r in iplayer.roles:
                            if str(r.id) == str(pr): pipr.append(r.name)
                    for dr in alldatakeys("pcdroles.txt"):
                        for r in iplayer.roles:
                            if str(r.id) == str(dr): pidr.append(r.name)
                    for psr in alldatakeys("pcposroles.txt"):
                        for r in iplayer.roles:
                            if str(r.id) == str(psr): pipsr.append(r.name)
                    pipl = "None"
                    if len(pipr) == 0: pipl = "None"
                    elif len(pipr) > 0:
                        pipl = ""
                        for pr in pipr: pipl += pr + ", "
                        pipl = pipl[:len(pipl) - 2]
                    if pipl == "": pipl = "None"
                    pidl = "None"
                    if len(pidr) == 0: pidl = "None"
                    elif len(pidr) > 0:
                        pidl = ""
                        for dr in pidr: pidl += dr + ", "
                        pidl = pidl[:len(pidl) - 2]
                    if pidr == "": pidr = "None"
                    pipsl = "None"
                    if len(pidr) == 0:
                        pipsl = "None"
                    elif len(pidr) > 0:
                        pipsl = ""
                        for psr in pipsl: pipsl += psr + ", "
                        pipsl = pipsl[:len(pipsl) - 2]
                    if pipsl == "": pipsl = "None"
                    pimd = 0; pied = 0; pild = 0
                    for d in pid['beaten']:
                        if int(d['position']) < 51: pimd += 1
                        elif int(d['position']) < 101 and int(d['position']) > 50: pied += 1
                        else: pild += 1
                    pim = "`------USER INFORMATION FOR   `**" + iplayer.name + "**`  ---`"
                    pim +="\n**User ID**: " + str(iplayer.id)
                    pim +="\n**Linked Pointercrate Account**: " + pid['name']
                    pim +=" (ID: " + datasettings(file="pcdata.txt",method="get",line=str(iplayer.id))
                    pim +=")\n`-----------POINTERCRATE STATS-----------`\n**List Points**: " + str(POINTSFORMULA(pid))
                    pim +="\n**Demons Completed**: " + str(len(pid['beaten'])) + " [" + str(pimd) + " Main, " + str(pied) \
                          + " Extended, " + str(pild) + " Legacy, " + str(len(pid['verified']) + len(pid['published']) +
                                                                len(pid['created'])) + " Published/Verified/Created]"
                    pim +="\n**Hardest Demon**: " + pihd['name'] + "\n**Banned**: " + str(pid['banned']) + "\n"
                    pim += "**Points Roles**: " + str(pipl) + "\n**Demons Roles**: " + str(pidl) + \
                           "\n**Positional Roles**: " + str(pipsl)
                    await message.add_reaction(emoji=CHAR_SUCCESS)
                    await message.channel.send(pim)
    if str(message.content).startswith("??addpositionalrole "):
        print("Recieved " + message.author.name + " " + message.content)
        if not membermoderator(message.author):
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not a Moderator!")
        else:
            prm = str(message.content).replace("??addpositionalrole ",""); prr = paramquotationlist(prm)
            prp = paramnumberlist(prm)
            if len(prr) != 1:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid role!")
            else:
                prr = prr[0]
                prr = getrole(message.guild,prr)
                if prr is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid role!")
                else:
                    if len(prp) != 2:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: Invalid parameters!")
                    else:
                        prpos = prp[0]
                        prpv = True
                        try: prpos = int(prpos)
                        except:
                            await message.add_reaction(emoji=CHAR_FAILED)
                            await message.channel.send("**Error**: Invalid position!")
                            prpv = False
                        if prpv:
                            if prpos < 1 or prpos > 100:
                                await message.add_reaction(emoji=CHAR_FAILED)
                                await message.channel.send("**Error**: Invalid position!")
                            else:
                                prnum = prp[1]
                                prpv = True
                                try: prnum = int(prnum)
                                except:
                                    await message.add_reaction(emoji=CHAR_FAILED)
                                    await message.channel.send("**Error**: Invalid number of Positional demons!")
                                    prpv = False
                                if prpv:
                                    if prnum > prpos or prnum < 1:
                                        await message.add_reaction(emoji=CHAR_FAILED)
                                        await message.channel.send("**Error**: Invalid number of Positional demons!")
                                    else:
                                        if datasettings(file="pcposroles.txt",method="get",line=str(prr.id)) is not None:
                                            await message.add_reaction(emoji=CHAR_FAILED)
                                            await message.channel.send("**Error**: Positional Role already exists for "
                                                                       + prr.name + "!")
                                        else:
                                            datasettings(file="pcposroles.txt",method="add",newkey=str(prr.id),
                                                         newvalue=str(prpos) + "-" + str(prnum))
                                            await message.add_reaction(emoji=CHAR_SUCCESS)
                                            await message.channel.send("**" + message.author.name + "**: *" + prr.name +
                                            "* added as a POSITIONAL ROLE, position requirement: " + str(prpos) +
                                                ", number of demons in that positional range required: " + str(prnum))
    if str(message.content).startswith("??removepositionalrole "):
        if not membermoderator(message.author):
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not a Moderator!")
        else:
            prm = str(message.content).replace("??removepositionalrole ",""); prr = paramquotationlist(prm)
            if len(prr) != 1:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid role!")
            else:
                prr = getrole(message.guild,prr[0])
                if prr is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid role!")
                else:
                    if datasettings(file="pcposroles.txt",method="get",line=str(prr.id)) is None:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: " + prr.name + " is not a Positional Role!")
                    else:
                        datasettings(file="pcposroles.txt",method="change",line=str(prr.id),newvalue="$REMOVED$")
                        await message.add_reaction(emoji=CHAR_SUCCESS)
                        await message.channel.send("**" + message.author.name + "**: Removed *" + prr.name +
                                                   "* as a POSITIONAL ROLE!")
    if str(message.content).startswith("??editpositionalrole "):
        print("Recieved " + message.author.name + " " + message.content)
        if not membermoderator(message.author):
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not a Moderator!")
        else:
            prm = str(message.content).replace("??editpositionalrole ",""); prr = paramquotationlist(prm)
            prp = paramnumberlist(prm)
            if len(prr) != 1:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid role!")
            else:
                prr = prr[0]
                prr = getrole(message.guild,prr)
                if prr is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid role!")
                else:
                    if len(prp) != 2:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: Invalid parameters!")
                    else:
                        prpos = prp[0]
                        prpv = True
                        try: prpos = int(prpos)
                        except:
                            await message.add_reaction(emoji=CHAR_FAILED)
                            await message.channel.send("**Error**: Invalid position!")
                            prpv = False
                        if prpv:
                            if prpos < 1 or prpos > 100:
                                await message.add_reaction(emoji=CHAR_FAILED)
                                await message.channel.send("**Error**: Invalid position!")
                            else:
                                prnum = prp[1]
                                prpv = True
                                try: prnum = int(prnum)
                                except:
                                    await message.add_reaction(emoji=CHAR_FAILED)
                                    await message.channel.send("**Error**: Invalid number of Positional demons!")
                                    prpv = False
                                if prpv:
                                    if prnum > prpos or prnum < 1:
                                        await message.add_reaction(emoji=CHAR_FAILED)
                                        await message.channel.send("**Error**: Invalid number of Positional demons!")
                                    else:
                                        if datasettings(file="pcposroles.txt",method="get",line=str(prr.id)) is None:
                                            await message.add_reaction(emoji=CHAR_FAILED)
                                            await message.channel.send("**Error**: Positional Role doesn't exist for "
                                                                       + prr.name + "!")
                                        else:
                                            datasettings(file="pcposroles.txt",method="change",line=str(prr.id),
                                                         newvalue=str(prpos) + "-" + str(prnum))
                                            await message.add_reaction(emoji=CHAR_SUCCESS)
                                            await message.channel.send("**" + message.author.name + "**: Set *" + prr.name +
                                            "* POSITIONAL ROLE position requirement: " + str(prpos) +
                                                ", number of demons in that positional range required: " + str(prnum))
    if str(message.content).startswith("??setnewdemonschannel "):
        if not membermoderator(message.author):
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not a Moderator!")
        else:
            ndcm = str(message.content).replace("??setnewdemonschannel ",""); ndcp = paramquotationlist(ndcm)
            if len(ndcp) != 1:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid parameters!")
            else:
                ndcp = getchannel(message.guild,ndcp[0])
                if ndcp is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid channel!")
                else:
                    if str(ndcp.id) in strtolist(datasettings(file="pcvars.txt",method="get",line="NEWDEMONSCHANNELS")):
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: *" + ndcp.name + "* is already set as a NEW DEMONS "
                                                                                "CHANNEL to watch!")
                    else:
                        ndcl = strtolist(datasettings(file="pcvars.txt",method="get",line="NEWDEMONSCHANNELS"))
                        ndcl.append(str(ndcp.id))
                        datasettings(file="pcvars.txt",method="change",line="NEWDEMONSCHANNELS",newvalue=str(ndcl))
                        await message.add_reaction(emoji=CHAR_SUCCESS)
                        await message.channel.send("**" + message.author.name + "**: Set a NEW DEMONS CHANNEL to *"
                                                   + ndcp.name + "*")
    if str(message.content).startswith("??getnotified"):
        gnp = linkedplayer(str(message.author.id))
        if gnp is None:
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not linked to a Pointercrate Player!")
        else:
            gn = datasettings(file="pcn.txt",method="get",line=str(message.author.id))
            if gn is None:
                datasettings(file="pcn.txt", method="add", newkey=str(message.author.id),newvalue=gnp)
                await message.add_reaction(CHAR_SUCCESS)
                await message.channel.send("**" + message.author.name + "**: You will no longer be Notified whenever a Record you "
                                                                      "submitted is seen!")
            else:
                datasettings(file="pcn.txt",method="remove",line=str(message.author.id))
                await message.add_reaction(CHAR_SUCCESS)
                await message.channel.send("**" + message.author.name + "**: You will be Notified whenever a "
                                                                      "Record you submitted is seen!")
    if str(message.content).startswith("??kcroles"):
        droles = []; posroles = []; proles = []
        for did in alldatakeys("pcdroles.txt"):
            drole = getrole(message.guild,did)
            if drole is not None:
                drolecount = 0
                for m in message.guild.members:
                    if drole in m.roles: drolecount += 1
                droledemons = datasettings(file="pcdroles.txt",method="get",line=did)
                droles.append("[" + str(drolecount) + "]*" + drole.name + "* - " + droledemons)
        for pid in alldatakeys("pcproles.txt"):
            prole = getrole(message.guild,pid)
            if prole is not None:
                prolecount = 0
                for m in message.guild.members:
                    if prole in m.roles: prolecount += 1
                prolepoints = datasettings(file="pcproles.txt",method="get",line=pid)
                proles.append("[" + str(prolecount) + "]*" + prole.name + "* - " + prolepoints)
        for posid in alldatakeys("pcposroles.txt"):
            posrole = getrole(message.guild,posid)
            if posrole is not None:
                posrolecount = 0
                for m in message.guild.members:
                    if posrole in m.roles: posrolecount += 1
                posdata = datasettings(file="pcposroles.txt",method="get",line=posid)
                posdata = posdata.split("-"); posnum = posdata[0]; posreq = posdata[1]
                posroles.append("[" + str(posrolecount) + "]*" + posrole.name + "* - POS: " + posnum + ", REQ: " + posreq)
        if len(droles) == 0 and len(proles) == 0 and len(posroles) == 0:
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: No Killbot Circles roles exist for this Guild!")
        else:
            kcrm = "Listing all Killbot Circles roles for **" + message.guild.name + "** and how many Members have them:\n"
            if len(droles) != 0:
                kcrm += "**Demons Roles**:\n"
                for d in droles: kcrm += d + "\n"
            if len(proles) != 0:
                kcrm += "**Points Roles**:\n"
                for p in proles: kcrm += p + "\n"
            if len(posroles) != 0:
                kcrm += "**Positional Roles**:\n"
                for pos in posroles: kcrm += pos + "\n"
            await message.add_reaction(emoji=CHAR_SUCCESS)
            await message.channel.send(kcrm)
    if str(message.content).startswith("??whohas "):
        whm = str(message.content).replace("??whohas ",""); whp = paramquotationlist(whm)
        if whp is None:
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: Invalid parameters!")
        else:
            if len(whp) != 1:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid parameters!")
            else:
                whr = getrole(message.guild,whp[0])
                if whr is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid role!")
                else:
                    whpl = ""; whc = 0
                    for m in message.guild.members:
                        if whr in m.roles: whpl += m.name + ", "; whc += 1
                    whpl = whpl[:len(whpl) - 2]
                    whrm = str(whc) + " member(s) have **" + whr.name + "**:\n"
                    for did in alldatakeys("pcdroles.txt"):
                        if did == str(whr.id):
                            whrm += "*This role is a DEMONS ROLE, demon requirements: " + datasettings(file="pcdroles.txt",
                                                                                            method="get",line=did) + "*\n"
                    for pid in alldatakeys("pcproles.txt"):
                        if pid == str(whr.id):
                            whrm += "*This role is a POINTS ROLE, points requirement: " + datasettings(file="pcproles.txt",
                                                                                            method="get",line=pid) + "*\n"
                    for posid in alldatakeys("pcposroles.txt"):
                        if posid == str(whr.id):
                            posdata = datasettings(file="pcdroles.txt",method="get",line=posid)
                            posdata = posdata.split("-"); posnum = posdata[0]; posreq = posdata[1]
                            whrm += "*This role is a POSITIONAL ROLE, demon requirements: " + posreq + " Demons in Top " + \
                                    posnum + " range*\n"
                    await message.add_reaction(emoji=CHAR_SUCCESS)
                    await message.channel.send(whrm + whpl)
    if str(message.content).startswith("??pointschange"):
        pcv = True; pcp = None; pcpl = None
        if str(message.content).startswith("??pointschange "):
            pcm = str(message.content).replace("??pointschange ",""); pcm = paramquotationlist(pcm)
            if len(pcm) != 1:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid parameters!")
                pcv = False
            else:
                pcp = PLAYERDATA(pcm[0])
                if pcp is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid Pointercrate player!")
                    pcv = False
                else:
                    pcp = pcm[0]; pcpl = None
                    for uid in alldatakeys("pcdata.txt"):
                        if linkedplayer(uid) == pcm[0]: pcpl = getglobalmember(uid); break
                    if pcpl is None:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: Invalid Pointercrate player!")
                        pcv = False
                    else: pcpl = pcpl.name
        else: pcp = linkedplayer(str(message.author.id)); pcpl = message.author.name
        if pcv:
            if pcp is None:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: You are not linked to a Pointercrate Player!")
            else:
                pcnp = int(POINTSFORMULA(PLAYERDATA(pcp)))
                pcc = loggedpointschange(pcp)
                if pcc is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: No new Points Changes to display!")
                else:
                    if int(pcc['id']) == 1:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: No new Points Changes to display!")
                    else:
                        pcdif = int(pcc['dif']); pcop = int(pcc['old'])
                        if pcop == 0:
                            await message.add_reaction(emoji=CHAR_FAILED)
                            await message.channel.send("**Error**: No new Points Changes to display!")
                        else:
                            pcsym = "+-"
                            if pcdif > 0: pcsym = "+"
                            if pcdif < 0: pcsym = ""
                            await message.add_reaction(emoji=CHAR_SUCCESS)
                            await message.channel.send("**" + pcpl + "**: Your Points changed by **" +
                                            pcsym + str(pcdif) + "** *[Old: " + str(pcop) + ", New: " + str(pcnp) + "]*")
    if str(message.content).startswith("??howcloseto "):
        hcm = str(message.content).replace("??howcloseto ", ""); hcp = paramquotationlist(hcm)
        if hcp is None:
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: Invalid parameters!")
        else:
            if len(hcp) != 1:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid parameters!")
            else:
                hcr = getrole(message.guild, hcp[0])
                if hcr is None:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid role!")
                else:
                    hcpl = linkedplayer(str(message.author.id))
                    if hcpl is None:
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: You are not linked to a Pointercrate Player!")
                    else:
                        hcpd = PLAYERDATA(hcpl)
                        if hcpd is None:
                            await message.add_reaction(emoji=CHAR_FAILED)
                            await message.channel.send("**Error**: You are linked to an Invalid Player!")
                        else:
                            hcpp = int(POINTSFORMULA(hcpd))
                            hcm = ""
                            for pid in alldatakeys("pcproles.txt"):
                                if pid == str(hcr.id):
                                    prq = datasettings(file="pcproles.txt",method="get",line=pid)
                                    if prq is None: continue
                                    if prq == "$REMOVED$": continue
                                    prq = int(prq)
                                    hcm += "Requirement for POINTS ROLE **" + hcr.name + "**: *" + str(prq) + \
                                           "*, you have: *" + str(hcpp) + "*\n"
                                    prd = prq - hcpp
                                    if prd > 0: hcm += "You need **" + str(prd) + "** more points for this role!\n"
                                    else: hcm += "You already meet the requirements for this role!\n"
                            for did in alldatakeys("pcdroles.txt"):
                                if did == str(hcr.id):
                                    drq = datasettings(file="pcdroles.txt",method="get",line=did)
                                    if drq is None: continue
                                    if drq == "$REMOVED$": continue
                                    drq = drq.split(";"); drh = []
                                    for d in hcpd['beaten']:
                                        if d['name'] in drq: drh.append(d['name'])
                                    for d in hcpd['verified']:
                                        if d['name'] in drq: drh.append(d['name'])
                                    drs = []
                                    for dr in drq:
                                        df = False
                                        if dr in drh: df = True
                                        drs.append({'name':dr,'found':df})
                                    drsf = True; drff = []
                                    for dr in drs:
                                        if not dr['found']: drsf = False; drff.append(dr['name'])
                                    drqn = ""
                                    for d in drq: drqn += d + ", "
                                    drqn = drqn[:len(drqn) - 2]
                                    drhn = ""
                                    for d in drh: drhn += d + ", "
                                    drhn = drhn[:len(drhn) - 2]
                                    if drhn == "": drhn = "No Required Demons"
                                    hcm += "Requirement for DEMONS ROLE **" + hcr.name + "**: *" + drqn + \
                                           "*, you have: *" + drhn + "*\n"
                                    if not drsf:
                                        drfn = ""
                                        for d in drff: drfn += d + ", "
                                        drfn = drfn[:len(drfn) - 2]
                                        hcm += "You need **" + drfn + "** for this role!\n"
                                    else: hcm += "You already meet the requirements for this role!\n"
                            for posid in alldatakeys("pcposroles.txt"):
                                if posid == str(hcr.id):
                                    posrq = datasettings(file="pcposroles.txt",method="get",line=posid)
                                    if posrq is None: continue
                                    if posrq == "$REMOVED$": continue
                                    posrq = posrq.split("-"); posnum = int(posrq[0]); posbase = int(posrq[1])
                                    poshr = 0
                                    for d in hcpd['beaten']:
                                        if int(d['position']) <= posbase: poshr += 1
                                    for d in hcpd['verified']:
                                        if int(d['position']) <= posbase: poshr += 1
                                    hcm += "Requirement for POSITIONAL ROLE **" + hcr.name + "**: *POS: " + str(posbase) \
                                           + ", REQ: " + str(posnum) + "*, you have in that range: *" + str(poshr) + "*\n"
                                    if poshr < posnum:
                                        posd = posnum - poshr
                                        hcm += "You need **" + str(posd) + "** more Demons in that range for this role!\n"
                                    else: hcm += "You already meet the requirements for this role!\n"
                            if hcm == "":
                                await message.add_reaction(emoji=CHAR_FAILED)
                                await message.channel.send("**" + message.author.name + "**: This is not a Points/Demons/Positional role!")
                            else:
                                await message.add_reaction(emoji=CHAR_SUCCESS)
                                await message.channel.send("**" + message.author.name + "**: " + hcm)
    if str(message.content).startswith("??kchelp"):
        if membermoderator(message.author):
            hm1 = "**Killbot Circles Command List**\n*Coded by GunnerBones, Pointercrate system by Stadust*\n"
            hm1 += "*Note: All GLOBAL commands can only be used by Demons List Mods*\n"
            hm1 += "====================================\n"
            hm1 += "??setmoderator \"role name\" - [Admin][LOCAL]\n"
            hm1 += "Sets the role required to use this bot. If none set, defaults to checking if the user has an " \
                  "Admin role.\n"
            hm1 += "??addpointsrole \"role name\" number - [Mod][LOCAL]\n"
            hm1 += "Assigns a point value to a role\n"
            hm1 += "??removepointsrole \"role name\" number - [Mod][LOCAL]\n"
            hm1 += "his command destroys the entire universe and makes Beany the owner of the list team. " \
                  "Gee what did you think this command would do\n"
            hm1 += "??playerlink \"user name\" \"player id\" - [Pointercrate Mod][GLOBAL]\n"
            hm1 += "Links a Discord User to the global pointercrate players\n"
            hm1 += "??playerunlink \"user name\" \"player id\" - [Pointercrate Mod][GLOBAL]\n"
            hm1 += "do I really need to type this one out too\n"
            hm1 += "??adddemonsrole \"role name\" \"demon 1 name, demon 2 name\" - [Mod][LOCAL]\n"
            hm1 += "Assigns demon(s) required to beat/verify (I gotchu tech) for this role\n"
            hm1 += "??removedemonsrole \"role name\" - [Mod][LOCAL]\n"
            hm1 += "epic style\n"
            hm1 += "??addpositionalrole \"role name\" position_number_requirement number_of_demons - [Mod][LOCAL]\n"
            hm1 += "Assigns a certain Positional demon requirement for a role, and how many in that range required for " \
                  "it.\n"
            hm1 += "??removepositionalrole \"role name\" - [Mod][LOCAL]\n"
            hm1 += "yes\n"
            hm1 += "??refresh - [Mod][LOCAL]\n"
            hm1 += "Refreshes the bot to add demons/points roles to players or check up on timed bans\n"
            hm1 += "*Note: Refreshes are bot taxing and take around a couple minutes. Don't try to overload the bot " \
                  "with refreshes.*\n"
            hm2 = "====================================\n"
            hm2 += "??feedback \"demon position\" \"message\" - [Anyone][GLOBAL]\n"
            hm2 += "Sends a feedback back to Pointercrate HQ on what you think of this demon's position. You can only " \
                  "send 1 feedback, and only if you've beaten that demon.\n"
            hm2 += "??feedbackban \"user name\" - [Pointercrate Mod][GLOBAL]\n"
            hm2 += "Toggles Bans/Unbans obnoxious beanys and ozzys from sending stupid feedbacks\n"
            hm2 += "??tempban \"user name\" days - [Mod][LOCAL]\n"
            hm2 += "Bans someone for # of days. Alerts to #feedback when time is up and unbans them\n"
            hm2 += "??info - [Anyone][BOTH]\n"
            hm2 += "Gets information about your LOCAL demons/points roles and GLOBAL pointercrate player info\n"
            hm2 += "??setnewdemonschannel \"channel name\" - [Mod][LOCAL]\n"
            hm2 += "Sets a channel where UltimateGDBot sends new demons for this bot to remove anything that isn\'t a " \
                  "Hard Demon or harder.\n"
            hm2 += "??editpointsrole \"role name\" number - [Mod][LOCAL]\n"
            hm2 += "Changes a Points Role\'s points number.\n"
            hm2 += "??editdemonsrole \"demon name\" \"demon1 name, demon2 name\" - [Mod][LOCAL]\n"
            hm2 += "Changes a Demons Role\'s demons.\n"
            hm2 += "??editpositionalrole \"role name\" position_number_requirement number_of_demons - [Mod][LOCAL]\n"
            hm2 += "Changes a Positional Role\'s position requirement and/or number required.\n"
            hm2 += "??kcroles - [Anyone][LOCAL]\n"
            hm2 += "Lists all Points, Demons, and Positional roles for the server.\n"
            hm2 += "??whohas \"role name\" - [Anyone][LOCAL]\n"
            hm2 += "Lists all members with a role (and if it\'s a Killbot Circles role)\n"
            hm2 += "??pointschangs - [Anyone][GLOBAL]\n"
            hm2 += "Shows points increase/decrease after list changes\n"
            hm2 += "??howcloseto - [Anyone][GLOBAL]\n"
            hm2 += "Shows how close you are to a Points/Demons/Positional role\n"
            await message.author.send(hm1)
            time.sleep(1)
            await message.author.send(hm2)
            await message.add_reaction(emoji=CHAR_SUCCESS)
            await message.channel.send(
                "**" + message.author.name + "**: Command list sent to your private messages!")
        else:
            await message.add_reaction(emoji=CHAR_FAILED)
            await message.channel.send("**Error**: You are not a Moderator!")
    if message.author.id == 358598636436979713:
        if str(message.channel.id) in strtolist(datasettings(file="pcvars.txt",method="get",line="NEWDEMONSCHANNELS")):
            dmv = True; dme = {}
            try: dme = message.embeds[0].to_dict()
            except: dmv = False
            if dmv:
                for dmef in dme['fields']:
                    if "`u!level " in dmef['value']:
                        p1 = dmef['value'].index("`") + 1; p = dmef['value'][p1:]
                        p2 = p.index("`"); p = p[:p2]; p = p.replace("`", "")
                        p = p.replace("u!level ", "")
                        ldata = getanylevel(p)
                        if ldata != []:
                            ldifa = ["Hard Demon", "Insane Demon", "Extreme Demon"]
                            if ldata["Difficulty"] not in ldifa:
                                await message.channel.delete_messages([message])
                                print("[NDCD] Deleted " + ldata["Name"] + " because it is "
                                      + ldata['Difficulty'] + " [Guild:" + message.guild.name + "]")
    if message.channel.id == 266332849387339777 and message.author.id != 277391246035648512:
        if str(message.content).startswith("??accept") or str(message.content).startswith("??reject") \
                or str(message.content).startswith("??records add") or str(message.content).startswith("hey bot accept") \
                or str(message.content).startswith("hey bot reject"):
            NRREVIEWRECORD = message.author.name
    if str(message.content).startswith("??rejectmessage "):
        if inallowedguild(message.guild,message.author):
            rmm = str(message.content).replace("??rejectmessage ",""); rmp = paramquotationlist(rmm)
            if rmp is None:
                await message.add_reaction(emoji=CHAR_FAILED)
                await message.channel.send("**Error**: Invalid parameters!")
            else:
                if len(rmp) != 1:
                    await message.add_reaction(emoji=CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid parameters!")
                else:
                    rmrm = rmp[0]
                    if rmrm == "" or rmrm == " ":
                        await message.add_reaction(emoji=CHAR_FAILED)
                        await message.channel.send("**Error**: Invalid message!")
                    else:
                        global NRREVIEWRM
                        for r in NRREVIEWRM:
                            if r[1] == message.author: NRREVIEWRM.remove(r)
                        NRREVIEWRM.append([rmrm,message.author,message.channel])
                        await message.add_reaction(emoji=CHAR_SUCCESS)
                        await message.channel.send("**" + message.author.name + "**, rejection message set. React to "
                                "the submission with the " + CHAR_SENT + " reacted to send out the Rejection Message!")
    if message.author.id == 277391246035648512 and message.guild.id == 162862229065039872 and NRREVIEWRECORD:
        smrv = True; smre = None
        try: smre = message.embeds[0].to_dict()
        except: smrv = False
        if smrv:
            smr = None
            try: smr = smre['fields']
            except: smrv = False
            if smrv:
                smrh = smr[1]['value'].split("\n")
                smrh = smrh[1].replace("**ID**: ","")
                smf = False
                for h in alldatakeys("pcn.txt"):
                    if datasettings(file="pcn.txt",method="get",line=h) == smrh:
                        smf = True
                if not smf:
                    smf = None
                    for ph in alldatakeys("pcdata.txt"):
                        if datasettings(file="pcdata.txt", method="get", line=ph) == smrh:
                            smf = ph
                    if smf is not None:
                        hu = getglobalmember(smf)
                        if hu is not None:
                            smf = False
                            try:
                                smrd = smr[0]['value'].split("\n")
                                smrd = smrd[0].replace("**Name**: ","")
                                smrdes = smre['description'].split("\n")
                                smrp = smrdes[1].replace("**Progress**: ","")
                                smrs = smrdes[3].replace("**Status**: ","")
                            except: smf = True
                            if not smf:
                                srr = "*Notification from the Pointercrate Team*\n"
                                srr += hu.name + ", your record **" + smrp + "** on **" + smrd + "** has been " + smrs.upper()
                                srr += "!\n[" + smrs + " by " + NRREVIEWRECORD + "]"
                                srr += "\n*If you don\'t want to be notified, type ??getnotified*"
                                await hu.send(srr)
                                await message.add_reaction(CHAR_SENT)
                                NRREVIEWRECORD = None
                                if smrs.lower() == "rejected":
                                    await message.channel.send("*This player was notified their submission was Rejected. "
                                                           "To send them a Reason, type ??rejectmessage \"message\" "
                                                           "and then React with the " + CHAR_SENT + " on that Rejected "
                                                                                                    "Message.*")
    if str(message.content).startswith("??embeddebug "):
        if message.author.id == 172861416364179456:
            edm = str(message.content).replace("??embeddebug ","")
            for guild in client.guilds:
                for channel in guild.channels:
                    try:
                        async for m in channel.history(limit=40):
                            if str(m.id) == edm: print(m.embeds[0].to_dict())
                    except: pass
    if message.channel.id == 502229541549244437 and not message.author.bot:
        await message.add_reaction("👍"); await message.add_reaction("👎"); await message.add_reaction("❓")

client.run(SECRET)
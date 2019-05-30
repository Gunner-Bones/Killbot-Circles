import discord, asyncio, sys, os, urllib.request, json, math, random, ast, datetime, base64, time
from discord.ext import commands

def condensedatetime(d):
    dt = str(d).split(" "); return dt[0]

def datetimetoshort(d):
    dt = str(d).split(":")
    dt[dt.index(dt[2])] = dt[2].split(".")[0]
    dr = ""
    if dt[0] != "0": dr += dt[0] + " hours "
    if dt[1] != "00": dr += dt[1] + " minutes "
    if dt[2] != "00": dr += dt[2] + " seconds"
    return dr

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
            if ag[1] == 1: return membermoderator(m)
            return True
    return False

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

def getglobalmember(m,client):
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

def getguild(sid,client):
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

def samelists(l1,l2):
    if len(l1) == 0 or len(l2) == 0: return False
    if len(l1) == 1 and len(l2) == 1 and l1[0] == l2[0]: return True
    lv = 0; lu = []
    for d1 in l1:
        for d2 in l2:
            if d2 == d1 and d1 not in lu:
                lv += 1; lu.append(d1); break
    if lv == len(l1) and lv == len(l2): return True
    return False

def differencesinlists(l1,l2):
    if samelists(l1,l2): return []
    dil = []
    for d1 in l1:
        if d1 not in l2 and d1 not in dil: dil.append(d1)
    for d2 in l2:
        if d2 not in l1 and d2 not in dil: dil.append(d2)
    return dil

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

def datetostr(d):
    dt = str(d).split(" ")
    return dt[0]

def timetostr(d):
    dt = str(d).split(" "); dt = str(dt[1]).split(":")
    return dt[0] + ":" + dt[1]

def formattoday():
    return datetostr(datetime.datetime.now()) + " " + timetostr(datetime.datetime.now())

def strtodatetime(s):
    # Format: 2018-12-25, 14:30
    st = str(s).split("-")
    st[2] = st[2][:st[2].index(" ")]
    stm = str(s).split(":")
    stm[0] = stm[0][stm[0].index(" ") + 1:]
    return [datetime.date(year=int(st[0]),month=int(st[1]),day=int(st[2])),datetime.time(hour=int(stm[0]),
                                                                                         minute=int(stm[1]))]

def comparedates(d1,d2):
    if len(d1) != 2 or len(d2) != 2: return None
    if d1[0] > d2[0]: return d1
    elif d1[0] < d2[0]: return d2
    else:
        if d1[1] > d2[1]: return d1
        else: return d2

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

def cleardata(file):
    s = None
    try: s = open(file,"w")
    except: return
    s.truncate(); s.close()

def POINTSFORMULA(data):
    global DEMONSLIST
    if data is None: return None
    # requires data from PLAYERDATA()
    s = 0
    for d in data['records']:
        if int(d['demon']['position']) <= 100:
            s += (((d['progress'] / 100) ** 5) * (100 / (math.exp(0.03 * (d['demon']['position'] - 1)))))
    for d in data['verified']:
        if int(d['position']) <= 100:
            s += (((100 / 100) ** 5) * (100 / (math.exp(0.03 * (d['position'] - 1)))))
    return s

def PLAYERDATA(id):
    if id is None: return None
    url = "https://pointercrate.com/api/v1/players/" + str(id)
    rq = urllib.request.Request(url)
    try: rt = str(urllib.request.urlopen(rq).read())
    except: return None
    rt = rt[2:len(rt) - 1]; rt = rt.replace("\\n",""); rt = rt.replace("  ","")
    rj = json.loads(rt)
    return rj['data']

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

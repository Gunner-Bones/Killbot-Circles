import datetime
def datetostr(d):
    dt = str(d).split(" ")
    return dt[0]

def timetostr(d):
    dt = str(d).split(" "); dt = str(dt[1]).split(":")
    return dt[0] + ":" + dt[1]

def strtodatetime(s):
    # Format: 2018-12-25, 14:30
    st = str(s).split("-")
    st[2] = st[2][:st[2].index(" ")]
    stm = str(s).split(":")
    stm[0] = stm[0][stm[0].index(" ") + 1:]
    return [datetime.date(year=int(st[0]),month=int(st[1]),day=int(st[2])),datetime.time(hour=int(stm[0]),
                                                                                         minute=int(stm[1]))]

def formattoday():
    return datetostr(datetime.datetime.now()) + " " + timetostr(datetime.datetime.now())



print(formattoday())
print(strtodatetime(formattoday()))

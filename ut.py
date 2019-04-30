import unittest, discord, asyncio, sys, os, urllib.request, json, math, random, ast, datetime, base64, time
from discord.ext import commands
from common import *

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


class TestRefreshList(unittest.TestCase):

    def test_refresh(self):
        try: DEMONSLISTREFRESH()
        except: self.fail("DEMONSLISTREFRESH() failed")

class TestDatasettings(unittest.TestCase):

    def test_addvalue(self):
        av = str(random.randint(0,1000))
        self.assertIsNone(datasettings(file="utfile.txt",method="add",newkey="TESTADD",newvalue=av))
    def test_returnrealvalue(self):
        dv = datasettings(file="utfile.txt",method="get",line="TESTGET")
        self.assertEqual(dv,"testdata")
    def test_returnnullvalue(self):
        dv = datasettings(file="utfile.txt",method="get",line="NOTAKEY")
        self.assertIsNone(dv)
    def test_changevalue(self):
        self.assertIsNone(datasettings(file="utfile.txt",method="change",line="TESTCHANGE",newvalue="notdata"))
    def test_removevalue(self):
        self.assertIsNone(datasettings(file="utfile.txt",method="remove",line="TESTREMOVE"))
        datasettings(file="utfile.txt",method="add",newkey="TESTREMOVE",newvalue="test")



unittest.main()
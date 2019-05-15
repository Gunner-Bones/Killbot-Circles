import unittest, discord, asyncio, sys, os, urllib.request, json, math, random, ast, datetime, base64, time
from discord.ext import commands
from common import *

def linkedplayer(uid):
    uid = str(uid)
    if alldatakeys("pcdata.txt") != []:
        for lp in alldatakeys("pcdata.txt"):
            if lp == uid: return datasettings(file="pcdata.txt",method="get",line=lp)


class TestLinkedPlayer(unittest.TestCase):

    def test_valid_player(self):
        self.assertEqual(linkedplayer("172861416364179456"),"271")
    def test_invalid_player(self):
        self.assertIsNone(linkedplayer(" "))



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
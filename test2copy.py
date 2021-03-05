import requests
from concurrent.futures import ThreadPoolExecutor
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
import sys

playerlist = []
arr = []
url_list = []
players = []

API_KEY = "f57c9f4a-175b-430c-a261-d8c199abd927"


def urls():
    for i in range(len(players)):
        url_list.append(f"https://api.hypixel.net/player?key={API_KEY}&name={players[i]}")


def getinfo(url):
    prearr = []
    html = requests.get(url)
    prearr.append(html.json())
    prearr.append(url)
    arr.append(prearr)


def runner():
    with ThreadPoolExecutor(80) as executor:
        for url in url_list:
            executor.submit(getinfo, url)


def printer():
    global allplayersinfo
    global lobby
    global whostring
    allplayersinfo = []
    lobby = []
    for l in range(len(arr)):
        s = arr[l][0]
        player = s.get('player')
        if not player == None:
            displayname = player.get("displayname")
            stats = player.get('stats')
            bw = stats.get('Bedwars')
            ach = player.get('achievements')
            bwlevel = ach.get('bedwars_level')
            finalk = bw.get('final_kills_bedwars')
            if finalk == None:
                finalk = 0
            finald = bw.get('final_deaths_bedwars')
            if finald == None:
                finald = 1
            playerinfo = []
            playerinfo.append(displayname)
            playerinfo.append(bwlevel)
            playerinfo.append(round(finalk / finald, 2))
            allplayersinfo.append(playerinfo)
            lobby.append(displayname)
        else:
            nickedurl = arr[l][1]
            nickedname = nickedurl[(nickedurl.rfind("=") + 1):]
            playerinfo = [nickedname, 0, 0]
            allplayersinfo.append(playerinfo)
    whostring = i


a = 0

app = QApplication(sys.argv)

table = QTableWidget()
table.setGeometry(100, 100, 400, 500)
table.setWindowTitle("Bedwars overlay")
table.setRowCount(16)
table.setColumnCount(3)
labels = ["Name", "Level", "FKDR"]
table.setHorizontalHeaderLabels(labels)
while True:
    arr = []
    url_list = []
    players = []
    allplayersinfo = []
    file1 = r"C:\Users\123\AppData\Roaming\.minecraft\logs\blclient\minecraft\latest.log"
    with open(file1) as file:
        pretimearray = file.readlines(-1)
        timearray = list(map(str, pretimearray[-1].split()))
        timeinfo = timearray[0]
        jointimeh = int(timeinfo[1:3])
        jointimem = int(timeinfo[4:6])
        jointimes = int(timeinfo[7:9])
    while a == 0:
        with open(file1) as f:
            for i in f:
                if len(i) >= 15:
                    if i[1].isdecimal() and i[4].isdecimal():
                        if jointimeh < int(i[1:3]) or (jointimeh == int(i[1:3]) and jointimem < int(i[4:6])) or (jointimeh == int(i[1:3]) and jointimem == int(i[4:6]) and jointimes <= int(i[7:9])):
                            if "ONLINE" in i and "[CHAT]" in i:
                                players = list(map(str, i.split(",")))
                                player1 = players[0].split(":")
                                players.append(player1[-1])
                                del players[0]
                                for g in range(len(players)):
                                    b = players[g]
                                    players[g] = b[1:]
                                b = players[-2]
                                players[-2] = b[:len(b) - 1]
                                jointimeh = int(i[1:3])
                                jointimem = int(i[4:6])
                                jointimes = int(i[7:9])
        if playerlist != players:
            playerlist = players
            a = 1
        else:
            time.sleep(1)
    if len(players) != 0:
        urls()
        runner()
        printer()
        print(allplayersinfo)
        print(len(allplayersinfo))

    a = 0
    joinedlist = []
    players = []
    joinedstr = ""
    quitstr = ""
    while True:
        with open(file1) as f:
            if len(i) >= 15:
                if i[1:3].isdecimal() and i[4:6].isdecimal():
                    if not i == whostring:
                        if ((jointimeh < int(i[1:3]) or (jointimeh == int(i[1:3]) and jointimem < int(i[4:6])) or (jointimeh == int(i[1:3]) and jointimem == int(i[4:6]) and jointimes <= int(i[7:9])))) and ("ONLINE" in i or "?????????????????????????" in i):
                            break
            for i in f:
                if len(i) >= 15:
                    if i[1].isdecimal() and i[4].isdecimal():
                        if jointimeh < int(i[1:3]) or (jointimeh == int(i[1:3]) and jointimem < int(i[4:6])) or (jointimeh == int(i[1:3]) and jointimem == int(i[4:6]) and jointimes <= int(i[7:9])):
                            if "has joined" in i:
                                if not joinedstr == i:
                                    preplayers = list(map(str, i.split()))
                                    if not preplayers[4] in joinedlist:
                                        printchecker = allplayersinfo
                                        if not preplayers[4] in playerlist and not preplayers[4] in players and not preplayers[4] in joinedlist:
                                            players.append(preplayers[4])
                                            playercount = preplayers[-1]
                                            playercount = playercount.split('/')
                                            playernumber = playercount[0][1:]
                                            if len(playercount[1]) == 3:
                                                playercounter = playercount[1][0]
                                            else:
                                                playercounter = playercount[1][0:2]
                                            if playernumber == playercounter or int(playernumber) + 1 == int(playercounter):
                                                arr = []
                                                urls()
                                                runner()
                                                printer()
                                                players = []
                                        jointimeh = int(i[1:3])
                                        jointimem = int(i[4:6])
                                        jointimes = int(i[7:9])
                                        joinedlist.append(preplayers[4])
                                        if joinedstr != i:
                                            print(allplayersinfo)
                                            print(len(allplayersinfo))
                                        joinedstr = i
                            elif "has quit" in i:
                                preplayers = list(map(str, i.split()))
                                if preplayers[4] in lobby:
                                    players.append(preplayers[4])
                                    apiurl = f"https://api.hypixel.net/player?key={API_KEY}&name={players[0]}"
                                    if apiurl in url_list:
                                        del url_list[url_list.index(apiurl)]
                                    del allplayersinfo[lobby.index(preplayers[4])]
                                    del lobby[lobby.index(preplayers[4])]
                                    players = []
                                jointimeh = int(i[1:3])
                                jointimem = int(i[4:6])
                                jointimes = int(i[7:9])
                                if quitstr != i:
                                    print(allplayersinfo)
                                    print(len(allplayersinfo))
                                quitstr = i

    allplayersinfo = []
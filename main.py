import requests
from concurrent.futures import ThreadPoolExecutor
import time
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QTableWidgetItem, QVBoxLayout, QApplication, QLabel, QWidget, QTableWidget
import sys
from threading import Thread


class Communicate(QObject):
    update_table = pyqtSignal()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.verticalLayout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.verticalLayout.addWidget(self.table)

        self.setWindowTitle("Bedwars overlay")
        self.show()
        print('UI init completed')

        self.playerlist = []
        self.arr = []
        self.url_list = []
        self.players = []
        self.API_KEY = "f57c9f4a-175b-430c-a261-d8c199abd927"
        self.a = 0
        self.whostring = ''
        self.allplayersinfo = []
        self.lobby = []

        self.signal = Communicate()
        self.signal.update_table.connect(self.fill_table)

        th1 = Thread(target=self.main_cycle)
        th1.start()

    def urls(self):
        for i in self.players:
            i = i.strip()
            self.url_list.append(f"https://api.hypixel.net/player?key={self.API_KEY}&name={i}")
        print(self.url_list)
        print('eto urls')

    def getinfo(self, url):
        prearr = []
        html = requests.get(url)
        prearr.append(html.json())
        prearr.append(url)
        self.arr.append(prearr)
        print('eto getinfo')

    def runner(self):
        with ThreadPoolExecutor(80) as executor:
            for url in self.url_list:
                executor.submit(self.getinfo, url)
        print('eto runer')

    def printer(self):
        self.allplayersinfo = []
        self.lobby = []
        for l in range(len(self.arr)):
            s = self.arr[l][0]
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
                self.allplayersinfo.append(playerinfo)
            else:
                nickedurl = self.arr[l][1]
                nickedname = nickedurl[(nickedurl.rfind("=") + 1):]
                playerinfo = [nickedname, 'nick', 0]
                self.allplayersinfo.append(playerinfo)
        print('eto printer')

    def main_cycle(self):
        while True:
            self.arr = []
            self.url_list = []
            self.players = []
            self.allplayersinfo = []
            self.lobby = []
            file1 = r"C:\Users\123\.lunarclient\offline\1.8\logs\latest.log"
            with open(file1) as file:
                pretimearray = file.readlines(-1)
                timearray = list(map(str, pretimearray[-1].split()))
                timeinfo = timearray[0]
                jointimeh = int(timeinfo[1:3])
                jointimem = int(timeinfo[4:6])
                jointimes = int(timeinfo[7:9])
            while self.a == 0:
                with open(file1) as f:
                    for i in f:
                        if len(i) >= 15:
                            if i[1].isdecimal() and i[4].isdecimal():
                                if jointimeh < int(i[1:3]) or (jointimeh == int(i[1:3]) and jointimem < int(i[4:6])) or (jointimeh == int(i[1:3]) and jointimem == int(i[4:6]) and jointimes <= int(i[7:9])):
                                    if "ONLINE" in i and "[CHAT]" in i:
                                        self.players = list(map(str, i.split(", ")))
                                        player1 = self.players[0].split(": ")
                                        self.players.append(player1[-1])
                                        del self.players[0]
                                        jointimeh = int(i[1:3])
                                        jointimem = int(i[4:6])
                                        jointimes = int(i[7:9])
                                        self.whostring = i
                                        print(self.whostring)
                if self.playerlist != self.players:
                    self.playerlist = self.players
                    self.a = 1
                else:
                    time.sleep(0.01)
            if len(self.players) != 0:
                self.urls()
                self.runner()
                self.printer()
                self.signal.update_table.emit()
                # print(self.allplayersinfo)
                # print(len(self.allplayersinfo))

            self.a = 0
            joinedlist = []
            joinedstr = ""
            quitstr = ""
            label = True
            while True:
                with open(file1) as f:
                    if label == False:
                        break
                    for i in f:
                        if len(i) >= 15:
                            if i[1:3].isdecimal() and i[4:6].isdecimal():
                                if "ONLINE" in i or "?????????????????????????" in i:
                                    if not i == self.whostring and (jointimeh < int(i[1:3]) or (jointimeh == int(i[1:3]) and jointimem < int(i[4:6])) or (jointimeh == int(i[1:3]) and jointimem == int(i[4:6]) and jointimes <= int(i[7:9]))):
                                        print('чел где брек')
                                        label = False
                                        break
                        if len(i) >= 15:
                            if i[1].isdecimal() and i[4].isdecimal():
                                if jointimeh < int(i[1:3]) or (jointimeh == int(i[1:3]) and jointimem < int(i[4:6])) or (jointimeh == int(i[1:3]) and jointimem == int(i[4:6]) and jointimes <= int(i[7:9])):
                                    if "has joined" in i:
                                        if not joinedstr == i:
                                            preplayers = list(map(str, i.split()))
                                            if not preplayers[4] in joinedlist:
                                                if not preplayers[4] in self.playerlist and not preplayers[4] in self.players and not preplayers[4] in joinedlist:
                                                    self.players.append(preplayers[4])
                                                    playercount = preplayers[-1]
                                                    playercount = playercount.split('/')
                                                    playernumber = playercount[0][1:]
                                                    if len(playercount[1]) == 3:
                                                        playercounter = playercount[1][0]
                                                    else:
                                                        playercounter = playercount[1][0:2]
                                                    if playernumber == playercounter or int(playernumber) + 1 == int(playercounter):
                                                        self.arr = []
                                                        self.url_list = []
                                                        self.urls()
                                                        self.runner()
                                                        self.printer()
                                                jointimeh = int(i[1:3])
                                                jointimem = int(i[4:6])
                                                jointimes = int(i[7:9])
                                                joinedlist.append(preplayers[4])
                                                self.signal.update_table.emit()
                                                    # print(self.allplayersinfo)
                                                    # print(len(self.allplayersinfo))
                                                joinedstr = i
                                    elif "has quit" in i:
                                        preplayers = list(map(str, i.split()))
                                        self.lobby = []
                                        for h in self.allplayersinfo:
                                            self.lobby.append(h[0])
                                        if preplayers[4] in self.lobby:
                                            playername = preplayers[4]

                                            apiurl = f"https://api.hypixel.net/player?key={self.API_KEY}&name={playername}"
                                            if apiurl in self.url_list:
                                                del self.url_list[self.url_list.index(apiurl)]
                                            del self.allplayersinfo[self.lobby.index(playername)]
                                            del self.lobby[self.lobby.index(playername)]
                                            del self.players[self.players.index(playername)]
                                        jointimeh = int(i[1:3])
                                        jointimem = int(i[4:6])
                                        jointimes = int(i[7:9])
                                        if quitstr != i:
                                            self.signal.update_table.emit()
                                            # print(self.allplayersinfo)
                                            # print(len(self.allplayersinfo))
                                        quitstr = i
        print('eto main')

    def fill_table(self):
        array = self.allplayersinfo[:]
        self.table.setRowCount(0)
        self.table.setRowCount(len(array))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Level", "FKDR"])

        array.sort(key=lambda x: x[2], reverse=True)
        for f in range(3):
            for i in range(len(array)):
                self.table.setItem(
                    i, f, QTableWidgetItem(str(array[i][f])))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.update()
        print('eto fill table')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    # window.show()
    sys.exit(app.exec_())

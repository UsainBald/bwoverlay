import requests
from concurrent.futures import ThreadPoolExecutor
import time
from PyQt5.QtWidgets import QTableWidgetItem, QVBoxLayout, QApplication, QLabel, QWidget, QTableWidget, QSizePolicy
import sys


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

        self.main_cycle()
        # self.test()

    def urls(self):
        for i in range(len(self.players)):
            self.url_list.append(
                f"https://api.hypixel.net/player?key={self.API_KEY}&name={self.players[i]}")

    def getinfo(self, url):
        prearr = []
        html = requests.get(url)
        prearr.append(html.json())
        prearr.append(url)
        self.arr.append(prearr)

    def runner(self):
        with ThreadPoolExecutor(80) as executor:
            for url in self.url_list:
                executor.submit(self.getinfo, url)

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
                self.lobby.append(displayname)
            else:
                nickedurl = self.arr[l][1]
                nickedname = nickedurl[(nickedurl.rfind("=") + 1):]
                playerinfo = [nickedname, 0, 0]
                self.allplayersinfo.append(playerinfo)
        self.whostring = i  # тут баг

    def main_cycle(self):
        while True:
            self.arr = []
            self.url_list = []
            self.players = []
            self.allplayersinfo = []
            file1 = r"C:\Users\123\AppData\Roaming\.minecraft\logs\blclient\minecraft\latest.log"
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
                                        self.players = list(
                                            map(str, i.split(",")))
                                        player1 = self.players[0].split(":")
                                        self.players.append(player1[-1])
                                        del self.players[0]
                                        for g in range(len(self.players)):
                                            b = self.players[g]
                                            self.players[g] = b[1:]
                                        b = self.players[-2]
                                        self.players[-2] = b[:len(b) - 1]
                                        jointimeh = int(i[1:3])
                                        jointimem = int(i[4:6])
                                        jointimes = int(i[7:9])
                if self.playerlist != self.players:
                    self.playerlist = self.players
                    self.a = 1
                else:
                    time.sleep(1)
            if len(self.players) != 0:
                self.urls()
                self.runner()
                self.printer()
                self.fill_table(self.allplayersinfo)
                # print(self.allplayersinfo)
                # print(len(self.allplayersinfo))

            self.a = 0
            joinedlist = []
            self.players = []
            joinedstr = ""
            quitstr = ""
            while True:
                with open(file1) as f:
                    if len(i) >= 15:
                        if i[1:3].isdecimal() and i[4:6].isdecimal():
                            if not i == self.whostring:
                                if ((jointimeh < int(i[1:3]) or (jointimeh == int(i[1:3]) and jointimem < int(i[4:6])) or (jointimeh == int(i[1:3]) and jointimem == int(i[4:6]) and jointimes <= int(i[7:9])))) and ("ONLINE" in i or "?????????????????????????" in i):
                                    break
                    for i in f:
                        if len(i) >= 15:
                            if i[1].isdecimal() and i[4].isdecimal():
                                if jointimeh < int(i[1:3]) or (jointimeh == int(i[1:3]) and jointimem < int(i[4:6])) or (jointimeh == int(i[1:3]) and jointimem == int(i[4:6]) and jointimes <= int(i[7:9])):
                                    if "has joined" in i:
                                        if not joinedstr == i:
                                            preplayers = list(
                                                map(str, i.split()))
                                            if not preplayers[4] in joinedlist:
                                                printchecker = self.allplayersinfo
                                                if not preplayers[4] in self.playerlist and not preplayers[4] in self.players and not preplayers[4] in joinedlist:
                                                    self.players.append(
                                                        preplayers[4])
                                                    playercount = preplayers[-1]
                                                    playercount = playercount.split(
                                                        '/')
                                                    playernumber = playercount[0][1:]
                                                    if len(playercount[1]) == 3:
                                                        playercounter = playercount[1][0]
                                                    else:
                                                        playercounter = playercount[1][0:2]
                                                    if playernumber == playercounter or int(playernumber) + 1 == int(playercounter):
                                                        self.arr = []
                                                        self.urls()
                                                        self.runner()
                                                        self.printer()
                                                        self.players = []
                                                jointimeh = int(i[1:3])
                                                jointimem = int(i[4:6])
                                                jointimes = int(i[7:9])
                                                joinedlist.append(
                                                    preplayers[4])
                                                if joinedstr != i:
                                                    self.fill_table(
                                                        self.allplayersinfo)
                                                    # print(self.allplayersinfo)
                                                    # print(
                                                    #     len(self.allplayersinfo))
                                                joinedstr = i
                                    elif "has quit" in i:
                                        preplayers = list(
                                            map(str, i.split()))
                                        if preplayers[4] in self.lobby:
                                            self.players.append(
                                                preplayers[4])
                                            apiurl = f"https://api.hypixel.net/player?key={self.API_KEY}&name={self.players[0]}"
                                            if apiurl in self.url_list:
                                                del self.url_list[self.url_list.index(
                                                    apiurl)]
                                            del self.allplayersinfo[self.lobby.index(
                                                preplayers[4])]
                                            del self.lobby[self.lobby.index(
                                                preplayers[4])]
                                            self.players = []
                                        jointimeh = int(i[1:3])
                                        jointimem = int(i[4:6])
                                        jointimes = int(i[7:9])
                                        if quitstr != i:
                                            self.fill_table(
                                                self.allplayersinfo)
                                            # print(self.allplayersinfo)
                                            # print(len(self.allplayersinfo))
                                        quitstr = i
            self.allplayersinfo = []

    #######
    #######
    #######

    def test(self):
        input('start 1: ')
        self.array = [['Eglyo', 20, 0.35], ['6692', 31, 0.36], [
            'edx_7', 18, 0.26], ['zaradog', 39, 0.44], ['Usain_Bald', 82, 8.07]]
        self.fill_table(self.array)
        print('1 done')

        input('start 2: ')
        self.array = [['Z4maaaaaaaaaaaaaaan', 234, 1.51], ['IssaRam', 61, 1.98], ['NotSxrry', 21, 2.15], ['Szczypson8985', 18, 0.21], ['ZXEMISKY12', 1, 1.0], ['BenGFox', 9, 0.66], ['IITMM', 23, 0.49], [
            'lazyshadow', 0, 0], ['EdvinTheBot', 70, 0.41], ['Genexis', 252, 0.95], ['IReallyLike_Bees', 14, 0.31], ['Usain_Bald', 82, 8.07], ['renoi', 72, 1.27], ['Adital', 21, 0.64]]
        self.fill_table(self.array)
        print('2 done')

    def fill_table(self, arr):
        array = arr[:]
        self.table.setRowCount(0)
        self.table.setRowCount(len(array))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Level", "FKDR"])

        array.sort(key=lambda x: x[2], reverse=True)
        for f in range(3):
            for i in range(len(array)):
                self.table.setItem(
                    i, f, QTableWidgetItem(str(array[i][f])))
        self.table.update()
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    # self.array = [['Eglyo', 20, 0.35], ['6692', 31, 0.36], ['edx_7', 18, 0.26],
    #          ['zaradog', 39, 0.44], ['Usain_Bald', 82, 8.07]]

    # table.show()
    # app.closeAllWindows()
    # time.sleep(1)
    # self.array = [['Z4man', 234, 1.51], ['IssaRam', 61, 1.98], ['NotSxrry', 21, 2.15], ['Szczypson8985', 18, 0.21], ['ZXEMISKY12', 1, 1.0], ['BenGFox', 9, 0.66], ['IITMM', 23, 0.49], [
    #     'lazyshadow', 0, 0], ['EdvinTheBot', 70, 0.41], ['Genexis', 252, 0.95], ['IReallyLike_Bees', 14, 0.31], ['Usain_Bald', 82, 8.07], ['renoi', 72, 1.27], ['Adital', 21, 0.64]]
    # self.array.sort(key=lambdself.ax: x[2], reverse=True)
    # app.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    # window.show()
    sys.exit(app.exec_())

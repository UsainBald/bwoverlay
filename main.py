import requests
from concurrent.futures import ThreadPoolExecutor
import time
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QTableWidgetItem, QVBoxLayout, QApplication, QLabel, QWidget, QTableWidget
import sys
from threading import Thread
import os


class Communicate(QObject):
    update_table = pyqtSignal()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.verticalLayout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.verticalLayout.addWidget(self.table)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Bedwars overlay")
        self.show()
        print('UI init completed')

        self.filename = "C:/Users/123/.lunarclient/offline/1.8/logs/latest.log"
        # self.filename = "D:/Users/DEN/Pictures/del4/asa/bwoverlay/a.log"
        self.logfile_lastchanged = 0  # время последнего изменения файла логов
        self.API_KEY = "f57c9f4a-175b-430c-a261-d8c199abd927"
        self.players = {}
        self.players_raw = []  # keep clean
        self.log_endpos = self.log_endpos_calibrate()  # последняя позиция чтения логов
        self.log_islastline = False  # уверены ли мы, что прочитана последняя линия
        # self.lobby_process = True  # смотрим, находимся мы в лобби или в игре

        self.signal = Communicate()
        self.signal.update_table.connect(self.fill_table)
        th1 = Thread(target=self.main)
        th1.start()

    def main(self):
        while True:
            time.sleep(0.0001)
            line = self.read_logs()
            changed = True
            if line == None:
                continue

            if "ONLINE" in line and "[CHAT]" in line:
                self.new_game(line)
            elif "has joined" in line:
                self.player_joined(line)
            elif "has quit" in line:
                self.player_quit(line)
            elif "?????????????????????????????????????" in line:
                self.players = {}
                self.players_raw = []
                # self.signal.update_table.emit()
                # changed = False
                # # self.showMinimized()
            else:
                changed = False
            if changed:
                self.signal.update_table.emit()

    def read_logs(self):
        curtime = os.stat(self.filename).st_mtime
        if curtime == self.logfile_lastchanged and self.log_islastline:
            return None
        elif not self.log_islastline:
            try:
                f = open(self.filename, mode='r')
                f.seek(self.log_endpos)
                c = f.read(1)
                f.close()
            except Exception:
                self.log_islastline = True
                return None
        else:
            self.logfile_lastchanged = curtime
        # time.sleep(0.01) - нужно посмотреть, нужна ли эта строчка
        try:
            f = open(self.filename, mode='r')
            f.seek(self.log_endpos)
            line = ''
            try:
                while True:
                    c = f.read(1)
                    line += c
                    if c == '\n':
                        break
            except Exception:
                print("####  ERROR: FILE LAST LINE NOT ENDS WITH \\n  ####")
                print(line, '\n')
                return None

            print('|', line.strip('\r\n'), '|', sep='')
            f.close()

            if line[-1] != '\n':
                print("####  ERROR: FILE LAST LINE NOT ENDS WITH \\n  ####")
                print(line, '\n')
                return None

            self.log_endpos += len(line) + 1
            self.log_islastline = False
            return line.strip('\n')

        except Exception as e:
            print('####  LOG READING ERROR  ####')
            print(e)
            # raise SystemExit
            # self.log_endpos = self.log_endpos_calibrate()
            # return ''

    def log_endpos_calibrate(self):
        f = open(self.filename, mode="r")
        r = f.read()
        t = f.tell()
        f.close()
        self.logfile_lastchanged = os.stat(self.filename).st_mtime
        return t

    def new_game(self, line):
        # 48 - длина   "[20:25:37] [Client thread/INFO]: [CHAT] ONLINE: "
        a = line[48:].split(', ')
        current = []
        for i in a:
            if i not in self.players:
                current.append(a)
        self.player_submit(current)

    def player_joined(self, line):
        self.player_submit([line.split()[4]])

    def player_quit(self, line):
        try:
            del self.players[line.split()[4]]
        except Exception:
            print("####  ERROR: QUITING PLAYER DOES NOT EXISTS  ####")
            pass  # todo: сделать обработку ошибки

    def player_submit(self, arr):
        self.multithreading_request(arr)
        self.players_rawdata_process()
        self.players_raw = []

    def multithreading_request(self, arr):
        url_list = []
        for i in arr:
            url_list.append(
                f"https://api.hypixel.net/player?key={self.API_KEY}&name={i.strip()}")
        with ThreadPoolExecutor(16) as executor:
            for url in url_list:
                executor.submit(self.get_raw_data, url)
        # for url in url_list:
        #     thread = Thread(target=self.get_raw_data, args=(url,))
        #     thread.start()

    def get_raw_data(self, url):
        self.players_raw.append(requests.get(url).json())
        # time.sleep(0.01)

    def players_rawdata_process(self):
        for i in self.players_raw:
            s = i
            player = s.get('player')
            if player != None:
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
                self.players[displayname] = playerinfo
            else:
                print('####  ERROR: NICKED PLAYER DETECTED  ####')
            # todo: nicked players process
            # else:
            #     nickedurl = i[1]
            #     nickedname = nickedurl[(nickedurl.rfind("=") + 1):]
            #     playerinfo = [nickedname, 0, 0]
            #     self.players[nickedname] = playerinfo

    def fill_table(self):
        array = []
        for i in self.players:
            array.append(self.players[i][:])

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
        # if self.isMinimized():
        #     self.showNormal()
        print('fill table')

    ####################################
    ####################################
    ########      OLDS      ############
    ####################################
    ####################################

    def urls(self):
        for i in range(len(self.players)):
            self.url_list.append(
                f"https://api.hypixel.net/player?key={self.API_KEY}&name={self.players[i]}")
        print('urls')

    def getinfo(self, url):
        prearr = []
        html = requests.get(url)
        prearr.append(html.json())
        prearr.append(url)
        self.arr.append(prearr)
        print('getinfo')

    def runner(self):
        with ThreadPoolExecutor(80) as executor:
            for url in self.url_list:
                executor.submit(self.getinfo, url)
        print('runer')

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
        print('printer')

    def main_cycle(self):
        wholist = []
        while True:
            self.arr = []
            self.url_list = []
            self.players = []
            self.allplayersinfo = []
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
                                        self.players = list(
                                            map(str, i.split(", ")))
                                        player1 = self.players[0].split(": ")
                                        self.players.append(player1[-1])
                                        del self.players[0]
                                        jointimeh = int(i[1:3])
                                        jointimem = int(i[4:6])
                                        jointimes = int(i[7:9])
                                        wholist.append(i)
                if self.playerlist != self.players:
                    self.playerlist = self.players
                    self.a = 1
                else:
                    time.sleep(1)
            if len(self.players) != 0:
                self.urls()
                self.runner()
                self.printer()
                self.signal.update_table.emit()
                # print(self.allplayersinfo)
                # print(len(self.allplayersinfo))

            self.a = 0
            joinedlist = []
            self.players = []
            joinedstr = ""
            quitstr = ""
            flag = True
            while True:
                if flag == False:
                    break
                with open(file1) as f:
                    for i in f:
                        if len(i) >= 15:
                            if i[1:3].isdecimal() and i[4:6].isdecimal():
                                if not i in wholist:
                                    if "ONLINE" in i or "?????????????????????????" in i:
                                        flag = False

                        if len(i) >= 15:
                            if i[1].isdecimal() and i[4].isdecimal():
                                if jointimeh < int(i[1:3]) or (jointimeh == int(i[1:3]) and jointimem < int(i[4:6])) or (jointimeh == int(i[1:3]) and jointimem == int(i[4:6]) and jointimes <= int(i[7:9])):
                                    if "has joined" in i:
                                        if not joinedstr == i:
                                            preplayers = list(
                                                map(str, i.split()))
                                            if not preplayers[4] in joinedlist:
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
                                                self.signal.update_table.emit()
                                                # print(self.allplayersinfo)
                                                # print(
                                                #     len(self.allplayersinfo))
                                                joinedstr = i
                                    elif "has quit" in i:
                                        preplayers = list(map(str, i.split()))
                                        if preplayers[4] in self.lobby:
                                            self.players.append(preplayers[4])
                                            apiurl = f"https://api.hypixel.net/player?key={self.API_KEY}&name={self.players[0]}"
                                            if apiurl in self.url_list:
                                                del self.url_list[self.url_list.index(
                                                    apiurl)]
                                            if preplayers[4] in self.allplayersinfo:
                                                del self.allplayersinfo[self.allplayersinfo.index(
                                                    preplayers[4])]
                                            del self.lobby[self.lobby.index(
                                                preplayers[4])]
                                            self.players = []
                                        jointimeh = int(i[1:3])
                                        jointimem = int(i[4:6])
                                        jointimes = int(i[7:9])
                                        if quitstr != i:
                                            self.signal.update_table.emit()
                                            # print(self.allplayersinfo)
                                            # print(len(self.allplayersinfo))
                                        quitstr = i
        print('main')
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
        self.array = [['Z4maaaaaaaaaaaaaaan', 234, 1.51], ['IssaRam', 61, 1.98], ['NotSxrry', 21, 2.15],
                      ['Szczypson8985', 18, 0.21], ['ZXEMISKY12', 1, 1.0], ['BenGFox', 9, 0.66], ['IITMM', 23, 0.49], [
                          'lazyshadow', 0, 0], ['EdvinTheBot', 70, 0.41], ['Genexis', 252, 0.95],
                      ['IReallyLike_Bees', 14, 0.31], [
                          'Usain_Bald', 82, 8.07], ['renoi', 72, 1.27],
                      ['Adital', 21, 0.64]]
        self.fill_table(self.array)
        print('2 done')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    # window.show()
    sys.exit(app.exec_())

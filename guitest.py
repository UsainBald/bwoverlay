import requests
from concurrent.futures import ThreadPoolExecutor
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
import sys

array = [['Eglyo', 20, 0.35], ['6692', 31, 0.36], ['edx_7', 18, 0.26], ['zaradog', 39, 0.44], ['Usain_Bald', 82, 8.07]]
array.sort(key = lambda x: x[2], reverse=True)
app = QApplication(sys.argv)

table = QTableWidget()
table.setGeometry(100, 100, 400, 500)
table.setWindowTitle("Bedwars overlay")
table.setRowCount(16)
table.setColumnCount(3)
labels = ["Name", "Level", "FKDR"]
table.setHorizontalHeaderLabels(labels)
for f in range(3):
    for i in range(len(array)):
        table.setItem(i, f, QTableWidgetItem(str(array[i][f])))
table.show()
app.closeAllWindows()
time.sleep(1)
array = [['Z4man', 234, 1.51], ['IssaRam', 61, 1.98], ['NotSxrry', 21, 2.15], ['Szczypson8985', 18, 0.21], ['ZXEMISKY12', 1, 1.0], ['BenGFox', 9, 0.66], ['IITMM', 23, 0.49], ['lazyshadow', 0, 0], ['EdvinTheBot', 70, 0.41], ['Genexis', 252, 0.95], ['IReallyLike_Bees', 14, 0.31], ['Usain_Bald', 82, 8.07], ['renoi', 72, 1.27], ['Adital', 21, 0.64]]
array.sort(key = lambda x: x[2], reverse=True)
for f in range(3):
    for i in range(len(array)):
        table.setItem(i, f, QTableWidgetItem(str(array[i][f])))
app.exec_()
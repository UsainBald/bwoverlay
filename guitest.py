import requests
from concurrent.futures import ThreadPoolExecutor
import time
from PyQt5.QtWidgets import QTableWidgetItem, QVBoxLayout, QApplication, QLabel, QWidget, QTableWidget, QSizePolicy
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.show()
        self.verticalLayout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.verticalLayout.addWidget(self.table)

        self.setWindowTitle("Bedwars overlay")

        self.test()

    def test(self):
        self.array = [['Eglyo', 20, 0.35], ['6692', 31, 0.36], [
            'edx_7', 18, 0.26], ['zaradog', 39, 0.44], ['Usain_Bald', 82, 8.07]]
        time.sleep(500)
        self.fill_table()
        self.array = [['Z4man', 234, 1.51], ['IssaRam', 61, 1.98], ['NotSxrry', 21, 2.15], ['Szczypson8985', 18, 0.21], ['ZXEMISKY12', 1, 1.0], ['BenGFox', 9, 0.66], ['IITMM', 23, 0.49], [
            'lazyshadow', 0, 0], ['EdvinTheBot', 70, 0.41], ['Genexis', 252, 0.95], ['IReallyLike_Bees', 14, 0.31], ['Usain_Bald', 82, 8.07], ['renoi', 72, 1.27], ['Adital', 21, 0.64]]
        time.sleep(500)
        self.fill_table()
        self.show()
        return self.test

        # sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(
        #     self.table.sizePolicy().hasHeightForWidth())
        # self.table.setSizePolicy(sizePolicy)

    def fill_table(self):

        self.table.clear()
        self.table.setRowCount(len(self.array))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Level", "FKDR"])

        self.array.sort(key=lambda x: x[2], reverse=True)
        for f in range(3):
            for i in range(len(self.array)):
                self.table.setItem(
                    i, f, QTableWidgetItem(str(self.array[i][f])))
        # self.table.resizeColumnsToContents()
        # self.table.resizeRowsToContents()

    # array = [['Eglyo', 20, 0.35], ['6692', 31, 0.36], ['edx_7', 18, 0.26],
    #          ['zaradog', 39, 0.44], ['Usain_Bald', 82, 8.07]]

    # table.show()
    # app.closeAllWindows()
    # time.sleep(1)
    # array = [['Z4man', 234, 1.51], ['IssaRam', 61, 1.98], ['NotSxrry', 21, 2.15], ['Szczypson8985', 18, 0.21], ['ZXEMISKY12', 1, 1.0], ['BenGFox', 9, 0.66], ['IITMM', 23, 0.49], [
    #     'lazyshadow', 0, 0], ['EdvinTheBot', 70, 0.41], ['Genexis', 252, 0.95], ['IReallyLike_Bees', 14, 0.31], ['Usain_Bald', 82, 8.07], ['renoi', 72, 1.27], ['Adital', 21, 0.64]]
    # array.sort(key=lambda x: x[2], reverse=True)
    # app.exec_()


if __name__ == '__main__':
    array = []
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())

import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Coffee')
        self.tab.cellClicked.connect(self.pokazknig)
        self.agg()

    def pokazknig(self):
        pass

    def closeEvent(self, event):
        self.connection.close()

    def agg(self):
        self.connection = sqlite3.connect("coffee.sqlite")
        self.cur = self.connection.cursor()
        res = self.cur.execute("""SELECT Sortes_name, Stepen_obzharki, Vid, Opisanie_vkusa, Price, Volume from cofe""").fetchall()
        vids = self.cur.execute("""SELECT ID, Vid from vid""").fetchall()
        obzh = self.cur.execute("""SELECT ID, Obzharka from obzharka""").fetchall()
        res = list(res)
        for i in range(len(res)):
            res[i] = list(res[i])
            for j in vids:
                if j[0] == res[i][2]:
                    res[i][2] = j[1]
                    break
            for j in obzh:
                if j[0] == res[i][1]:
                    res[i][1] = j[1]
                    break
        name = ['Название сорта', 'Степень обжарки', 'Молотый/В зернах', 'Описание вкуса', 'Цена', 'Объем упаковки']
        self.tab.setColumnCount(len(name))
        for i in range(len(name)):
            item = QTableWidgetItem()
            item.setText(name[i])
            self.tab.setHorizontalHeaderItem(i, item)
        self.tab.setRowCount(0)
        for i, row in enumerate(res):
            self.tab.setRowCount(self.tab.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tab.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tab.resizeColumnToContents(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mn = Main()
    mn.show()
    sys.exit(app.exec())

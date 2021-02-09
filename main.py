import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from main_ui import Ui_MainWindow
from addEditCoffeeForm import Ui_smWin


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Coffee')
        self.tab.cellClicked.connect(self.iz_cof)
        self.add_cofe.clicked.connect(self.ad_cof)
        self.agg()

    def iz_cof(self, i, j):
        global izm
        res = self.cur.execute("""SELECT ID, Sortes_name, Stepen_obzharki, Vid, Opisanie_vkusa, Price, Volume from cofe
        WHERE (ID = ?)""", (self.tab.item(i, 0).text(), )).fetchall()[0]
        ad.idd.setText(str(res[0]))
        ad.name.setText(res[1])
        ad.obz.setCurrentIndex(res[2] - 1)
        ad.molot.setCurrentIndex(res[3] - 1)
        ad.ob.setValue(res[6])
        ad.price.setValue(res[5])
        ad.vkus.setText(res[4])
        izm = True
        ad.show()

    def ad_cof(self):
        res = self.cur.execute("""SELECT ID from cofe""").fetchall()
        for i in range(len(res)):
            res[i] = res[i][0]
        ad.idd.setText(str(max(res) + 1))
        ad.show()
        self.agg()

    def closeEvent(self, event):
        self.connection.close()

    def agg(self):
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.cur = self.connection.cursor()
        res = self.cur.execute("""SELECT ID, Sortes_name, Stepen_obzharki, Vid, Opisanie_vkusa, Price, Volume from cofe""").fetchall()
        vids = self.cur.execute("""SELECT ID, Vid from vid""").fetchall()
        obzh = self.cur.execute("""SELECT ID, Obzharka from obzharka""").fetchall()
        res = list(res)
        for i in range(len(res)):
            res[i] = list(res[i])
            for j in vids:
                if j[0] == res[i][3]:
                    res[i][3] = j[1]
                    break
            for j in obzh:
                if j[0] == res[i][2]:
                    res[i][2] = j[1]
                    break
        name = ['id', 'Название сорта', 'Степень обжарки', 'Молотый/В зернах', 'Описание вкуса', 'Цена', 'Объем упаковки']
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


class Add_cofe(QMainWindow, Ui_smWin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Add coffee')
        self.save.clicked.connect(self.sav)

    def sav(self):
        global izm
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.cur = self.connection.cursor()
        if izm:
            vids = self.cur.execute("""SELECT ID, Vid from vid""").fetchall()
            obzh = self.cur.execute("""SELECT ID, Obzharka from obzharka""").fetchall()
            obzhar = ''
            vd = ''
            for j in vids:
                if j[1] == self.molot.currentText():
                    vd = j[0]
                    break
            for j in obzh:
                if j[1] == self.obz.currentText():
                    obzhar = j[0]
                    break
            self.cur.execute('''UPDATE cofe
                                SET Sortes_name = ?
                                WHERE (ID = ?)''', (self.name.text(), int(ad.idd.text())))
            self.cur.execute('''UPDATE cofe
                                SET Stepen_obzharki = ?
                                WHERE (ID = ?)''', (obzhar, int(ad.idd.text())))
            self.cur.execute('''UPDATE cofe
                                SET Vid = ?
                                WHERE (ID = ?)''', (vd, int(ad.idd.text())))
            self.cur.execute('''UPDATE cofe
                                SET Opisanie_vkusa = ?
                                WHERE (ID = ?)''', (self.vkus.text(), int(ad.idd.text())))
            self.cur.execute('''UPDATE cofe
                                SET Price = ?
                                WHERE (ID = ?)''', (self.price.value(), int(ad.idd.text())))
            self.cur.execute('''UPDATE cofe
                                SET Volume = ?
                                WHERE (ID = ?)''', (self.ob.value(), int(ad.idd.text())))
            ad.idd.setText('1')
            ad.name.setText('')
            ad.obz.setCurrentIndex(0)
            ad.molot.setCurrentIndex(0)
            ad.ob.setValue(1)
            ad.price.setValue(1)
            ad.vkus.setText('')
        else:
            vids = self.cur.execute("""SELECT ID, Vid from vid""").fetchall()
            obzh = self.cur.execute("""SELECT ID, Obzharka from obzharka""").fetchall()
            obzhar = ''
            vd = ''
            for j in vids:
                if j[1] == self.molot.currentText():
                    vd = j[0]
                    break
            for j in obzh:
                if j[1] == self.obz.currentText():
                    obzhar = j[0]
                    break
            self.cur.execute('''INSERT INTO cofe(ID, Sortes_name, Stepen_obzharki, Vid, Opisanie_vkusa, Price, Volume) VALUES(?, ?, ?, ?, ?, ?, ?)''', (int(ad.idd.text()), self.name.text(), obzhar, vd, self.vkus.text(), self.price.value(), self.ob.value(), ))
            ad.idd.setText('1')
            ad.name.setText('')
            ad.obz.setCurrentIndex(0)
            ad.molot.setCurrentIndex(0)
            ad.ob.setValue(1)
            ad.price.setValue(1)
            ad.vkus.setText('')
        self.connection.commit()
        ad.close()
        mn.agg()
        izm = False


if __name__ == '__main__':
    izm = False
    app = QApplication(sys.argv)
    mn = Main()
    ad = Add_cofe()
    mn.show()
    sys.exit(app.exec())

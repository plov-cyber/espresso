import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic
import sqlite3


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.fill_table()
        self.titles = None

    def fill_table(self):
        with sqlite3.connect('coffee.db') as con:
            cur = con.cursor()
            result = cur.execute('select * from coffee').fetchall()
            r_degree = cur.execute('select r_degree from roast_degree').fetchall()
            tastes = cur.execute('select taste from tastes').fetchall()
            c_type = cur.execute('select name from type').fetchall()
            self.table.setRowCount(len(result))
            self.table.setColumnCount(len(result[0]))
            for i, row in enumerate(result):
                for j, elem in enumerate(row):
                    if j == 2:
                        self.table.setItem(i, j, QTableWidgetItem(str(r_degree[elem - 1][0])))
                    elif j == 3:
                        self.table.setItem(i, j, QTableWidgetItem(str(c_type[elem - 1][0])))
                    elif j == 4:
                        self.table.setItem(i, j, QTableWidgetItem(str(tastes[elem - 1][0])))
                    else:
                        self.table.setItem(i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

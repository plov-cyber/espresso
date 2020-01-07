from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sqlite3
from AddEditForm import EditForm


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/main.ui', self)
        self.fill_table()
        self.add_btn.clicked.connect(self.add_form)
        self.edit_btn.clicked.connect(self.edit_form)
        self.titles = None
        self.form = EditForm(self.table, self)

    def fill_table(self):
        with sqlite3.connect('data/coffee.db') as con:
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

    def add_form(self):
        self.form.setWindowModality(Qt.ApplicationModal)
        self.form.setWindowTitle('Добавить строку')
        self.form.save_btn.setText('Добавить')
        self.form.show()

    def edit_form(self):
        self.form.setWindowModality(Qt.ApplicationModal)
        self.form.setWindowTitle('Редактировать строку')
        self.form.save_btn.setText('Сохранить')
        self.form.fill_form(self.table.currentRow())
        self.form.show()

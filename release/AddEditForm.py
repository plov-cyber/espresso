from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import sqlite3


class EditForm(QMainWindow):
    def __init__(self, table, mainwindow):
        super().__init__()
        uic.loadUi('UI/addEditCoffeeForm.ui', self)
        self.mainwindow = mainwindow
        self.table = table
        self.save_btn.clicked.connect(self.save_res)
        self.row = None
        with sqlite3.connect('data/coffee.db') as con:
            cur = con.cursor()
            r_degree = cur.execute('select r_degree from roast_degree').fetchall()
            tastes = cur.execute('select taste from tastes').fetchall()
            c_type = cur.execute('select name from type').fetchall()
            self.r_degree_box.addItems([i[0] for i in r_degree])
            self.c_type_box.addItems([i[0] for i in c_type])
            self.taste_box.addItems([i[0] for i in tastes])

    def fill_form(self, row):
        self.row = row
        self.name_edit.setText(self.table.item(row, 1).text())
        self.r_degree_box.setCurrentText(self.table.item(row, 2).text())
        self.c_type_box.setCurrentText(self.table.item(row, 3).text())
        self.taste_box.setCurrentText(self.table.item(row, 4).text())
        self.price_box.setValue(int(self.table.item(row, 5).text()))
        self.vol_box.setValue(int(self.table.item(row, 6).text()))

    def save_res(self):
        with sqlite3.connect('data/coffee.db') as con:
            cur = con.cursor()
            r_degree = cur.execute(
                f"select id from roast_degree where r_degree = '{self.r_degree_box.currentText()}'").fetchone()[0]
            c_type = cur.execute(
                f"select id from type where name = '{self.c_type_box.currentText()}'").fetchone()[0]
            taste = cur.execute(
                f"select id from tastes where taste = '{self.taste_box.currentText()}'").fetchone()[0]
            if self.save_btn.text() == 'Добавить':
                cur.execute(
                    f"insert into coffee(name, roast_degree, type, taste, price, pack_vol) values"
                    f"('{self.name_edit.text()}', {r_degree}, {c_type},"
                    f" {taste}, {self.price_box.value()}, {self.vol_box.value()})")
                self.table.setRowCount(self.table.rowCount() + 1)
            else:
                id = self.table.item(self.row, 0).text()
                cur.execute(f"update coffee set name = '{self.name_edit.text()}' where id = {id}")
                cur.execute(f"update coffee set roast_degree = {r_degree} where id = {id}")
                cur.execute(f"update coffee set type = {c_type} where id = {id}")
                cur.execute(f"update coffee set taste = {taste} where id = {id}")
                cur.execute(f"update coffee set price = {self.price_box.value()} where id = {id}")
                cur.execute(f"update coffee set pack_vol = {self.vol_box.value()} where id = {id}")
        self.clear_form()
        self.mainwindow.fill_table()
        self.close()

    def clear_form(self):
        self.name_edit.setText('')
        self.r_degree_box.setCurrentIndex(0)
        self.c_type_box.setCurrentIndex(0)
        self.taste_box.setCurrentIndex(0)
        self.price_box.setValue(0)
        self.vol_box.setValue(0)

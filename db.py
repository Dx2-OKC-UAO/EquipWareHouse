import sqlite3 as sq
from datetime import date
from dirwork import create_file, create_file_between
from xlsxwriter.workbook import Workbook
from tkinter import messagebox as mb


def start_object_db():
    global db, cur
    db = sq.connect('1C.db')
    cur = db.cursor()
    if db:
        print('Object data base connected OK!')


def start_cart_db():
    global db_cart, cur_cart
    db_cart = sq.connect('Cart.db')
    cur_cart = db_cart.cursor()
    if db:
        print('Cart data base connected OK!')


def get_data():
    all_data = []
    query = """ SELECT * FROM Home """
    cur.execute(query)
    all_data = cur.fetchall()

    return all_data


def get_data_cart():
    cart = []
    query = """ SELECT * FROM Warehouse """
    cur_cart.execute(query)
    cart = cur_cart.fetchall()

    return cart


def write_off(var):
    status = 'Списано'
    cur.execute('''UPDATE Home SET Status=? WHERE Id_number=?''', (status, var))
    db.commit()


def add_new_record(local, name, ident, number, quantity, status, state):
    cur.execute(
        '''INSERT INTO Home (Local, Name, Ident, Number, Quantity, Status, State) VALUES (?, ?, ?, ?, ?, ?, ?) ''',
        (local, name, ident, number, quantity, status, state))
    db.commit()


def add_new_record_cart(name, quantity, barcode):
    cur_cart.execute(
        '''INSERT INTO Warehouse (Name, Quantity, Barcode) VALUES (?, ?, ?) ''',
        (name, quantity, barcode))
    db_cart.commit()


def edit_records(local, name, ident, number, quantity, status, state, var):
    cur.execute(
        '''UPDATE Home SET Local=?, Name=?, Ident=?, Number=?, Quantity=?, Status=?, State=? WHERE Id_number=?''',
        (local, name, ident, number, quantity, status, state, var))
    db.commit()


def search_records(description):
    cur.execute('''SELECT * FROM Home WHERE name LIKE ?''', description)
    row = cur.fetchall()
    return row


def search_records_cart(description):
    cur_cart.execute('''SELECT * FROM Warehouse WHERE name LIKE ?''', description)
    row = cur_cart.fetchall()
    return row


def give_object(state, var):
    status = 'Выдано'
    cur.execute(
        '''UPDATE Home SET Status=?, State=? WHERE Id_number=?''',
        (status, state, var))
    db.commit()


def give_object_cart(name, quantity, barcode, state, user, application, var):
    current_date = date.today()
    cur_cart.execute('''Select Quantity FROM Warehouse WHERE Id=?''', var)
    number = cur_cart.fetchone()
    number_f = int(number[0])
    final = number_f - int(quantity)
    if final > 0:
        cur_cart.execute('''UPDATE Warehouse SET Quantity=? WHERE Id=?''', (final, var))
        db_cart.commit()
        cur_cart.execute('''SELECT ID FROM Issued WHERE Id=(SELECT MAX(Id) FROM Issued)''')
        ID_last = cur_cart.fetchone()
        cur_cart.execute(
            '''INSERT INTO Issued (Name, Quantity, Barcode, State, User, Application, Data) VALUES (?, ?, ?, ?, ?, ?, ?) ''',
            (name, quantity, barcode, state, user, application, current_date))
        db_cart.commit()
        cur_cart.execute('''SELECT ID FROM Issued WHERE Id=(SELECT MAX(Id) FROM Issued)''')
        ID_new = cur_cart.fetchone()

        if ID_new > ID_last:
            mb.showinfo('Информация', 'Картридж выдан')
        else:
            mb.showerror('Ошибка', 'Убери свои кривые руки от компьютера!!!')

    else:
        mb.showerror('Информация', 'Картриджы отсутвуют')


def get_map():
    maps = []
    cur_cart.execute('''SELECT Maps FROM Map''')
    maps = cur_cart.fetchall()
    return maps


def download_cart():
    name_of_file = create_file()
    workbook = Workbook('Отчеты/' + name_of_file)
    worksheet = workbook.add_worksheet()

    cur_cart.execute("SELECT * FROM Issued")
    mysel = cur_cart.fetchall()
    for i, row in enumerate(mysel):
        for j, value in enumerate(row):
            worksheet.write(i, j, row[j])
    workbook.close()


def download_cart_between(data_1, data_2):
    name_of_file = create_file_between()
    workbook = Workbook('Отчеты/' + name_of_file)
    worksheet = workbook.add_worksheet()
    data_1_1 = "'" + data_1 + "'"
    data_2_1 = "'" + data_2 + "'"

    cur_cart.execute(f'SELECT * FROM Issued WHERE Data BETWEEN {data_1_1} and {data_2_1}')
    list_records = cur_cart.fetchall()
    for i, row in enumerate(list_records):
        for j, value in enumerate(row):
            worksheet.write(i, j, row[j])
    workbook.close()


def change_cart_quantity(have, take, var):
    summ = int(have) + int(take)
    cur_cart.execute('''UPDATE Warehouse SET Quantity=? WHERE Id=?''', (summ, var))
    db_cart.commit()
    mb.showinfo('Информация', 'Данные обновлены')


def check_user(log, pas):
    log_r, pas_r = 0, 0
    current_date = date.today()
    log_list = []
    pas_list = []
    cur_cart.execute('''SELECT LOGIN FROM Users''')
    log_list = cur_cart.fetchall()
    cur_cart.execute('''SELECT PASSWORD FROM Users''')
    pas_list = cur_cart.fetchall()

    for login in log_list:
        if ("".join(login)) == log:
            log_r = 2
            for password in pas_list:
                if ("".join(password)) == pas:
                    pas_r = 1
                    cur_cart.execute('''INSERT INTO History (Login,Data) VALUES (?,?)''', (log, current_date))
                    db_cart.commit()
                    mb.showinfo('Авторизация', 'Авторизация прошла успешно')
                else:
                    mb.showerror('Авторизация', 'Пароль не верный')
        else:
            mb.showerror('Авторизация', 'Такой логин не зарегистрирован')

    res = log_r + pas_r
    return res


def defalt_data(var):
    cur.execute('''SELECT * FROM Home WHERE Id_number=?''', [var])
    row = cur.fetchone()
    return row


def defalt_data_cart(var):
    cur_cart.execute('''SELECT * FROM Warehouse WHERE Id=?''', [var])
    row = cur_cart.fetchone()
    return row


def defalt_quantity(var):
    cur_cart.execute('''SELECT Quantity FROM Warehouse WHERE Id=?''', [var])
    row = cur_cart.fetchone()
    return row



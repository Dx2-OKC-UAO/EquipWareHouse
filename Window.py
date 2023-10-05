from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import db
from tkinter.ttk import Notebook
from tkcalendar import DateEntry
import functions
import globals


class Window(Frame):

    def __init__(self, root, res):
        super().__init__(root)
        self.res = res
        self.update_img = None
        self.draw_widgets()
        self.draw_menu()
        self.view_records()

    #        self.view_records_cart()

    def draw_widgets(self):
        tabs_control = Notebook()
        tabs_control.enable_traversal()
        tab_1 = Frame(tabs_control)
        tabs_control.add(tab_1, text="Техника")
        tab_2 = Frame(tabs_control)
        tabs_control.add(tab_2, text="Катриджи")
        tabs_control.pack(fill=BOTH, expand=1)

        # Создание меню техники

        toolbar = Frame(tab_1, width=1000, height=100, bg='beige', bd=2)

        self.add_img = PhotoImage(file='icons/add.png')
        btn_open_dialog = Button(toolbar, text='Добавить товар ', bg='beige',
                                 bd=0, compound=TOP, image=self.add_img, command=self.add)
        btn_open_dialog.grid(row=0, column=0)

        self.update_img = PhotoImage(file='icons/edit.png')
        btn_edit_dialog = Button(toolbar, text='Редактировать', bg='beige', bd=0, image=self.update_img,
                                 compound=TOP, command=self.edit)
        btn_edit_dialog.grid(row=0, column=1)

        self.delete_img = PhotoImage(file='icons/delete.png')
        btn_delete_dialog = Button(toolbar, text='Списать', bg='beige', bd=0, image=self.delete_img,
                                   compound=TOP, command=self.write_off_db)
        btn_delete_dialog.grid(row=0, column=2)

        self.search_img = PhotoImage(file='icons/search.png')
        btn_search = Button(toolbar, text='Поиск', bg='beige', bd=0, image=self.search_img,
                            compound=TOP, command=self.search)

        btn_search.grid(row=0, column=3)

        self.refresh_img = PhotoImage(file='icons/refresh.png')
        btn_refresh = Button(toolbar, text='Обновить', bg='beige', bd=0, image=self.refresh_img,
                             compound=TOP, command=self.view_records)
        btn_refresh.grid(row=0, column=4)

        self.give_img = PhotoImage(file='icons/delete.png')
        btn_delete_dialog = Button(toolbar, text='Выдать', bg='beige', bd=0, image=self.delete_img,
                                   compound=TOP, command=self.give)
        btn_delete_dialog.grid(row=0, column=5)
        toolbar.pack(fill=BOTH)

        # Создание меню картриджей

        toolbar_cart = Frame(tab_2, width=1000, height=100, bg='beige', bd=2)

        self.add_img_cart = PhotoImage(file='icons/add.png')
        btn_open_dialog = Button(toolbar_cart, text='Добавить товар ', bg='beige',
                                 bd=0, compound=TOP, image=self.add_img_cart, command=self.add_cart)
        btn_open_dialog.grid(row=0, column=0, padx=3)

        self.come_img_cart = PhotoImage(file='icons/come.png')
        btn_open_dialog = Button(toolbar_cart, text='Приход  ', bg='beige',
                                 bd=0, compound=TOP, image=self.come_img_cart, command=self.add_cart_quantity)
        btn_open_dialog.grid(row=0, column=1, padx=3)

        self.search_img_cart = PhotoImage(file='icons/search.png')
        btn_search = Button(toolbar_cart, text='Поиск', bg='beige', bd=0, image=self.search_img_cart,
                            compound=TOP, command=self.search_cart)

        btn_search.grid(row=0, column=2, padx=3)

        self.refresh_img_cart = PhotoImage(file='icons/refresh.png')
        btn_refresh = Button(toolbar_cart, text='Обновить', bg='beige', bd=0, image=self.refresh_img_cart,
                             compound=TOP, command=self.view_records)
        btn_refresh.grid(row=0, column=3, padx=3)

        self.give_img_cart = PhotoImage(file='icons/delete.png')
        cart_btn_delete_dialog = Button(toolbar_cart, text='Выдать', bg='beige', bd=0, image=self.delete_img,
                                        compound=TOP, command=self.give_cart)
        cart_btn_delete_dialog.grid(row=0, column=4, padx=3)

        self.add_cart_img_cart = PhotoImage(file='icons/add_cart.png')
        btn_open_dialog = Button(toolbar_cart, text='Добавить товар в список ', bg='beige',
                                 bd=0, compound=TOP, image=self.add_cart_img_cart, command=self.add_list_cart)
        btn_open_dialog.grid(row=0, column=5, padx=3)

        self.give_all_img_cart = PhotoImage(file='icons/give.png')
        btn_open_dialog = Button(toolbar_cart, text='Выдать все картриджи ', bg='beige',
                                 bd=0, compound=TOP, image=self.give_all_img_cart, command=self.open_many_cart)
        btn_open_dialog.grid(row=0, column=6, padx=3)

        self.clean_basket_img_cart = PhotoImage(file='icons/delete.png')
        btn_open_dialog = Button(toolbar_cart, text='Очистить список', bg='beige',
                                 bd=0, compound=TOP, image=self.clean_basket_img_cart, command=self.clear)
        btn_open_dialog.grid(row=0, column=7, padx=3)

        self.buy_img_cart = PhotoImage(file='icons/basket.png')
        btn_open_dialog = Button(toolbar_cart, text='Добавить в закупку', bg='beige',
                                 bd=0, compound=TOP, image=self.buy_img_cart, command=self.cart_to_buy)
        btn_open_dialog.grid(row=0, column=8, padx=3)

        toolbar_cart.pack(fill=BOTH)


        # СОЗДАНИЕ ВИДЖЕТА ТАБЛИЦЫ ТЕХНИКИ

        heads = ['Id_number', 'Local', 'Name', 'Ident', 'Number', 'Quantity', 'Status', 'State']
        self.tree = ttk.Treeview(tab_1, show='headings')
        self.tree['columns'] = heads
        self.tree.column('Id_number', width=5, anchor='center')
        self.tree.column('Local', width=100, anchor='w')
        self.tree.column('Name', width=95, anchor='w')
        self.tree.column('Ident', width=100, anchor='e')
        self.tree.column('Number', width=50, anchor='w')
        self.tree.column('Quantity', width=50, anchor='center')
        self.tree.column('Status', width=100, anchor='w')
        self.tree.column('State', width=100, anchor='w')
        self.tree.heading('Id_number', text='ID')
        self.tree.heading('Local', text='Местоположение')
        self.tree.heading('Name', text='Название')
        self.tree.heading('Ident', text='Идент')
        self.tree.heading('Number', text='Номер')
        self.tree.heading('Quantity', text='Количество')
        self.tree.heading('Status', text='Статус')
        self.tree.heading('State', text='Кому выдано')
        for row in db.get_data():
            self.tree.insert('', END, values=row)
        scroll_y = ttk.Scrollbar(tab_1, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(fill=Y, side=RIGHT)
        self.tree.pack(fill=BOTH, expand=1)

        # СОЗДАНИЕ ВИДЖЕТА ТАБЛИЦЫ КАТРИДЖЕЙ

        heads = ['Id', 'Name', 'Quantity', 'Barcode']
        self.tree2 = ttk.Treeview(tab_2, show='headings')
        self.tree2['columns'] = heads
        self.tree2.column('Id', width=5, anchor='center')
        self.tree2.column('Name', width=95, anchor='w')
        self.tree2.column('Quantity', width=50, anchor='center')
        self.tree2.column('Barcode', width=100, anchor='w')
        self.tree2.heading('Id', text='ID')
        self.tree2.heading('Name', text='Название')
        self.tree2.heading('Quantity', text='Количество')
        self.tree2.heading('Barcode', text='Штрих-код')
        self.tree2.tag_configure('few', foreground='red')
        self.tree2.tag_configure('buy', foreground='green')
        self.tree2.tag_configure('enough', foreground='black')
        for row in db.get_data_cart():
            if row[2] == '':
                self.tree2.insert('', END, values=row, tags=('enough',))
                continue
            if row[2] is None:
                self.tree2.insert('', END, values=row, tags=('enough',))
                continue
            if row[2] < 5:
                self.tree2.insert('', END, values=row, tags=('few',))
            if row[4] == 1:
                self.tree2.insert('', END, values=row, tags=('buy',))
        scroll_y = ttk.Scrollbar(tab_2, orient='vertical', command=self.tree2.yview)
        self.tree2.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(fill=Y, side=RIGHT)
        self.tree2.pack(fill=BOTH, expand=1)

    def draw_menu(self):

        menu_bar = Menu(root)
        root.configure(menu=menu_bar)
        #        menu_bar.add_command(label='Выгрузить')
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_separator()
        file_menu.add_command(label='Выгрузить за все время', command=self.download)
        file_menu.add_command(label='Выгрузить с определенной даты')
        file_menu.add_command(label='Выгрузить за период', command=self.download_b)

        log_menu = Menu(menu_bar, tearoff=0)
        log_menu.add_command(label='Авторизоваться в программе', command=self.class_log)
        log_menu.add_command(label='Выйти из аккаунта', command=self.exit)

        bar_menu = Menu(menu_bar, tearoff=0)
        bar_menu.add_command(label='Вывести штрих-код', command=self.print_bar)

        #
        # info_menu = Menu(menu_bar, tearoff=0)
        # info_menu.add_command(label="О приложении")
        #
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        menu_bar.add_cascade(label='Авторизация', menu=log_menu)
        menu_bar.add_cascade(label='Штрих-код', menu=bar_menu)

        # menu_bar.add_cascade(label="Справка", menu=info_menu)

    # ++++++++++++++++++++БЛОК ФУНКЦИЙ МЕНЮ++++++++++++++++++++ #

    # --------------------Выгрузка отчетов-------------------- #
    def download(self):
        db.download_cart()
        mb.showinfo('Информация', 'Данные выгружены в папку отчеты')

    def download_between(self, data_1, data_2):
        db.download_cart_between(data_1, data_2)
        mb.showinfo('Информация', 'Данные выгружены в папку отчеты')

    # --------------------Обновление данных на страницах-------------------- #
    def view_records(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in db.get_data()]
        [self.tree2.delete(i) for i in self.tree2.get_children()]
        for row in db.get_data_cart():
            if row[4] == 1:
                self.tree2.insert('', END, values=row, tags=('buy',))
            else:
                if row[2] == '':
                    self.tree2.insert('', END, values=row, tags=('enough',))
                    continue
                if row[2] is None:
                    self.tree2.insert('', END, values=row, tags=('enough',))
                    continue
                if row[2] < 5:
                    self.tree2.insert('', END, values=row, tags=('few',))
                if row[2] >= 5:
                    self.tree2.insert('', END, values=row, tags=('enough',))

    def cart_to_buy(self):

        # if self.res == 3:
        try:
            db.cart_buy_db(self.tree2.set(self.tree2.selection()[0], '#1'))
        except IndexError:
            mb.showwarning('Информация', 'Пожалуйста выберите запись')
        # else:
        #     mb.showerror('Ошибка', 'Необходимо авторизоваться')
        self.view_records()



    # --------------------Добавление записей-------------------- #
    # Добавить запись
    def add_new_record(self, local, name, ident, number, quantity, status, state):
        db.add_new_record(local, name, ident, number, quantity, status, state)
        self.view_records()

    def add_new_record_cart(self, name, quantity, barcode):
        db.add_new_record_cart(name, quantity, barcode)
        self.view_records()

    # --------------------Редактирование записей-------------------- #

    def update_record(self, local, name, ident, number, quantity, status, state):
        try:
            db.edit_records(local, name, ident, number, quantity, status, state,
                            self.tree.set(self.tree.selection()[0], '#1'))
        except IndexError:
            mb.showwarning('Информация', 'Пожалуйста выберите запись')
        self.view_records()

    def change_quantity(self, have, take):
        db.change_cart_quantity(have, take, self.tree2.set(self.tree2.selection()[0], '#1'))
        self.view_records()

    def write_off_db(self):

        if self.res == 3:
            try:
                db.write_off(self.tree.set(self.tree.selection()[0], '#1'))
            except IndexError:
                mb.showwarning('Информация', 'Пожалуйста выберите запись')
        else:
            mb.showerror('Ошибка', 'Необходимо авторизоваться')
        self.view_records()

    def give_object(self, state):

        db.give_object(state, self.tree.set(self.tree.selection()[0], '#1'))
        self.view_records()

    def give_object_cart(self, name, quantity, barcode, state, user, application):

        db.give_object_cart(name, quantity, barcode, state, user, application,
                            self.tree2.set(self.tree2.selection()[0], '#1'))
        self.view_records()

    def give_many_cart(self, final_list):

        db.give_many_cart(final_list)
        self.view_records()

    def clear(self):
        globals.listCart = []


    def add_in_list_cart(self, name, quantity):

        functions.list_of_cart(name, quantity, self.tree2.set(self.tree2.selection()[0], '#1'))
        self.view_records()

    # --------------------Поиск среди записей-------------------- #
    def search_records(self, name, trigger):
        if trigger == 1:
            description = ('%' + name + '%',)
            [self.tree.delete(i) for i in self.tree.get_children()]
            [self.tree.insert('', 'end', values=row) for row in db.search_records(description, 1)]
        else:
            description = ('%' + name + '%',)
            [self.tree2.delete(i) for i in self.tree2.get_children()]
            [self.tree2.insert('', 'end', values=row) for row in db.search_records(description, 2)]

    # --------------------Menu bar-------------------- #
    def logg_in(self, log, pas):
        self.res = db.check_user(log, pas)

    def exit(self):
        self.res = 0

    def print_bar(self):
        try:
            self.tree2.set(self.tree2.selection()[0], '#1')
            db.get_bar(self.tree2.set(self.tree2.selection()[0], '#1'))
        except IndexError:
            mb.showwarning('Информация', 'Пожалуйста выберите запись')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    # ---------------------------------------------------------- #
    # ++++++++++++++++++++Активация дочерних окон++++++++++++++++++++ #

    # --------------------Добавление записей-------------------- #
    def add(self):
        if self.res == 3:
            AddData()
        else:
            mb.showerror('Ошибка', 'Необходимо авторизоваться')

    def add_cart(self):
        if self.res == 3:
            AddDataCart()
        else:
            mb.showerror('Ошибка', 'Необходимо авторизоваться')

    # --------------------Редактирование записей-------------------- #
    def edit(self):
        if self.res == 3:
            try:
                self.tree.set(self.tree.selection()[0], '#1')
                EditRecord()
            except IndexError:
                mb.showwarning('Информация', 'Пожалуйста выберите запись')
        else:
            mb.showerror('Ошибка', 'Необходимо авторизоваться')

    def give(self):
        try:
            self.tree.set(self.tree.selection()[0], '#1')
            Give()
        except IndexError:
            mb.showwarning('Информация', 'Пожалуйста выберите запись')

    def give_cart(self):
        try:
            self.tree2.set(self.tree2.selection()[0], '#1')
            GiveCart()
        except IndexError:
            mb.showwarning('Информация', 'Пожалуйста выберите запись')

    def add_list_cart(self):
        try:
            self.tree2.set(self.tree2.selection()[0], '#1')
            ListCart()
        except IndexError:
            mb.showwarning('Информация', 'Пожалуйста выберите запись')

    def add_cart_quantity(self):
        if self.res == 3:
            try:
                self.tree2.set(self.tree2.selection()[0], '#1')
                AddCartQuantity()
            except IndexError:
                mb.showwarning('Информация', 'Пожалуйста выберите запись')
        else:
            mb.showerror('Ошибка', 'Необходимо авторизоваться')

    def open_many_cart(self):
        ManyCart()

    # --------------------Поиск среди записей-------------------- #
    def search(self):
        Search()

    def search_cart(self):
        SearchCart()

    # --------------------Menu bar-------------------- #

    def download_b(self):
        DownLoad()

    def class_log(self):
        Authorization()
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    # ---------------------------------------------------------- #


class AddData(Toplevel):

    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_child()

    def init_child(self):
        self.title('Добавить товар')
        self.geometry('400x250+400+300')
        self.resizable(False, False)

        label_local = Label(self, text='Местоположение')
        label_local.grid(row=0, column=0, sticky='w', padx=50)

        label_name = Label(self, text='Название')
        label_name.grid(row=1, column=0, sticky='w', padx=50)

        label_ident = Label(self, text='Ident: ')
        label_ident.grid(row=2, column=0, sticky='w', padx=50)

        label_number = Label(self, text='Номер: ')
        label_number.grid(row=3, column=0, sticky='w', padx=50)

        label_quantity = Label(self, text='Количесвто: ')
        label_quantity.grid(row=4, column=0, sticky='w', padx=50)

        label_status = Label(self, text='Статус: ')
        label_status.grid(row=5, column=0, sticky='w', padx=50)

        label_state = Label(self, text='Кому выдано: ')
        label_state.grid(row=6, column=0, sticky='w', padx=50)

        self.entry_local = ttk.Entry(self, width=25)
        self.entry_local.grid(row=0, column=1, sticky='e', padx=10, pady=3)

        self.entry_name = ttk.Entry(self, width=25)
        self.entry_name.grid(row=1, column=1, sticky='e', padx=10, pady=3)

        self.entry_ident = ttk.Entry(self, width=25)
        self.entry_ident.grid(row=2, column=1, sticky='e', padx=10, pady=3)

        self.entry_number = ttk.Entry(self, width=25)
        self.entry_number.grid(row=3, column=1, sticky='e', padx=10, pady=3)

        self.entry_quantity = ttk.Entry(self, width=25)
        self.entry_quantity.grid(row=4, column=1, sticky='e', padx=10, pady=3)

        self.btn_combobox = ttk.Combobox(self, values=['', 'В наличии', 'Списано', 'Выдано'], width=22)
        self.btn_combobox.current(0)
        self.btn_combobox.grid(row=5, column=1, sticky='e', padx=10, pady=3)

        self.entry_state = ttk.Entry(self, width=25)
        self.entry_state.grid(row=6, column=1, sticky='e', padx=10, pady=3)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.grid(row=7, column=0, pady=10)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.grid(row=7, column=1, pady=10)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.add_new_record(self.entry_local.get(),
                                                                              self.entry_name.get(),
                                                                              self.entry_ident.get(),
                                                                              self.entry_number.get(),
                                                                              self.entry_quantity.get(),
                                                                              self.btn_combobox.get(),
                                                                              self.entry_state.get()))

        self.grab_set()
        self.focus_set()


class AddDataCart(Toplevel):

    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_child()

    def init_child(self):
        self.title('Добавить товар')
        self.geometry('400x130+400+300')
        self.resizable(False, False)

        cart_label_name = Label(self, text='Название')
        cart_label_name.grid(row=0, column=0, sticky='w', padx=60)

        cart_label_quantity = Label(self, text='Количесвто: ')
        cart_label_quantity.grid(row=1, column=0, sticky='w', padx=60)

        cart_label_barcode = Label(self, text='Штрих-код: ')
        cart_label_barcode.grid(row=2, column=0, sticky='w', padx=60)

        self.cart_entry_name = ttk.Entry(self)
        self.cart_entry_name.grid(row=0, column=1, sticky='e', padx=10, pady=3)

        self.cart_entry_quantity = ttk.Entry(self)
        self.cart_entry_quantity.grid(row=1, column=1, sticky='e', padx=10, pady=3)

        self.cart_entry_barcode = ttk.Entry(self)
        self.cart_entry_barcode.grid(row=2, column=1, sticky='e', padx=10, pady=3)

        cart_btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        cart_btn_cancel.grid(row=3, column=0, sticky='e', padx=10, pady=10)

        self.cart_btn_ok = ttk.Button(self, text='Добавить')
        self.cart_btn_ok.grid(row=3, column=1)
        self.cart_btn_ok.bind('<Button-1>', lambda event: self.view.add_new_record_cart(self.cart_entry_name.get(),
                                                                                        self.cart_entry_quantity.get(),
                                                                                        self.cart_entry_barcode.get()))

        self.grab_set()
        self.focus_set()


class EditRecord(AddData):
    def __init__(self):
        super().__init__()
        self.default()
        self.view = app
        self.init_edit()

    def init_edit(self):
        self.title('Редактировать товары')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.grid(row=7, column=1)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_local.get(),
                                                                          self.entry_name.get(),
                                                                          self.entry_ident.get(),
                                                                          self.entry_number.get(),
                                                                          self.entry_quantity.get(),
                                                                          self.btn_combobox.get(),
                                                                          self.entry_state.get()))

        # self.btn_ok.destroy()

    def default(self):
        row = db.defalt_data(self.view.tree.set(self.view.tree.selection()[0], '#1'))
        self.entry_local.insert(0, row[1])
        self.entry_name.insert(0, row[2])
        self.entry_ident.insert(0, row[3])
        self.entry_number.insert(0, row[4])
        self.entry_quantity.insert(0, row[5])
        self.btn_combobox.insert(0, row[6])
        if row[7] is not None:
            self.entry_state.insert(0, row[7])
        else:
            self.entry_state.insert(0, 'None')


class AddCartQuantity(Toplevel):
    def __init__(self):
        super().__init__()
        self.view = app
        self.change()
        self.default_change()

    def change(self):
        self.title('Приход')
        self.geometry('300x130+400+300')
        self.resizable(False, False)

        label_have = Label(self, text='Катриджей на складе: ')
        label_have.grid(row=0, column=0, padx=20, pady=5, sticky='w')

        label_take = Label(self, text='Катриджей пришло:')
        label_take.grid(row=1, column=0, padx=20, pady=5, sticky='w')

        self.entry_have = ttk.Entry(self)
        self.entry_have.grid(row=0, column=1)

        self.entry_take = ttk.Entry(self)
        self.entry_take.grid(row=1, column=1)

        btn_edit = ttk.Button(self, text='Принять')
        btn_edit.grid(row=2, column=1, pady=20)
        btn_edit.bind('<Button-1>', lambda event: self.view.change_quantity(self.entry_have.get(),
                                                                            self.entry_take.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.grid(row=2, column=0, pady=20)

    def default_change(self):
        row = db.defalt_quantity(self.view.tree2.set(self.view.tree2.selection()[0], '#1'))
        if row[0] is not None:
            self.entry_have.insert(0, row[0])
        else:
            self.entry_have.insert(0, ' ')


class Search(Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_search()

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get(), 1))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class SearchCart(Search):
    def __init__(self):
        super().__init__()
        self.view = app
        self.init_search_cart()

    def init_search_cart(self):
        self.title('Поиск')
        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get(), 2))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class GiveCart(Toplevel):
    def __init__(self):
        super().__init__(root)
        self.buf = []
        self.view = app
        self.init_give_cart()
        self.default_cart()

    def init_give_cart(self):
        self.title('Выдача')
        self.geometry('600x220+400+300')


        self.resizable(False, False)

        cart_label_name = Label(self, text='Название')
        cart_label_name.grid(row=0, column=0, sticky='w', padx=30)

        cart_label_quantity = Label(self, text='Количество: ')
        cart_label_quantity.grid(row=1, column=0, sticky='w', padx=30)

        cart_label_barcode = Label(self, text='Штрих-код: ')
        cart_label_barcode.grid(row=2, column=0, sticky='w', padx=30)

        cart_label_state = Label(self, text='Куда выдано: ')
        cart_label_state.grid(row=3, column=0, sticky='w', padx=30)

        cart_label_state = Label(self, text='Кому выдано: ')
        cart_label_state.grid(row=4, column=0, sticky='w', padx=30)

        cart_label_application = Label(self, text='Номер заявки: ')
        cart_label_application.grid(row=5, column=0, sticky='w', padx=30)

        self.cart_entry_name = ttk.Entry(self, width=60)
        self.cart_entry_name.grid(row=0, column=1, sticky='e', padx=30, pady=3)

        self.cart_entry_quantity = ttk.Entry(self, width=60)
        self.cart_entry_quantity.insert(END, '1')
        self.cart_entry_quantity.grid(row=1, column=1, sticky='e', padx=30, pady=3)

        self.cart_entry_barcode = ttk.Entry(self, width=60)
        self.cart_entry_barcode.grid(row=2, column=1, sticky='e', padx=30, pady=3)

        self.cart_btn_combobox = ttk.Combobox(self, values=db.get_map(), width=57)
        self.cart_btn_combobox.current(0)
        self.cart_btn_combobox.grid(row=3, column=1, sticky='e', padx=30, pady=3)

        self.cart_entry_user = ttk.Entry(self, width=60)
        self.cart_entry_user.grid(row=4, column=1, sticky='e', padx=30, pady=3)

        self.cart_entry_application = ttk.Entry(self, width=60)
        self.cart_entry_application.grid(row=5, column=1, sticky='e', padx=30, pady=3)

        cart_btn_edit = ttk.Button(self, text='Выдать')
        cart_btn_edit.grid(row=6, column=1, pady=15)
        cart_btn_edit.bind('<Button-1>', lambda event: self.view.give_object_cart(self.cart_entry_name.get(),
                                                                                  self.cart_entry_quantity.get(),
                                                                                  self.cart_entry_barcode.get(),
                                                                                  self.cart_btn_combobox.get(),
                                                                                  self.cart_entry_user.get(),
                                                                                  self.cart_entry_application.get()))
        cart_btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        cart_btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        cart_btn_cancel.grid(row=6, column=0, pady=15)

    def default_cart(self):
        row_cart = db.defalt_data_cart(self.view.tree2.set(self.view.tree2.selection()[0], '#1'))
        self.cart_entry_name.insert(0, row_cart[1])
        self.cart_entry_name.config(state='readonly')
        if row_cart[3] is not None:
            self.cart_entry_barcode.insert(0, row_cart[3])
            self.cart_entry_barcode.config(state='readonly')
        else:
            self.cart_entry_barcode.insert(0, 'None')
            self.cart_entry_barcode.config(state='readonly')


class ListCart(Toplevel):
    def __init__(self):
        super().__init__(root)
        self.buf = []
        self.view = app
        self.init_give_cart()
        self.default_cart()

    def init_give_cart(self):
        self.title('Выдача')
        #self.geometry('400x220+400+300')
        self.geometry('400x130+400+300')
        self.resizable(False, False)

        cart_label_name = Label(self, text='Название')
        cart_label_name.grid(row=0, column=0, sticky='w', padx=30)

        cart_label_quantity = Label(self, text='Количество: ')
        cart_label_quantity.grid(row=1, column=0, sticky='w', padx=30)

        self.cart_entry_name = ttk.Entry(self, width=30)
        self.cart_entry_name.grid(row=0, column=1, sticky='e', padx=30, pady=3)

        self.cart_entry_quantity = ttk.Entry(self, width=30)
        self.cart_entry_quantity.insert(END, '1')
        self.cart_entry_quantity.grid(row=1, column=1, sticky='e', padx=30, pady=3)

        cart_btn_edit = ttk.Button(self, text='Выдать')
        cart_btn_edit.grid(row=6, column=1, pady=15)
        cart_btn_edit.bind('<Button-1>', lambda event: self.view.add_in_list_cart(self.cart_entry_name.get(),
                                                                                  self.cart_entry_quantity.get()))
        cart_btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        cart_btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        cart_btn_cancel.grid(row=6, column=0, pady=15)

    def default_cart(self):
        row_cart = db.defalt_data_cart(self.view.tree2.set(self.view.tree2.selection()[0], '#1'))
        self.cart_entry_name.insert(0, row_cart[1])
        self.cart_entry_name.config(state='readonly')


class Give(Toplevel):
    def __init__(self):
        super().__init__()
        self.view = app
        self.init_give()

    def init_give(self):
        self.title('Выдача')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        self.btn_combobox = ttk.Combobox(self, values=db.get_map(), width=30)
        self.btn_combobox.current(0)
        self.btn_combobox.grid(row=0, column=0, columnspan=10, padx=50, pady=20)

        btn_edit = ttk.Button(self, text='Выдать')
        btn_edit.grid(row=1, column=4)
        btn_edit.bind('<Button-1>', lambda event: self.view.give_object(self.btn_combobox.get()))

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.grid(row=1, column=6)


class DownLoad(Toplevel):

    def __init__(self):
        super().__init__()
        self.view = app
        self.main_cal()

    def main_cal(self):
        self.title('Выбрать промежуток')
        self.geometry('300x120+400+300')

        def get_date():
            selected_date = cal.get()
            print(f"Selected date: {selected_date}")
            return selected_date

        def get_date_2():
            selected_date_2 = cal_2.get()
            print(f"Selected date: {selected_date_2}")
            return selected_date_2

        label_1 = Label(self, text='Начальная дата: ')
        label_1.grid(row=0, column=0, sticky='w', padx=30, pady=10)

        label_2 = Label(self, text='Финальная дата: ')
        label_2.grid(row=1, column=0, sticky='w', padx=30)

        cal = DateEntry(self, date_pattern="yyyy-mm-dd")
        cal.grid(row=0, column=1, pady=10)
        cal_2 = DateEntry(self, date_pattern="yyyy-mm-dd")
        cal_2.grid(row=1, column=1)
        btn = Button(self, text="Подтвердить")
        btn.bind('<Button-1>', lambda event: self.view.download_between(get_date(), get_date_2()))

        btn.grid(row=2, column=0, columnspan=2, pady=15)


class Authorization(Toplevel):
    def __init__(self):
        super().__init__()
        self.view = app
        self.log_in()

    def log_in(self):
        self.title('Авторизация')
        self.geometry('300x130+400+300')

        label_log = Label(self, text='Логин: ')
        label_log.grid(row=0, column=0, sticky='w', padx=5, pady=10)

        label_pas = Label(self, text='Пароль: ')
        label_pas.grid(row=1, column=0, sticky='w', padx=5)

        self.entry_log = ttk.Entry(self, width=30)
        self.entry_log.grid(row=0, column=1, sticky='e', padx=30, pady=3)

        self.entry_pas = ttk.Entry(self, width=30)
        self.entry_pas.grid(row=1, column=1, sticky='e', padx=30, pady=3)

        cart_btn_edit = ttk.Button(self, text='Войти')
        cart_btn_edit.grid(row=6, column=1, pady=15)
        cart_btn_edit.bind('<Button-1>', lambda event: self.view.logg_in(self.entry_log.get(),
                                                                         self.entry_pas.get()))
        cart_btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')


class ManyCart(Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_many_cart()

    def init_many_cart(self):
        my_entries_name = []
        my_entries_count = []
        my_entries_application = []
        list_of_id = []
        self.title('Выдача')
        ll = functions.get_len()
        dl = 50*ll
        self.geometry(f'700x{150 + dl}+500+300')
        label_name = Label(self, text='Название')
        label_qua = Label(self, text='Количество')
        label_num = Label(self, text='Номер заявки')
        label_name.grid(row = 0, column = 0)
        label_qua.grid(row = 0, column = 1)
        label_num.grid(row = 0, column = 2)
        y = 1
        for x in range(ll):
            my_entry = ttk.Entry(self)
            my_entry.insert(END, globals.listCart[x][0])
            my_entry_2 = ttk.Entry(self)
            my_entry_2.insert(END, globals.listCart[x][1])
            my_entry_3 = ttk.Entry(self)

            my_entry.grid(row= x+1, column = 0, pady=10, padx = 5)
            my_entry_2.grid(row= x+1, column = 1, pady=10, padx = 5)
            my_entry_3.grid(row= x+1, column = 2, pady=10, padx = 5)
            my_entries_name.append(my_entry)
            my_entries_count.append(my_entry_2)
            my_entries_application.append(my_entry_3)
            list_of_id.append(globals.listCart[x][2])
            y += 1

        label = Label(self, text = '-------------------------------------------------------------------------------------------------------------------------')
        label.grid(row = y + 1, column=0, columnspan=3)
        cart_label_state = Label(self, text='Куда выдано: ')
        cart_label_state.grid(row = y + 2, column=0, sticky='w', padx = 15)

        cart_label_state = Label(self, text='Кому выдано: ')
        cart_label_state.grid(row = y + 3, column=0, sticky='w', padx = 15)


        self.cart_btn_combobox = ttk.Combobox(self, values=db.get_map(), width=57)
        self.cart_btn_combobox.current(0)
        self.cart_btn_combobox.grid(row = y + 2, column=1, sticky='e', padx=30, pady=3)

        self.cart_entry_user = ttk.Entry(self, width=60)
        self.cart_entry_user.grid(row = y + 3, column=1, sticky='e', padx=30, pady=3)

        cart_btn_edit = ttk.Button(self, text='Выдать')
        cart_btn_edit.grid(row = y + 4, column=1, pady=15)
        # cart_btn_edit.bind('<Button-1>', lambda event: self.list_name(my_entries_name, list_1), add='+')
        # print(list_1)
        # cart_btn_edit.bind('<Button-1>', lambda event: self.list_count(my_entries_count, list_2), add='+')
        # cart_btn_edit.bind('<Button-1>', lambda event: self.list_application(my_entries_application, list_3), add='+')
        cart_btn_edit.bind('<Button-1>', lambda event: self.get_c(y - 1, self.list_name(my_entries_name),
                                                                  self.list_count(my_entries_count),
                                                                  self.list_application(my_entries_application),
                                                                  self.cart_btn_combobox.get(),
                                                                  self.cart_entry_user.get(), list_of_id), add='+')

        cart_btn_edit.bind('<Button-1>', lambda event: self.view.clear(), add='+')
        cart_btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        cart_btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        cart_btn_cancel.grid(row = y + 4, column=0, pady=15)

    def get_c(self, y, list_1, list_2, list_3, map, user, var):
        final_list = []
        for i in range(y):
            final_list.append((list_1[i], list_2[i], map, user, list_3[i], var[i]))
        self.view.give_many_cart(final_list)


    def list_name(self, my_entries_name):
        list_1=[]
        for entries in my_entries_name:
            list_1.append(entries.get())
        return list_1

    def list_count(self, my_entries_count):
        list_2 = []
        for entries in my_entries_count:
            list_2.append(entries.get())
        return list_2

    def list_application(self, my_entries_application):
        list_3=[]
        for entries in my_entries_application:
            list_3.append(entries.get())
        return list_3

    # def clean(self):
    #     globals.listCart = []
    #     globals.list_1 = []
    #     globals.list_2 = []
    #     globals.list_3 = []


if __name__ == "__main__":
    globals.init_global()
    db.start_object_db()
    db.start_cart_db()
    root = Tk()
    app = Window(root, 0)
    app.pack()
    title = 'Склад'
    root.title(title)
    root.geometry("1000x700+50+50")
    root.resizable(True, True)
    root.mainloop()

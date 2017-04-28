from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Scrollbar
from tkinter.ttk import Treeview
import os
import sqlite3 as sq3
from dbhandling import db_creation
from gui_misc import ManageButtons

"""TODO:
        # поместить приложение в отдельный класс
       
        # автоматически вытаскивать имена из БД далее
        # получить имена таблиц
        curs.execute("select name from sqlite_master where type = 'table'").fetchall()

        
        # получить имена столбцов из таблицы
        curs.execute("pragma table_info(Main)").fetchall()[1]
        
"""
class DbHandler:

    # def table_builder(self, name):
    #     self.tree.delete(*self.tree.get_children())
    #     res_dr = self.curs.execute('pragma table_info(' + name + ');').fetchall()
    #     indexes = tuple(map(lambda x: ''.join(['#', str(x)]),
    #                         range(len(res_dr))))
    #     self.tree['columns'] = indexes
    #     for item in res_dr:
    #         self.tree.column(indexes[item[0]], width=150)
    #         self.tree.heading(indexes[item[0]], text=item[1])
    #
    # def drawing_tree(self):
    #
    #     res = self.curs.execute('''SELECT name FROM sqlite_master
    #                             WHERE TYPE = "table"''').fetchall()
    #     table_names = [item[0] for item in res]
    #
    #     try:
    #         self.table_menu.destroy()
    #     except AttributeError:
    #         pass
    #     else:
    #         self.the_menu.delete(2)
    #
    #     self.table_menu = Menu(self.the_menu, tearoff=0)
    #     for name in table_names:
    #         self.table_menu.add_command(label=name,
    #                                     command=lambda: self.table_builder(name))
    #     self.the_menu.add_cascade(label='Выбор таблицы', menu=self.table_menu)
    def draw(self, event=None):
        name = self.list_box.get(self.list_box.curselection())
        self.tree.delete(*self.tree.get_children())
        res_dr = self.curs.execute('pragma table_info(' + name + ');').fetchall()
        indexes = tuple(map(lambda x: ''.join(['#', str(x)]),
                            range(len(res_dr))))
        self.tree['columns'] = indexes[1:]
        for item in res_dr:
            self.tree.column(indexes[item[0]], width=150)
            self.tree.heading(indexes[item[0]], text=item[1])
        self.tree.pack(fill=BOTH, expand=1)

    def quit_app(self, event=None):
        try:
            self.conn.close()
        except AttributeError:
            pass
        finally:
            ask = messagebox.askyesno('Выход', "Действительно выйти?")
            if ask:
                self.root.destroy()
            return

    def load_bd(self, event=None):
        fn = filedialog.Open(self.root, filetypes=[('*.db files', '.db')]).show()
        if fn == '':
            return
        try:
            self.conn = sq3.connect(fn)
            self.curs = self.conn.cursor()
        except:
            return

    def save_bd(self, event=None):
        try:
            self.conn.commit()
        except AttributeError:
            pass

    def create_db(self, event=None):
        fn = filedialog.SaveAs(self.root, filetypes=[('*.db files', '.db')]).show()
        if fn == '':
            return
        if not fn.endswith('.db'):
            fn += '.db'
        db_creation(fn)
        self.conn = sq3.connect(fn)
        self.curs = self.conn.cursor()

    def set_menu(self):
        self.the_menu = Menu(self.root)
        self.file_menu = Menu(self.the_menu, tearoff=0)
        self.file_menu.add_command(label='Создать', command=self.create_db)
        self.file_menu.add_command(label='Открыть', command=self.load_bd)
        self.file_menu.add_command(label='Сохранить', command=self.save_bd)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Выйти', command=self.quit_app)
        self.the_menu.add_cascade(label='Файл', menu=self.file_menu)
        self.root.config(menu=self.the_menu)

    def set_top_frame(self):
        self.top_frame = Frame(self.root, height=360, bg='gray')
        self.top_frame.pack(side=TOP, fill=BOTH)
        self.tree_scroll = Scrollbar(self.top_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)
        self.tree = Treeview(self.top_frame, yscrollcommand=self.tree_scroll)
        self.tree_scroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        self.tree.pack(fill=BOTH, expand=1)
        self.tree.column('#0', width=798)

    def set_bot_frame(self):
        self.bot_frame = Frame(self.root, height=200, bg='yellow')
        self.bot_frame.pack(side=BOTTOM, fill=BOTH)

    def list_for_select(self):
        try:
            res = self.curs.execute('''SELECT name FROM sqlite_master
                                    WHERE TYPE = "table"''').fetchall()
        except AttributeError:
            return
        else:
            for item in res:
                self.list_box.insert(END, item[0])


    def select_db(self):
        self.form = Toplevel(self.root)
        self.form.minsize(400, 400)
        self.form.title('Выберете БД')
        self.list_box = Listbox(self.form, selectmode=SINGLE)
        self.list_box.pack(side=LEFT, fill=BOTH, expand=1)
        self.list_for_select()
        btn_exit = Button(self.form, text='Закрыть', command=self.form.destroy)
        btn_load = Button(self.form, text='Выбрать', command=self.draw)
        btn_load.pack()
        btn_exit.pack()
        self.form.transient(self.root)
        self.form.grab_set()
        self.root.wait_window(self.form)



    def create_terminal(self):
        ''' Создание дочернего окна
        '''
        pass


    def __init__(self):
        self.root = Tk()
        self.root.title('Blue Mesa')
        self.set_menu()
        self.set_top_frame()
        self.set_bot_frame()
        # buttons = ManageButtons(self.bot_frame, {'insert': self.not_implemented,
        #                                          'update': self.not_implemented,
        #                                          'delete': self.not_implemented,
        #                                          'select': self.not_implemented,
        #                                          'magic': self.create_terminal,
        #                                          })
        buttons = ManageButtons(self.bot_frame, {'select': self.select_db,
                                                 'magic': self.create_terminal
                                                 })
        self.root.mainloop()


if __name__ == '__main__':
    DbHandler()

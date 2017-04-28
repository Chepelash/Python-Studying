import sys
import sqlite3 as sq3


def print_help():
    print("help - получение справки")
    print('select <параметр> <значение> - получение выборки')
    print('delete <параметр> <значение> - удаление значений')
    print('Возможные параметры - operation; date; id; all.')


def db_selecting():
    """Выбор записей
    """
    conn = sq3.connect('main.db')
    curs = conn.cursor()
    if key == 'operation':
        result = curs.execute('SELECT * FROM Main WHERE Operation_type = (?)', (value, )).fetchall()
        for item in result:
            print(item)
    elif key == 'date':
        value += ' 00:00:00'
        result = curs.execute('SELECT * FROM Main WHERE Datetime >= (?)', (value,)).fetchall()
        for item in result:
            print(item)
    elif key == 'id':
        result = curs.execute('SELECT * FROM Main WHERE Id = (?)', (value,)).fetchone()
        print(result)
    elif key == 'all':
        result = curs.execute('SELECT * FROM Main')
        for item in result:
            print(item)
    conn.close()


def db_deleting():
    """Удаление записей из БД
    """
    conn = sq3.connect('main.db')
    curs = conn.cursor()
    if key == 'operation':
        curs.execute('DELETE FROM Main WHERE Operation_type = (?)', (value, )).fetchall()
    elif key == 'date':
        value += ' 00:00:00'
        curs.execute('DELETE FROM Main WHERE Datetime >= (?)', (value,)).fetchall()
    elif key == 'id':
        curs.execute('DELETE FROM Main WHERE Id = (?)', (value,)).fetchone()
    elif key == 'all':
        curs.execute('DELETE FROM Main')

    print('Удаление выполнено')
    conn.close()


do = {
    'help': print_help,
    'select': db_selecting,
    'delete': db_deleting
}

try:
    key = sys.argv[1]
    value = sys.argv[2]
except IndexError:
    key = value = None

if key and value:
    if do.get(key):
        do[key]()
    else:
        print('Задан неверный ключ')
        print("Введите help для получения справки")

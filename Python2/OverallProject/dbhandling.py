import sqlite3 as sq3


def db_selection():
    pass


def db_deleting():
    pass


def data_compression(year, month, day, hours, minutes,
                         seconds, terminal_id, tranzact_num,
                         tranz_type, tranz_data, tranz_info):
    year = str(year)
    month, day, hours, minutes, seconds = map(lambda x: str(x).rjust(2, '0'),
                                              [month, day, hours, minutes, seconds])
    datetime = '{}-{}-{} {}:{}:{}'.format(year, month, day, hours, minutes, seconds)
    if tranz_type == 0:
        operation_type = 'Service'
        money = None
        if tranz_data == 0:
            message = 'Turn on'
        elif tranz_data == 1:
            message = 'Reboot'
        elif tranz_data == 2:
            message = 'Turn off'
        elif tranz_data == 3:
            message = 'Sensor activation'
        elif tranz_data == 4:
            message = 'Blocking'
    elif tranz_type == 1:
        operation_type = 'Withdrawal'
        money = tranz_info
        message = 'Charge-off'
    elif tranz_type == 2:
        operation_type = 'Encashment'
        message = 'Successful job'
        money = tranz_info

    return datetime, operation_type, terminal_id, tranzact_num, message, money


def db_creation(name):
    conn = sq3.connect(name)
    curs = conn.cursor()
    conn.execute('pragma foreign_keys=ON')
    curs.execute("""CREATE TABLE IF NOT EXISTS Main (
    Id INTEGER PRIMARY KEY,
    Datetime DATETIME NOT NULL,
    Operation_type TEXT NOT NULL,
    Terminal_id INTEGER NOT NULL,
    Operation_number INTEGER NOT NULL,
    Message TEXT NOT NULL,
    Money INTEGER
    );
    """)
    curs.execute("""CREATE TABLE IF NOT EXISTS Service_request (
    Id INTEGER PRIMARY KEY,
    Datetime DATETIME NOT NULL,
    Terminal_id INTEGER NOT NULL,
    Operation_number INTEGER NOT NULL,
    Message TEXT NOT NULL    
    );
    """)
    curs.execute("""CREATE TABLE IF NOT EXISTS Partners (
    Id INTEGER PRIMARY KEY,
    Datetime DATETIME NOT NULL,
    Terminal_id INTEGER NOT NULL,
    Money INTEGER NOT NULL
    );
    """)
    curs.execute("""CREATE TABLE IF NOT EXISTS Organizations (
    Id INTEGER PRIMARY KEY,
    Datetime DATETIME NOT NULL,
    Terminal_id INTEGER NOT NULL,
    Money INTEGER NOT NULL    
    );
    """)
    conn.commit()
    conn.close()


def db_filling(data):
    conn = sq3.connect('main.db')
    curs = conn.cursor()
    '''return datetime, operation_type, terminal_id, tranzact_num, message, money'''
    conn.execute('pragma foreign_keys=ON')
    curs.execute('''INSERT INTO Main(Datetime, Operation_type, Terminal_id,
                 Operation_number, Message, Money) VALUES (?, ?, ?, ?, ?, ?);''',
                 (data[0], data[1], data[2], data[3], data[4], data[5]))
    conn.commit()
    if data[1] == 'Service':
        curs.execute('''INSERT INTO Service_request(Datetime, Terminal_id, 
                     Operation_number, Message) VALUES (?, ?, ?, ?);''',
                     (data[0], data[2], data[3], data[4]))
    elif data[1] == 'Withdrawal':
        curs.execute('''INSERT INTO Organizations(Datetime, Terminal_id,
                     Money) VALUES (?, ?, ?);''',
                     (data[0], data[2], data[5]))
    elif data[1] == 'Encashment':
        curs.execute('''INSERT INTO Partners(Datetime, Terminal_id,
                     Money) VALUES (?, ?, ?);''',
                     (data[0], data[2], data[5]))
    conn.commit()


if __name__ == '__main__':
    pass
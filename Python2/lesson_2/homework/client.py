
import socket
from datetime import datetime
import time
import random

__author__ = 'Чепелев Антон'


class Terminals():

    def __init__(self, name):
        self.id = name
        self.operation = 0

    @property
    def tranzaction(self):
        self.operation += 1
        return self.operation


terminals = [Terminals(num) for num in range(128)]
organizations = [num for num in range(16)]


def encoding_protocol(tranz_type, tranz_data, terminal_num, tranz_info=None):
    header = ''.join((hex(ord('z')) * 2).split('0x'))
    timing = datetime.timetuple(datetime.now())
    seconds = timing[3] * 3600 + timing[4] * 60 + timing[5]
    date_info = hex(((timing[0] - 2000) << 9) | (timing[1] << 5) |
                    (timing[2] & 31)).lstrip('0x')

    if not tranz_info:
        tranzact = hex((terminal_num.tranzaction << 30) |
                       (tranz_type << 28) |
                       (terminal_num.id << 21) |
                       (tranz_data << 17) | (seconds & 131071)).lstrip('0x')
        return ''.join([header, date_info, tranzact])
    else:
        tranzact = hex((terminal_num.tranzaction << 38) |
                       (tranz_type << 36) |
                       (terminal_num.id << 29) |
                       (tranz_data << 25) | (seconds << 8) |
                       (tranz_info & 255)).lstrip('0x')
        return ''.join([header, date_info, tranzact])

HOST = 'localhost'
print('Клиент запущен')


while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for port in range(9999, 10000):
        try:
            sock.connect((HOST, port))
        except ConnectionRefusedError:
            pass

    # sec = int(random.random() * 600 + 5)
    sec = 5
    time.sleep(sec)
    terminal = random.choice(terminals)
    action = random.randint(0, 2)
    if action == 0:
        service_type = random.randint(0, 4)
        res_data = encoding_protocol(action, service_type, terminal)
    elif action == 1:
        organiz_id = random.choice(organizations)
        money = random.randint(1, 255)
        res_data = encoding_protocol(action, organiz_id, terminal, money)
    elif action == 2:
        stuff_id = random.randrange(0, 128)
        money = random.randint(1, 255)
        res_data = encoding_protocol(action, stuff_id, terminal, money)

    print(res_data)
    sock.sendall(bytes(res_data, 'ascii'))
    sock.close()

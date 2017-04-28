import socketserver
from dbhandling import *

__author__ = 'Чепелев Антон'


class MemTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).decode('utf-8')
        header = ''.join((hex(ord('z')) * 2).split('0x'))

        print("Клиент {} прислал сообщение".format(self.client_address[0]))
        if self.data[:4] != header:
            return 'Неизвестное сообщение'
        time_data = int(''.join(['0x', self.data[4:8]]), 16)
        year = (time_data & 0xfe00) >> 9
        month = (time_data & 0x1e0) >> 5
        day = time_data & 0x1f
        other_data = int(''.join(['0x', self.data[8:]]), 16)
        if len(bin(other_data)) <= 40:
            terminal_id = (other_data & 0xfe00000) >> 21
            tranzact_num = (other_data & 0x3fc0000000) >> 30
            tranz_type = (other_data & 0x30000000) >> 28
            tranz_data = (other_data & 0x1e0000) >> 17
            time_in_seconds = other_data & 0x1ffff
            tranz_info = None

        else:
            terminal_id = (other_data & 0xfe0000000) >> 29
            tranzact_num = (other_data & 0x3fc000000000) >> 38
            tranz_type = (other_data & 0x3000000000) >> 36
            tranz_data = (other_data & 0x1e000000) >> 25
            time_in_seconds = (other_data & 0x1ffff00) >> 8
            tranz_info = (other_data & 255) * 100

        hours = time_in_seconds // 3600
        minutes = time_in_seconds // 60 - hours * 60
        seconds = time_in_seconds % 60
        db_filling(data_compression(year, month, day, hours, minutes,
                                    seconds, terminal_id, tranzact_num,
                                    tranz_type, tranz_data, tranz_info))


HOST, PORT = 'localhost', 9999

db_creation('main.db')
server = socketserver.TCPServer((HOST, PORT), MemTCPHandler)
print('Сервер запущен')

server.serve_forever()

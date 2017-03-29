# Задание-1:
# Доработайте реализацию программы из примера examples/5_with_args.py,
# добавив реализацию следующих команд (переданных в качестве аргументов):
#   cp <file_name> - создает копию указанного файла
#   rm <file_name> - удаляет указанный файл (запросить подтверждение операции)
#   cd <full_path or relative_path> - меняет текущую директорию на указанную
#   ls - отображение полного пути текущей директории
# путь считать абсолютным (full_path) -
# в Linux начинается с /, в Windows с имени диска,
# все остальные пути считать относительными.

# Важно! Все операции должны выполняться в той директории, в который вы находитесь.
# Исходной директорией считать ту, в которой был запущен скрипт.

# P.S. По возможности, сделайте кросс-платформенную реализацию.

import os
import sys
import shutil

print('sys.argv = ', sys.argv)


def print_help():
    print("help - получение справки")
    print("mkdir <dir_name> - создание директории")
    print("ping - тестовый ключ")
    print("cp <file_name> - создает копию указанного файла")
    print("rm <file_name> - удаляет указанный файл (запросить подтверждение операции)")
    print("cd <full_path or relative_path> - меняет текущую директорию на указанную")
    print("ls - отображение полного пути текущей директории")


def cp():
    if not dir_name:
        print("Необходимо указать имя директории или файла вторым параметром")
        return
    dir_path = os.path.join(os.getcwd(), dir_name)
    try:
        shutil.copy(dir_path)
        print('Копирование {} успешно'.format(dir_name))
    except (FileExistsError, IOError, PermissionError):
        print('Копирование не удалось')


def rm():
    if not dir_name:
        print("Необходимо указать имя директории или файла вторым параметром")
        return
    dir_path = os.path.join(os.getcwd(), dir_name)
    try:
        os.remove(dir_path)
        print('Удаление {} успешно'.format(dir_name))
    except (PermissionError, OSError):
        print('Удаление не удалось')


def cd():
    if not dir_name:
        print("Необходимо указать имя директории вторым параметром")
        return
    dir_path = os.path.join(os.getcwd(), dir_name)
    try:
        os.chdir(dir_path)
        print('Переход успешен')
    except (FileNotFoundError, NotADirectoryError):
        print('Переход не удался')


def ls():
    path = os.path.join(os.getcwd())
    norm = os.path.normcase(path)
    print(norm)


def make_dir():
    if not dir_name:
        print("Необходимо указать имя директории вторым параметром")
        return
    dir_path = os.path.join(os.getcwd(), dir_name)
    try:
        os.mkdir(dir_path)
        print('директория {} создана'.format(dir_name))
    except FileExistsError:
        print('директория {} уже существует'.format(dir_name))


def ping():
    print("pong")

do = {
    "help": print_help,
    "mkdir": make_dir,
    "ping": ping,
    'cp': cp,
    'rm': rm,
    'cd': cd,
    'ls': ls
}

try:
    dir_name = sys.argv[2]
except IndexError:
    dir_name = None

try:
    key = sys.argv[1]
except IndexError:
    key = None


if key:
    if do.get(key):
        do[key]()
    else:
        print("Задан неверный ключ")
        print("Укажите ключ help для получения справки")


import os
import sys
import shutil


# Задача-1:
# Напишите скрипт, создающий директории dir_1 - dir_9 в папке,
# из которой запущен данный скрипт.
# И второй скрипт, удаляющий эти папки.
def creation():
    for i in range(1, 10):
        path = os.path.join(os.getcwd(), 'dir_{}'.format(i))
        try:
            os.mkdir(path=path)
        except FileExistsError:
            print("Директория уже существует")


def deleting():
    dir_lst = os.listdir('.')
    for item in dir_lst:
        if item.startswith("dir_"):
            path = os.path.join(os.getcwd(), item)
            os.rmdir(path)


# Задача-2:
# Напишите скрипт, отображающий папки текущей директории.
def show():
    dir_lst = os.listdir('.')
    for item in dir_lst:
        print(item, end="; ")


# Задача-3:
# Напишите скрипт, создающий копию файла, из которого запущен данный скрипт.
def copy():
    file = sys.argv[0]
    try:
        shutil.copy(file, "copy.py")
    except IOError:
        print("Ошибка копирования")
    except:
        print("Странная ошибка")
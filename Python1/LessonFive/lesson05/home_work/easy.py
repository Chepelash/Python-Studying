import os


def dirlist():
    for item in os.listdir('.'):
        print(item, end="; ")
    print()


def cd(path):
    way = os.path.join(os.getcwd(), path)
    try:
        os.chdir(way)
        print('Успешно перешли')
    except FileNotFoundError:
        print('Невозможно перейти')


def deldir(dirname):
    path = os.path.join(os.getcwd(), dirname)
    try:
        os.rmdir(path)
        print('Успешно удалено')
    except (FileNotFoundError, PermissionError, OSError):
        print('Невозможно удалить папку')


def createdir(dirname):
    path = os.path.join(os.getcwd(), dirname)
    try:
        os.mkdir(path)
        print("Успешно создано")
    except FileExistsError:
        print("Невозможно создать")


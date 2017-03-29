import os

__author__ = "Чепелев Антон"


# Задание-1: Решите задачу (дублированную ниже):

# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы,
# то их ЗП уменьшается пропорционально, а за заждый час переработки
# они получают удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"

# С использованием классов.
# Реализуйте классы сотрудников так, чтобы на вход функции-конструктора
# каждый работник получал строку из файла


class Worker():

    def __init__(self, name, surname, wage, job, norm_hours, worked_hours=0):
        self.name = name
        self.surname = surname
        self.wage = int(wage)
        self.job = job
        self.norm_hours = int(norm_hours)
        self.worked_hours = worked_hours

    @property
    def get_payment(self):
        if self.worked_hours == self.norm_hours:
            return self.wage
        elif self.worked_hours > self.norm_hours:
            return self.wage + 2 * self.wage / self.norm_hours
        else:
            return self.wage - self.wage / self.norm_hours


employees = []
path = os.path.join('data', 'workers')
with open(path, 'r', encoding="UTF-8") as f:
    f.readline()
    for line in f:
        info = line.split()
        employees.append(Worker(info[0], info[1], info[2], info[3], info[4]))

path = os.path.join('data', 'hours_of')
with open(path, 'r', encoding='UTF-8') as f:
    f.readline()
    for line in f:
        info = line.split()
        for employee in employees:
            if employee.name == info[0] and employee.surname == info[1]:
                employee.worked_hours = int(info[2])

for employee in employees:
    print('ЗП у работника {} {} составила {} руб.'.format(employee.name,
                                                          employee.surname,
                                                          employee.get_payment))

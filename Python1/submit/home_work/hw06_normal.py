
__author__ = "Чепелев Антон"

# Задание-1:
# Реализуйте описаную ниже задачу, используя парадигмы ООП:
# В школе есть Классы(5А, 7Б и т.д.), в которых учатся Ученики.
# У каждого ученика есть два Родителя(мама и папа).
# Также в школе преподают Учителя. Один учитель может преподавать 
# в неограниченном кол-ве классов свой определенный предмет. 
# Т.е. Учитель Иванов может преподавать математику у 5А и 6Б,
# но больше математику не может преподавать никто другой.

# Выбранная и заполненная данными структура должна решать следующие задачи:
# 1. Получить полный список всех классов школы
# 2. Получить список всех учеников в указанном классе
#  (каждый ученик отображается в формате "Фамилия И.О.")
# 3. Получить список всех предметов указанного ученика 
#  (Ученик --> Класс --> Учителя --> Предметы)
# 4. Узнать ФИО родителей указанного ученика
# 5. Получить список всех Учителей, преподающих в указанном классе

# Подсказка: обратите внимание на примеры в директории examples.


class People:
    def __init__(self, name, surname, birth_date, school):
        self.name = name
        self.surname = surname
        self.birth_date = birth_date
        self.school = school

    def get_full_name(self):
        return self.name + ' ' + self.surname

    def set_name(self, new_name):
        self.name = new_name


class Student(People):
    class_dict = {}

    def __init__(self, name, surname, birth_date, school, class_room,
                 dad_name, mom_name, study):
        People.__init__(self, name, surname, birth_date, school)
        self._class_room = {'class_num': int(class_room.split()[0]),
                            'class_char': class_room.split()[1]}
        self.dad_name = dad_name
        self.mom_name = mom_name
        self.study = set(study.split(", "))
        if self.class_room not in Student.class_dict.keys():
            Student.class_dict.update({self.class_room: ['{} {}.'.format(self.surname, self.name[0])]})
        else:
            Student.class_dict[self.class_room].append('{} {}.'.format(self.surname, self.name[0]))

    @property
    def get_parents(self):
        return 'Отец - {}, Мать - {}'.format(self.dad_name, self.mom_name)

    @property
    def class_room(self):
        return "{} {}".format(self._class_room['class_num'], self._class_room['class_char'])

    def add_study(self, study):
        self.study.add(study.split(", "))

    @property
    def get_study(self):
        return str(self.study).strip('{}')

    def next_class(self):
        self._class_room['class_num'] += 1


class Teacher(People):
    dict_teacher = {}

    def __init__(self, name, surname, birth_date, school, teach_classes, study):
        People.__init__(self, name, surname, birth_date, school)
        self.teach_classes = list(teach_classes.split(', '))
        self.__study = study
        for classes in self.teach_classes:
            if classes not in Teacher.dict_teacher.keys():
                Teacher.dict_teacher.update({classes: ['{} {}.'.format(self.surname,
                                                                      self.name[0])]})
            else:
                Teacher.dict_teacher[classes].append('{} {}.'.format(self.surname,
                                                                     self.name[0]))


vasa = Student('Сванте', "Свантенсон", 1965, '345', '3 В',
               "Герр Свантесон", "Фрау Свантесон", "математика, немецкий")
mari = Teacher("Марь", "Иванна", 1934, "345", "3 В", "математика")


# 1. Получить полный список всех классов школы
def get_classes():
    if Student.class_dict:
        return ', '.join(Student.class_dict.keys())
    else:
        return 'Пока никто не учится'


print('Список классов - {}'.format(get_classes()))


# 2. Получить список всех учеников в указанном классе
#  (каждый ученик отображается в формате "Фамилия И.О.")
def get_pupils(class_room):
    if class_room in Student.class_dict.keys():
        return ", ".join(Student.class_dict[class_room])
    else:
        return "Нет такого класса"


print('Ученики в классе {} - {}'.format('3 В', get_pupils('3 В')))

# 3. Получить список всех предметов указанного ученика
#  (Ученик --> Класс --> Учителя --> Предметы)
print('Предметы - {}'.format(vasa.get_study))

# 4. Узнать ФИО родителей указанного ученика
print(vasa.get_parents)


# 5. Получить список всех Учителей, преподающих в указанном классе
def get_teachers(class_room):
    if class_room in Teacher.dict_teacher.keys():
        return ", ".join(Teacher.dict_teacher[class_room])
    else:
        return "Никто не учит этот класс"


print("Учителя в классе {} - {}".format('3 В', get_teachers('3 В')))

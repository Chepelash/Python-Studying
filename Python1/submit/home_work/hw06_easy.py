import math

__author__ = "Чепелев Антон"


# Задача-1: Написать класс для фигуры-треугольника,
# заданного координатами трех точек.
# Определить методы, позволяющие вычислить: площадь, высоту и периметр фигуры.
class Triangle():
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.__len_a = math.sqrt((self.a[0] - self.b[0]) ** 2 +
                                 (self.a[1] - self.b[1]) ** 2)
        self.__len_b = math.sqrt((self.b[0] - self.c[0]) ** 2 +
                                 (self.b[1] - self.c[1]) ** 2)
        self.__len_c = math.sqrt((self.a[0] - self.c[0]) ** 2 +
                                 (self.a[1] - self.c[1]) ** 2)
        self.__p = (self.__len_a + self.__len_b + self.__len_c) / 2

    def square(self):
        return math.sqrt(self.__p * (self.__p - self.__len_a) *
                         (self.__p - self.__len_b) *
                         (self.__p - self.__len_c))

    def height_a(self):
        return 2 / self.__len_a * self.square()

    def height_b(self):
        return 2 / self.__len_b * self.square()

    def height_c(self):
        return 2 / self.__len_c * self.square()

    def perimeter(self):
        return self.__len_a + self.__len_b + self.__len_c


# Пример использования класса треугольника:
tr_1 = Triangle((1, 2), (7, 9), (5, 0))
print(tr_1)
print('Площадь:', tr_1.square())
print('Высота к стороне a:', tr_1.height_a())
print('Высота к стороне b:', tr_1.height_b())
print('Высота к стороне c:', tr_1.height_c())
print('Периметр:', tr_1.perimeter())


# Задача-2: Написать Класс "Равнобочная трапеция", заданной координатами 4-х точек.
# Предусмотреть в классе методы для:
#  - проверки, является ли фигура равнобочной трапецией;
#  - вычисления: длины сторон, периметр, площадь.
class Trapezoid():
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.__len_a = math.sqrt((self.a[0] - self.b[0]) ** 2 +
                                 (self.a[1] - self.b[1]) ** 2)
        self.__len_b = math.sqrt((self.b[0] - self.c[0]) ** 2 +
                                 (self.b[1] - self.c[1]) ** 2)
        self.__len_c = math.sqrt((self.d[0] - self.c[0]) ** 2 +
                                 (self.d[1] - self.c[1]) ** 2)
        self.__len_d = math.sqrt((self.a[0] - self.d[0]) ** 2 +
                                 (self.a[1] - self.d[1]) ** 2)

    def is_isosceles(self):
        if self.__len_a == self.__len_c:
            return True
        else:
            return False

    def sides(self):
        return self.__len_a, self.__len_b, self.__len_c, self.__len_d

    def square(self):
        t_1 = (self.__len_b + self.__len_d) / 2
        t_2 = self.__len_d - self.__len_b
        return t_1 * math.sqrt(self.__len_a ** 2 *
                               ((t_2 ** 2 + self.__len_a ** 2 -
                                 self.__len_c ** 2) / (2 * t_2)) ** 2)

    def perimeter(self):
        return self.__len_b + self.__len_a + self.__len_c + self.__len_d


# Пример использования класса трапеции:
trap_1 = Trapezoid((0, 0), (1, 2), (3, 2), (4, 0))
trap_2 = Trapezoid((0, 0), (1, 2), (3, 2), (6, 0))
traps = [trap_1, trap_2]

for trap in traps:
    print(trap)
    if trap.is_isosceles():
        print('Равнобочная')
    else:
        print('Неравнобочная')
    print('Длины сторон:', trap.sides())
    print('Площадь:', trap.square())
    print('Периметр:', trap.perimeter())

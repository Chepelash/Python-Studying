# -*- coding: utf-8 -*-

__authtor__ = 'Чепелев Антон'

"""
Это пример небольшой программы для рисования кругов и квадратов.
Вам нужно на основе этой программы сделать небольшую "танцевальную" сценку с
использованием кругов, квардратов и треугольников. Сделать всё это нужно в
объектно ориентированном стиле.

Какие классы нужно реализовать:

-Многоугольник(на его основе сделать квадрат и правильный треугольник)
--класс должен уметь отрисовывать себя
--перемещаться в некоторм направлении, заданом координатами x, y
--увеличивать(необязательно)
--поворачивать(необязательно)

-Квардрат(наследуется от многоугольника)
--метод __init__ принимает координаты середины, ширину и цвет

-Треугольник(наследуется от многоугольника)
--метод __init__ принимает координаты середины, длинну грани и цвет

-Круг
--метод __init__ принимает координаты середины, радиус и цвет
--класс должен уметь отрисовывать себя
--премещаться в некоторм направлении, заданом координатами x, y
--увеличивать(необязательно)

Также рекомендуется создать вспомогательный сласс Vector для представления
точек на плоскости и различных операций с ними - сложение, умножение на число,
вычитание.


Из получившихся классов нужно составить какую-нибудь динамическую сцену.
Смотрите пример example.gif
"""

import turtle
import time
import random
import math

"""Я пытался, но никогда не любил геометрию
"""

class Polygon():

    def __init__(self, center, width, color):
        self.width = width
        self.x = center[0]
        self.y = center[1]
        self.color = color

    def spin(self, ttl):
        ttl.left(25)


class Rectangle(Polygon):

    def __init__(self, center, width, color):
        Polygon.__init__(self, center, width, color)

    def draw_rect(self, ttl):
        x = self.x  # получаем случайные координаты
        y = self.y

        ttl.color(self.color)  # устанавливаем цвет линии
        ttl.penup()  # убираем "ручку" от холста, чтобы переместить в нужное место
        ttl.setpos(int(x - self.width / 2), int(y - self.width / 2))  # перемещаем на первую вершину
        ttl.pendown()  # опускаем ручку обратно
        for _ in range(4):
            ttl.forward(self.width)  # проводим линии для сторон четырёхугольника
            ttl.left(90)


class Triangle(Polygon):

    def __init__(self, center, width, color):
        Polygon.__init__(self, center, width, color)

    def draw_trng(self, ttl):
        x = self.x  # получаем случайные координаты
        y = self.y

        ttl.color(self.color)  # устанавливаем цвет линии
        ttl.penup()  # убираем "ручку" от холста, чтобы переместить в нужное место
        ttl.setpos(x, y)  # перемещаем на первую вершину
        ttl.pendown()  # опускаем ручку обратно
        for _ in range(3):
            ttl.forward(self.width)  # проводим линии для сторон четырёхугольника
            ttl.right(120)


# -Круг
# --метод __init__ принимает координаты середины, радиус и цвет
# --класс должен уметь отрисовывать себя
# --премещаться в некоторм направлении, заданом координатами x, y
# --увеличивать(необязательно)

class Circle(Polygon):

    def __init__(self, center, rad, color, width=0):
        Polygon.__init__(self, center, width, color)
        self.rad = rad

    def draw_crcl(self, ttl):
        x = self.x  # получаем случайные координаты
        y = self.y
        ttl.color(self.color)     # устанавливаем цвет линии
        ttl.penup()             # убираем "ручку" от холста, чтобы переместить в нужное место
        ttl.setpos(x, y)        # перемещаем в "основание" - это будет самая низкая точка
        ttl.pendown()           # опускаем ручку обратно
        ttl.circle(self.rad)          # рисуем круг радиуса 25


def main():
    turtle.tracer(0, 0)  # устанавливаем все задержки в 0, чтобы рисовалось мгновенно
    turtle.hideturtle()  # убираем точку посередине

    ttl = turtle.Turtle()  # создаём объект черепашки для рисования
    ttl.hideturtle()  # делаем её невидимой

    rec = Rectangle((0, 0), 250, 'red')
    circ = Circle((0, -50), 50, 'violet')
    tr1 = Triangle((-275, -250), 25, 'orange')
    circ1 = Circle((-230, -275), 16, 'green')
    tr2 = Triangle((-210, -255), 25, 'orange')
    tr3 = Triangle((250, 250), 25, 'orange')
    circ2 = Circle((230, 225), 16, 'green')
    tr4 = Triangle((185, 255), 25, 'orange')

    while True:
        time.sleep(0.5) # засыпаем на полсекунды, чтобы увидеть что нарисовали
        ttl.clear()     # очищаем всё нарисованое ранее
        rec.draw_rect(ttl)
        tr1.draw_trng(ttl)
        tr2.draw_trng(ttl)
        circ1.draw_crcl(ttl)
        circ.draw_crcl(ttl)
        tr4.draw_trng(ttl)
        tr3.draw_trng(ttl)
        circ2.draw_crcl(ttl)
        rec.spin(ttl)
        circ.spin(ttl)
        tr1.spin(ttl)
        circ1.spin(ttl)
        tr2.spin(ttl)
        tr3.spin(ttl)
        circ2.spin(ttl)
        tr4.spin(ttl)

        turtle.update()  # т.к. мы сделали turtle.tracer(0, 0), нужно обновить экран, чтобы увидеть нарисованное


if __name__ == '__main__':
    main()

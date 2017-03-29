
__author__ = "Чепелев Антон"


# Задание-1:
# Напишите функцию, возвращающую ряд Фибоначчи с n-элемента до m-элемента.
# Первыми элементами ряда считать цифры 1 1
def fibonacci(n, m):
    fib1 = 1
    fib2 = 1
    lst = [0, 1, 1]
    for i in range(2, m):
        lst.append(fib1 + fib2)
        fib1, fib2 = fib2, fib1 + fib2
    return lst[n:m]


# Задача-2:
# Напишите функцию, сортирующую принимаемый список по возрастанию.
# Для сортировки используйте любой алгоритм (например пузырьковый).
# Для решения данной задачи нельзя использовать встроенную функцию и метод sort()
def sort_to_max(origin_list):
    x = len(origin_list) - 1
    while x:
        for i in range(len(origin_list)-1):
            if origin_list[i] > origin_list[i + 1]:
                origin_list[i], origin_list[i + 1] = \
                    origin_list[i + 1], origin_list[i]
        x -= 1
    return origin_list

sort_to_max([2, 10, -12, 2.5, 20, -11, 4, 4, 0])


# Задача-3:
# Напишите собственную реализацию стандартной функции filter.
# Разумеется, внутри нельзя использовать саму функцию filter.
def not_filter(func, nums):
    lst = [x for x in nums if func(x)]
    return lst


# Задача-4:
# Даны четыре точки А1(х1, у1), А2(x2 ,у2), А3(x3 , у3), А4(х4, у4).
# Определить, будут ли они вершинами параллелограмма.
def checking(x1, x2, x3, x4, y1, y2, y3, y4):
    if y1 == y4 and y2 == y3 and abs(x1 - x2) == abs(x3 - x4):
        return True
    return False

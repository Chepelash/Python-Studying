import random

__author__ = "Чепелев Антон"

# Все задачи текущего блока решите с помощью генераторов списков!


# Задание-1:
# Дан список, заполненный произвольными целыми числами. 
# Получить новый список, элементы которого будут
# квадратами элементов исходного списка
# [1, 2, 4, 0] --> [1, 4, 16, 0]
lst = [random.randint(-50, 50) for i in range(100)]
new_lst = [nums ** 2 for nums in lst]


# Задание-2:
# Даны два списка фруктов.
# Получить список фруктов, присутствующих в обоих исходных списках.
lst1 = ['яблоко', 'апельсин', 'груша', 'банан']
lst2 = ['банан', "киви", "мандарин", "авокадо", "яблоко"]
resLst = [word for word in lst1 if word in lst2]


# Задание-3:
# Дан список, заполненный произвольными числами.
# Получить список из элементов исходного, удовлетворяющих следующим условиям:
# + Элемент кратен 3
# + Элемент положительный
# + Элемент не кратен 4
lst3 = [num for num in lst if not num % 3 and num >= 0 and num % 4]

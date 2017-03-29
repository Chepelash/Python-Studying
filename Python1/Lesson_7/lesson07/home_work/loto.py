#!/usr/bin/python3

import random
import sys

"""
== Лото ==

Правила игры в лото.

Игра ведется с помощью специальных карточек, на которых отмечены числа, 
и фишек (бочонков) с цифрами.

Количество бочонков — 90 штук (с цифрами от 1 до 90).

Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр, 
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:

--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86 
--------------------------

В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается 
случайная карточка. 

Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.
	
Побеждает тот, кто первый закроет все числа на своей карточке.

Пример одного хода:

Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71   
--------------------------
-- Карточка компьютера ---
 7 87     - 14    11      
      16 49    55 88    77    
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)

Подсказка: каждый следующий случайный бочонок из мешка удобно получать 
с помощью функции-генератора.

Подсказка: для работы с псевдослучайными числами удобно использовать 
модуль random: http://docs.python.org/3/library/random.html

"""


class Card():

    def __init__(self, name='Компьютер'):
        if name == 'Компьютер':
            self.__mode = ' Карточка компьютера '
        elif not name.isalpha():
            raise SyntaxError
        else:
            self.__mode = ' Ваша карточка '

        self.__lotto_card = set()
        while len(self.__lotto_card) <= 14:
            self.__lotto_card.add(random.randint(1, 90))

        self.__lotto_list = list(map(str, sorted(self.__lotto_card)))

        for i in range(12):
            self.__lotto_list.insert(random.randrange(0, len(self.__lotto_list)), '__')

    def __str__(self):
        return '{:-^27}\n{:^27}\n{:^27}\n{:^27}\n' \
               '{:-^27}\n'.format(self.__mode,
                                  ' '.join(self.__lotto_list[::3]),
                                  ' '.join(self.__lotto_list[1::3]),
                                  ' '.join(self.__lotto_list[2::3]),
                                  '')

    def pop_item(self, item):
        try:
            self.__lotto_card.remove(int(item))
        except KeyError:
            print('Такого числа нет в вашей карте')
            print('Вы проиграли')
            sys.exit()

        ind = self.__lotto_list.index(item)
        self.__lotto_list[ind] = '--'

        if not self.__lotto_card:
            print('Все числа закрыты')
            if self.__mode == ' Карточка компьютера ':
                print("Компьютер победил!")
            else:
                print('Вы победили!')
            sys.exit()

    @property
    def get_set(self):
        return self.__lotto_card


rand_lst = [i for i in range(1, 91)]
random.shuffle(rand_lst)
numb_generator = iter(rand_lst)


if __name__ == '__main__':
    name = input('Ваше имя?\n>>> ')
    player = Card(name)
    ai = Card()
    counter = 90
    while counter > 0:
        counter -= 1
        print()
        print(player)
        print(ai)
        num = next(numb_generator)
        print('Новый бочонок: {} (осталось {})'.format(num, counter))
        while True:
            us_choice = input('Зачеркнуть цифру? (y/n); q - выход из игры\n>>> ')
            if us_choice.lower().strip() == 'y':
                player.pop_item(str(num))
                if num in ai.get_set:
                    ai.pop_item(str(num))
                break
            elif us_choice.lower().strip() == 'n':
                if num in ai.get_set:
                    ai.pop_item(str(num))
                break
            elif us_choice.lower().strip() == 'q':
                print('Выход из игры')
                sys.exit()
            else:
                print('Непонятный ввод')

    print('Кончились бочонки')

import urllib.request
import os
import sys
import gzip
import json
import sqlite3
import re

""" 
== OpenWeatherMap ==

OpenWeatherMap — онлайн-сервис, который предоставляет бесплатный API
 для доступа к данным о текущей погоде, прогнозам, для web-сервисов
 и мобильных приложений. Архивные данные доступны только на коммерческой основе.
 В качестве источника данных используются официальные метеорологические службы
 данные из метеостанций аэропортов, и данные с частных метеостанций.

Необходимо решить следующие задачи:

== Получение APPID ==
    Чтобы получать данные о погоде необходимо получить бесплатный APPID.
    
    Предлагается 2 варианта (по желанию):
    - получить APPID вручную
    - автоматизировать процесс получения APPID, 
      используя дополнительную библиотеку Grab (pip install grab)
            (или любую другую - BeautifulSoup/Scrapy)

            Для установки Grab под Windows следуйте инструкциям:
            http://docs.grablib.org/ru/latest/grab/installation.html


        Необходимо зарегистрироваться на сайте openweathermap.org:
        https://home.openweathermap.org/users/sign_up

        Войти на сайт по ссылке:
        https://home.openweathermap.org/users/sign_in

        Свой ключ "вытащить" со страницы отсюда:
        https://home.openweathermap.org/api_keys
        
        Ключ имеет смысл сохранить в локальный файл, например, "app.id"

        
== Получение списка городов ==
    Список городов может быть получен по ссылке:
    http://bulk.openweathermap.org/sample/city.list.json.gz
    
    Далее снова есть несколько вариантов (по желанию):
    - скачать и распаковать список вручную
    - автоматизировать скачивание (ulrlib) и распаковку списка 
     (воспользоваться модулем gzip 
      или распаковать внешним архиватором, воспользовавшись модулем subprocess)
    
    Список достаточно большой. Представляет собой JSON-строки:
{"_id":707860,"name":"Hurzuf","country":"UA","coord":{"lon":34.283333,"lat":44.549999}}
{"_id":519188,"name":"Novinki","country":"RU","coord":{"lon":37.666668,"lat":55.683334}}
    
    
== Получение погоды ==
    На основе списка городов можно делать запрос к сервису по id города. И тут как раз понадобится APPID.
        By city ID
        Examples of API calls:
        http://api.openweathermap.org/data/2.5/weather?id=2172797&appid=b1b15e88fa797225412429c1c50c122a

    Для получения температуры по Цельсию:
    http://api.openweathermap.org/data/2.5/weather?id=520068&units=metric&appid=b1b15e88fa797225412429c1c50c122a

    Для запроса по нескольким городам сразу:
    http://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743&units=metric&appid=b1b15e88fa797225412429c1c50c122a


    Данные о погоде выдаются в JSON-формате
    {"coord":{"lon":38.44,"lat":55.87},
    "weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],
    "base":"cmc stations","main":{"temp":280.03,"pressure":1006,"humidity":83,
    "temp_min":273.15,"temp_max":284.55},"wind":{"speed":3.08,"deg":265,"gust":7.2},
    "rain":{"3h":0.015},"clouds":{"all":76},"dt":1465156452,
    "sys":{"type":3,"id":57233,"message":0.0024,"country":"RU","sunrise":1465087473,
    "sunset":1465149961},"id":520068,"name":"Noginsk","cod":200}    


== Сохранение данных в локальную БД ==    
Программа должна позволять:
1. Создавать файл базы данных SQLite со следующей структурой данных
   (если файла базы данных не существует):

    Погода
        id_города           INTEGER PRIMARY KEY
        Город               VARCHAR(255)
        Дата                DATE
        Температура         INTEGER
        id_погоды           INTEGER                 # weather.id из JSON-данных

2. Выводить список стран из файла и предлагать пользователю выбрать страну 
(ввиду того, что список городов и стран весьма велик
 имеет смысл запрашивать у пользователя имя города или страны
 и искать данные в списке доступных городов/стран (регуляркой))

3. Скачивать JSON (XML) файлы погоды в городах выбранной страны
4. Парсить последовательно каждый из файлов и добавлять данные о погоде в базу
   данных. Если данные для данного города и данного дня есть в базе - обновить
   температуру в существующей записи.


При повторном запуске скрипта:
- используется уже скачанный файл с городами;
- используется созданная база данных, новые данные добавляются и обновляются.


При работе с XML-файлами:

Доступ к данным в XML-файлах происходит через пространство имен:
<forecast ... xmlns="http://weather.yandex.ru/forecast ...>

Чтобы работать с пространствами имен удобно пользоваться такими функциями:

    # Получим пространство имен из первого тега:
    def gen_ns(tag):
        if tag.startswith('{'):
            ns, tag = tag.split('}')
            return ns[1:]
        else:
            return ''

    tree = ET.parse(f)
    root = tree.getroot()

    # Определим словарь с namespace
    namespaces = {'ns': gen_ns(root.tag)}

    # Ищем по дереву тегов
    for day in root.iterfind('ns:day', namespaces=namespaces):
        ...

"""


def preparations():
    """Подготовка к работе программы:
    получение ключей, имен городов, создание или проверка базы данных
    """
    # Getting APPID
    appid_key = open('app.id').read().strip()

    # Downloading city names
    url = 'http://bulk.openweathermap.org/sample/city.list.json.gz'
    try:
        os.stat('data')
    except FileNotFoundError:
        os.mkdir('data')

    out = os.path.join('data', 'city.list.json.gz')

    try:
        os.stat(out)
    except FileNotFoundError:
        urllib.request.urlretrieve(url, out)

    # Unzipping city names
    cities = gzip.open(out, 'rb').read().decode()

    # List of dictionaries with cities' info
    city_names = [json.loads(line) for line in cities.split('\n')[:-1]]

    # DB creation and filling in
    path_db = os.path.join('data', 'weather.db')

    # DB existence checking
    try:
        os.stat(path_db)
    except FileNotFoundError:
        with sqlite3.connect(path_db) as conn:
                curs = conn.cursor()
                curs.execute("""
                             CREATE TABLE Weather (
                             City_id INTEGER PRIMARY KEY,
                             City_name VARCHAR(255),
                             Date DATE,
                             Temperature INTEGER,
                             Weather_id INTEGER
                             );
                             """)
    return appid_key, city_names
# Filling in DB if it's not existing
# def db_filling(path, data):
#     with sqlite3.connect(path) as conn:
#         curs = conn.cursor()
#         curs.execute("""
#                      CREATE TABLE Weather (
#                      City Name TEXT PRIMARY KEY,
#                      Coordinates BLOB,
#                      ID INTEGER PRIMARY KEY,
#                      Country TEXT,
#                      );
#                      """)
#         curs.executemany("INSERT INTO Weather VALUES (?, ?, ?, ?)", data)


def weatherrequest(name, unit):
    """Запрос погоды по Id города
    Получение данных в формате JSON и обработка
    """
    for num in range(len(cityNames)):
        if name == cityNames[num]['name']:
            city_id = 'id=' + str(cityNames[num]['_id'])
    metr = 'units=' + unit
    final_url = 'http://api.openweathermap.org/data/2.5/weather?' + city_id + \
                metr + '&lang=ru&appid=' + appid
    webdata = urllib.request.urlopen(final_url)
    # encoding = webdata.info().get_content_charset('utf-8')
    weatherdata = json.loads(webdata)
    return weatherdata




if __name__ == '__main__':
    while True:
        start = input('Начнём работу? (y\\n)\n>>> ').lower()
        if start == 'y':
            print('Загрузка...')
            appid, cityNames = preparations()
            break
        elif start == 'n':
            sys.exit()
        else:
            print("Непонятный ввод")

    while True:
        metric = input('Температура в Цельсиях или Фаренгейтах? (C\F)\n>>> ').lower()
        if metric == 'c':
            units = 'metric'
            break
        elif metric == 'f':
            units = 'imperial'
            break
        else:
            print('Нет других метрик')

    while True:
        weatherdata = None
        cityName = input('Введите название города: ').title()
        if cityName == 'Exit':
            sys.exit()
        catches = []
        for line in cityNames:
            if cityName == line['name']:
                weatherdata = weatherrequest(cityName, units)
                break
            elif line['name'].startswith(cityName[:int(len(cityName) / 1.5)]):
                catches.append(line['name'])
        if weatherdata is not None:
            break
        print("Уточните название")
        if len(catches):
            print("Возможные варианты:")
            print('\n'.join(catches))
        else:
            print('не обнаружено совпадений')

    conn = sqlite3.connect(os.path.join('data', 'weather.db'))
    curs = conn.cursor()
    curs.execute('INSERT INTO Weather '
                 'VALUES ({}, {}, {}, {}, {})'.format(weatherdata['id'],
                                                      weatherdata['name'],
                                                      weatherdata['dt'],
                                                      weatherdata['main']['temp'],
                                                      weatherdata['weather']['id']))
    conn.commit()
    res = curs.execute('SELECT * FROM Weather')
    res.fetchall()
    conn.close()





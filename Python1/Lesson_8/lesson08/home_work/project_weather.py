
import os
import sys
import re
import multiprocessing as mp
import pprint
import gzip
import json
import urllib.request
import grab


def connect(url, grabber):
    """Авторизация на сайте и получения apid ключа для запроса
    """
    grabber.go(url)
    grabber.doc.set_input('user[email]', 'weather_zora@mail.ru')
    grabber.doc.set_input('user[password]', 'Simple_Weather')
    grabber.doc.submit()
    page = gr.doc.unicode_body()
    success = re.search(r"(?<=<div class='panel-body'>)(.*)(?=</div>)", page)
    if 'success' not in success.group(0):
        sys.exit(1)

    grabber.go('https://home.openweathermap.org/api_keys')
    page = gr.doc.unicode_body()
    apid_key = re.search(r"(?<=<pre>)(.*)(?=</pre>)", page).group(0)

    return apid_key


def get_cities(queue):
    """Скачивание словаря с названиями городов
    """
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
    names = [json.loads(line) for line in cities.split('\n')[:-1]]
    queue.put(names)


def get_weather_data(grabber, city_id, apid_key):
    """Получение и вывод данных о погоде
    """

    def printing(data):
        """Вывод погоды в красивом виде
        """
        print('{:-^30}'.format('Погода сегодня'))
        print('Температура: {}'.format(data['main']['temp']))
        print('Условия: {}'.format(data['weather'][0]['description']))
        print('Давление: {}'.format(data['main']['pressure']))
        print('Влажность : {}'.format(data['main']['humidity']))


    url = ('http://api.openweathermap.org/data/2.5/weather?'
          'id={}&units=metric&lang=ru&appid={}').format(city_id, apid_key)
    grabber.go(url)
    weather_data = json.loads(grabber.doc.unicode_body())
    printing(weather_data)


def get_city_id(cities, grabber, apid_key):
    """Получаем от пользователя id города
    """
    pp = pprint.PrettyPrinter(width=40, compact=True)
    print('{:*^40}'.format('Погода'))
    city_id = None
    while True:
        choise = input('\nВведите название города (quit - выход)\n>>> ').capitalize()
        if choise == 'Quit':
            print('Выход из программы')
            sys.exit()
        else:
            suggest = []
            for line in cities:
                if choise == line['name']:
                    city_id = line['_id']
                    break
                elif line['name'].startswith(choise[:int(len(choise) / 1.5)]):
                    suggest.append(line['name'])
        if city_id is not None:
            get_weather_data(grabber, city_id, apid_key)
            continue

        print("Уточните название")
        if len(suggest):
            print("Возможные варианты:")
            pp.pprint(suggest)
        else:
            print('не обнаружено совпадений')


if __name__ == '__main__':
    # Та часть, где получаем все необходимые данные
    url = 'https://home.openweathermap.org/users/sign_in'
    gr = grab.Grab(log_file='out.html')
    queue = mp.Queue()
    download_names = mp.Process(target=get_cities, args=(queue,))
    download_names.start()
    apid_key = connect(url, gr)
    cities = queue.get()
    download_names.join()

    # Та часть, где пользователь вводит данные
    get_city_id(cities, gr, apid_key)

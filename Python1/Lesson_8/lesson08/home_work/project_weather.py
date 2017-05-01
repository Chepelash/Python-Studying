
import os
import sys
import re
import multiprocessing as mp
import gzip
import json
import urllib.request
import grab


def connect(url, grabber, queue):
    """Авторизация на сайте и получения apid ключа для запроса
    """
    grabber.go(url)
    grabber.set_input('user[email]', 'weather_zora@mail.ru')
    grabber.set_input('user[password]', 'Simple_Weather')
    grabber.submit()
    page = gr.doc.unicode_body()
    success = re.search(r"(?<=<div class='panel-body'>)(.*)(?=</div>)", page)
    if 'success' not in success:
        sys.exit(1)

    grabber.go('https://home.openweathermap.org/api_keys')
    page = gr.doc.unicode_body()
    apid_key = re.search(r"(?<=<pre>)(.*)(?=</pre>)", page)

    queue.put(apid_key)


def get_cities():
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
    return [json.loads(line) for line in cities.split('\n')[:-1]]


def get_weather_data(grabber, id, apid_key):
    url = 'http://api.openweathermap.org/data/2.5/weather?\
           id={}&units=metric&appid={}'.format(id, apid_key)
    grabber.go(url)
    weather_data = json.loads(grabber.doc.unicode_body())

    return weather_data


if __name__ == '__main__':
    url = 'https://home.openweathermap.org/users/sign_in'
    gr = grab.Grab(log_file='out.html')
    queue = mp.Queue()
    authtorization = mp.Process(target=connect, args=(url, gr, queue))
    city_names = get_cities()
    apid_key = queue.get()
    authtorization.join()

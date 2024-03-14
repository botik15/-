import sys
import time
from random import randint
import requests
from bs4 import BeautifulSoup
import telebot
from fake_useragent import UserAgent
import configparser

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг
'''
[settings]
token_chatgtp = *******
chat_id = *******
token_telegram = *******
message_id = *******
'''

token_telegram = (config["settings"]["token_telegram"])

bot = telebot.TeleBot(token_telegram)
ua = UserAgent()
# print(ua.random)
header = {'User-Agent': str(ua.chrome)}

for i in range(10):
    url = 'https://cheb.ws/prodam/kvartira/?class=3&page=' + str(i)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for items in soup.find_all('table'):
        for item in items.find_all('tr', 'odo'):
            try:
                img = 'https://cheb.ws/' + item.find('td', 'col-foto').find('div').find('a').img['src'].replace(
                    'thumbnails', 'normal')
            except:
                img = ''
            name = item.find('td', 'col-type').find('a').find('span').text
            opicanie = item.find('td', 'col-type').find('a').find('div').text
            urls = item.find('td', 'col-type').find('a').get('href')
            adress = item.find('td', 'col-address').text.replace('г. ', ' г. ')
            etaj = item.find('td', 'col-etazh').text
            ploschad = item.find('td', 'col-ploschad').text
            price_kv_m = item.find('td', 'rowprice').find('div').text
            price = item.find('td', 'rowprice').text.replace(price_kv_m, '')
            prodavec = item.find('td', 'col-author').find('a').text
            phone = item.find('td', 'col-author').find('div', 'phone').text
            data = item.find('td', 'col-author').find('div', 'tabdate').text

            x = (f'{opicanie}\n\nАдрес: {ploschad}, {adress}, {etaj}\n\nЦена: {price}\nКв.м: {price_kv_m}\n'
                 f'\nПродавец: {prodavec}\nПродавец: {phone}\nДата публикации: {data}\n\nПодробнее : {urls}')

            with open('db.txt', 'r', encoding='utf8') as f_r:
                line = f_r.readlines()[0]
                if line.find(urls) == -1:
                    with open('db.txt', 'a', encoding='utf8') as f:
                        try:
                            bot.send_photo(chat_id='601548422', photo=img, caption=x)
                        except BaseException as error:
                            print('An exception occurred: {}'.format(error))
                            time.sleep(randint(10, 15))
                            continue
                        print('Добавил:\n ' + x)
                        f.write(urls)
                        time.sleep(randint(5, 10))

    print('\n')
    print('____________________________________' + str(i) + '____________________________________')

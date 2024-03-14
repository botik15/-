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
ua = UserAgent()
# print(ua.random)
header = {'User-Agent':str(ua.chrome)}
# bot.send_message(chat_id='601548422', text='11')

for i in range(1):
    urls = 'https://chuvashia.move.ru/cheboksary/kvartiry/prodazha_trehkomnatnih_kvartir/ot_sobstvennika/ne_pervii_etazh/ne_poslednii_etazh/?price_max=6000000&limit=100'
    response = requests.get(urls)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(response)
    for item in soup.find_all('ul', 'search-item move-object'):

            try:
                name = item.find('div').find('div','LayoutSnippet__main').find('div').find('div','LayoutSnippet__generalInfo').find('div','LayoutSnippet__title').find('a').text
                adress = item.find('div').find('div','LayoutSnippet__main').find('div').find('div','LayoutSnippet__generalInfo').find('div','LayoutSnippet__title').find('div','LayoutSnippet__address').text
                price = item.find('div').find('div','LayoutSnippet__main').find('div').find('div','LayoutSnippet__generalInfo').find('div','LayoutSnippet__priceDescription').find('div','LayoutSnippet__price').find('div').find('div').text
                price_kv_m = item.find('div').find('div','LayoutSnippet__main').find('div').find('div','LayoutSnippet__generalInfo').find('div','LayoutSnippet__priceDescription').find('div','LayoutSnippet__priceDetail').find('div').find('div').text
                zastroishik = item.find('div').find('div','LayoutSnippet__main').find('div').find('div','LayoutSnippet__dealInfo').find('div','LayoutSnippet__dealInfoTop').find('div','LayoutSnippet__building').find('div').find('div').find('a').text
                opicanie = item.find('div').find('div','LayoutSnippet__main').find('div').find('div','LayoutSnippet__dealInfo').find('div','LayoutSnippet__dealInfoTop').find('div','LayoutSnippet__description').text
                data = item.find('div').find('div','LayoutSnippet__main').find('div').find('div','LayoutSnippet__dealInfo').find('div','LayoutSnippet__dealInfoTop').find('div','LayoutSnippet__lastUpdate').text
                prodavec = item.find('div').find('div','LayoutSnippet__main').find('div').find('div','LayoutSnippet__dealInfo').find('div','LayoutSnippet__ownerInfo').find('div','LayoutSnippet__seller').find('div').find('div').find('div','AuthorBadge__seller').find('div').text
                url = item.find('div').find('div','LayoutSnippet__main').find('div').find('div','LayoutSnippet__generalInfo').find('div','LayoutSnippet__title').find('a').get('href')
                img = item.find('div').find('div', 'ClOfferSnippet__gallery').find('a').find('div').find('div','GallerySnippet__preview').find('picture').img['src'].replace('//','')

                x = (f'{name}\n{opicanie}\n\nАдрес: {adress}\n\nЦена: {price}\nКв.м: {price_kv_m}\n\n'
                     f'\nПродавец: {prodavec}\nДата публикации: {data}\n\nПодробнее : {url}')

                with open('db_m2.txt', 'r', encoding='utf8') as f_r:
                    line = f_r.readlines()[0]
                    if line.find(url) == -1:
                        with open('db_m2.txt', 'a', encoding='utf8') as f:
                            try:
                                bot.send_photo(chat_id='601548422', photo=img, caption=x)
                            except BaseException as error:
                                print('An exception occurred: {}'.format(error))
                                continue
                            print('Добавил:\n ' + x)
                            f.write(url)
                            time.sleep(randint(5, 10))
            except:
                pass


    print('\n')
    print('____________________________________'+str(i)+'____________________________________')

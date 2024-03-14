from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
header = {'User-Agent':str(ua.chrome)}
options = Options()
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

for i in range(3):
    driver.get('https://www.avito.ru/cheboksary/kvartiry/prodam/3-komnatnye/vtorichka-ASgBAQICAUSSA8YQAkDmBxSMUsoIFIRZ?cd=1&f=ASgBAQECAkSSA8YQwMENuv03BEDmBxSMUsoIFIRZ5hYU5vwBrL4NFKTHNQFFxpoMF3siZnJvbSI6MCwidG8iOjYwMDAwMDB9&p='+str(i)+'&s=104')
    timeout = 5
    while True:
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'index-root-KVurS'))
            WebDriverWait(driver, timeout).until(element_present)
            break # it will break from the loop once the specific element will be present.
        except TimeoutException:
            print("Timed out waiting for page to load")
    element = driver.find_element(By.CLASS_NAME, 'index-root-KVurS').get_attribute('innerHTML')
    time.sleep(2)
    soup = BeautifulSoup(element, 'html.parser')
    for items in soup.find_all('div', 'items-items-kAJAg'):
        for item in items.find_all('div','iva-item-content-rejJg'):

            try:
                name = item.find('div', 'iva-item-body-KLUuy').find('div','iva-item-titleStep-pdebR').find('a').find('h3').text.replace('\n', '')
            except:
                name = ''
            try:
                url = 'https://www.avito.ru/' + item.find('div', 'iva-item-body-KLUuy').find('div','iva-item-titleStep-pdebR').find('a').get('href')
            except:
                url = ''
            try:
                price = item.find('div', 'iva-item-body-KLUuy').find('div','iva-item-priceStep-uq2CQ').find('span').find('span','price-price-JP7qe').find('span').text
            except:
                price = ''
            try:
                price_kv_m = item.find('div', 'iva-item-body-KLUuy').find('div','iva-item-priceStep-uq2CQ').find('span').text.replace(price,'')
            except:
                price_kv_m = ''
            try:
                data = item.find('div', 'iva-item-body-KLUuy').find('div','iva-item-dateInfoStep-_acjp').find('div').find('span').find('span').find('div').text
            except:
                data = ''
            try:
                adress = item.find('div', 'iva-item-body-KLUuy').find('div','iva-item-developmentNameStep-qPkq2').find('div').find('span').text
            except:
                adress = ''
            try:
                opicanie = item.find('div', 'iva-item-body-KLUuy').find('div','iva-item-descriptionStep-C0ty1').find('div').text
            except:
                opicanie = ''


            x = (f'{name}\n{opicanie}\n\nАдрес: {adress}\n\nЦена: {price}\nКв.м: {price_kv_m}\n\n'
                 f'Дата публикации: {data}\n\nПодробнее : {url}')

            with open('db_avito.txt', 'r', encoding='utf8') as f_r:
                line = f_r.readlines()[0]
                if line.find(url) == -1:
                    with open('db_avito.txt', 'a', encoding='utf8') as f:
                        bot.send_message(chat_id='601548422', text=x)
                        print('Добавил:\n ' + x)
                        f.write(url)
                        time.sleep(randint(5, 10))
            print('\n')
            print('_______________________________________________________________________')

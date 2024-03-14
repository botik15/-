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

ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}
options = Options()
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

for i in range(4):
    driver.get('https://cheboksary.cian.ru/cat.php?deal_type=sale&engine_version=2&floornl=1&house_material%5B0%5D=1&house_material%5B1%5D=2&house_material%5B2%5D=3&house_material%5B3%5D=8&ipoteka=1&is_first_floor=0&min_house_year=1980&minfloorn=7&minlift=1&offer_type=flat&p='+str(i)+'&region=5047&room3=1&totime=2592000&with_neighbors=0&wp=1')
    timeout = 5
    while True:
        try:
            element_present = EC.presence_of_element_located((By.ID, 'frontend-serp'))
            WebDriverWait(driver, timeout).until(element_present)
            break # it will break from the loop once the specific element will be present.
        except TimeoutException:
            print("Timed out waiting for page to load")
    element = driver.find_element(By.CLASS_NAME, '_93444fe79c--wrapper--W0WqH').get_attribute('innerHTML')
    time.sleep(2)

    soup = BeautifulSoup(element, 'html.parser')
    for item in soup.find_all('article'):
        name = item.find('div','_93444fe79c--card--ibP42').find('div','_93444fe79c--content--lXy9G').find('div','_93444fe79c--general--BCXJ4').find('div').find_all('div')[0].find('span').find('span').text
        url = item.find('div','_93444fe79c--card--ibP42').find('div','_93444fe79c--content--lXy9G').find('div','_93444fe79c--general--BCXJ4').find('div').find('a').get('href')


        x = (f'{name}\n\nПодробнее : {url}')

        with open('db_cian.txt', 'r', encoding='utf8') as f_r:
            line = f_r.readlines()[0]
            if line.find(url) == -1:
                with open('db_cian.txt', 'a', encoding='utf8') as f:
                    # bot.send_message(chat_id='601548422', text=x)
                    print('Добавил:\n ' + x)
                    f.write(url)
                    # time.sleep(randint(5, 10))
        print('\n')
        print('_______________________________________________________________________')

import requests
from bs4 import BeautifulSoup
import lxml

import db

headers = {
    'accept': '*/*',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.4.840 Yowser/2.5 Safari/537.36"
}

req = requests.get(f"https://rostov.proshoper.ru/actions/pyaterochka/", headers=headers)
src = req.text
soup = BeautifulSoup(src, 'lxml')
category = ['moloko-syr-yajca', 'tovary-dlya-detej', 'voda-soki-napitki']
def find_product(category):
    category1 = soup.find('div', {'id': category})
    category1 = category1.find_all('article', {'class': 'product relative bg-white px-3 py-2 border-b border-solid border-color-300e md:border-none md:w-1/4 md:mb-4 md:mt-4 md:mx-2 md:px-2'})
    for i in category1:
        name = i.find('div', {'class': 'break-words leading-snug text-2sm md:font-medium'}).text
        cost = i.find('span', {'class': 'font-bold text-2xl md:text-red-e6'}).text
        cost = cost.replace(' ₽', '')
        db.add_product(name, 'Напитки', cost)
        print (f"{name} добавлен")

import requests
from bs4 import BeautifulSoup
import lxml

import json

from fake_useragent import UserAgent

import datetime
import os
import sys

# from random import randrange
ua = UserAgent()
ua_ = ua.random



my_path_ = './data/all'


def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,vi;q=0.5,pt;q=0.4,ka;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'ASPSESSIONIDAESQDRRS=KBCNMBPCFPPCDFAJMFIODMHG',
    'If-Modified-Since': 'Fri, 05 Aug 2022 13:53:54 GMT',
    'If-None-Match': '"d0db3dcdd2a8d81:0"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    "User-Agent": f'{ua}',
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

print('start...')


y_ = 2000

a = 'data\\collect\\'
n = os.path.join(os.getcwd(), os.path.normpath(a))

with open(os.path.join(n, f'collect_{y_}.json'), 'r', encoding='utf-8') as set_:
    set_data = json.load(set_)

for i in set_data:
    sid = i['sid']
    event = i['event']

    # print(f'{sid} --->>> {event}')
    # sid = 2266

    url_start_ = f'https://www.nrchadata.com/pdf/news/prod/ShowResultsDetails.asp?sid={sid}'

    with requests.Session() as session:
        response = session.get(url=url_start_, headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')
        name__ = soup.find('span')#.split('<br>')

        # print(name__)

        for i, x in enumerate(name__):
            if i == 0:
                # print(f'{i} ---> {x}')

                xx = str(x).split(' - ')
                data__ = (xx[-1]).strip()
                dir_y__ = data__.split('/')[-1]

                # print(data__)

                # print(datetime.datetime.strptime(data_, '%Y-%m-%d %H:%M:%S').strftime('%m/%d %a %H:%M'))
                year_ = datetime.datetime.strptime(data__, '%m/%d/%Y').strftime('%Y')
                my_makedirs(f'{my_path_}/{year_}')



                data_ = datetime.datetime.strptime(data__, '%m/%d/%Y').strftime('%Y%m%d')
                name__ = str(xx[0:-1])

                name__ = f'{str(xx[0:-1])}' \
                    .replace("['", "") \
                    .replace("']", "") \
                    .replace("'", "") \
                    .replace(",", "") \
                    .replace("?", "") \
                    .replace("#", "") \
                    .replace(" ", "_") \
                    .replace("\\", "") \
                    .replace("/", "") \
                    .replace('"', '=') \
                    .replace("*", "")

                full_name_ = f'{data_}_{sid}_{name__}'

                my_makedirs(f'{my_path_}/{year_}/{full_name_}')

        items_ = []
        titles = soup.find_all('span', class_='bodyTextBold')#.text

        for i in titles:
            file_name = i.text

        all__ = soup.find_all('table')[1]
        col_ = all__.find_all('td', class_='bodyTextBold')

        colums_ = []
        for i in col_:
            colums_.append(i.text)

        # print(f'{len(col_)} === {colums_}')

        events_ = all__.find_all('span', class_='bodyTextBold')

        trs_ = all__.find_all('tr')

        ttt = 0
        file_name_old_ = ''
        file_name_ = ''

        for i in trs_:
            try:
                events_ = i.find('span', class_='bodyTextBold')
                file_name_old_ = file_name_
                file_name_ = events_.text

                if ttt != 0:

                    with open(f'{my_path_}/{year_}/{full_name_}/{file_name_old_}.json', 'w', encoding='utf-8') as file:
                        json.dump(info_, file, indent=4, ensure_ascii=False)
                    info_ = []

                ttt = 1
                info_ = []

                print(f'--->>> {file_name_}')
            except:
                www = i.find_all('td', class_='bodyText')

                value_ = []

                for c, eee in enumerate(www):
                    ele_ = eee.text
                    if ele_ == '-':
                        ele_ = 'NONE'

                    value_.append(ele_)

                tr_ = []
                tr_ = dict(zip(colums_, value_))
                info_.append(tr_)

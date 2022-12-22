import requests
from bs4 import BeautifulSoup
import lxml

import json

from fake_useragent import UserAgent

import datetime
import os
import sys
import re

# from random import randrange
ua = UserAgent()
ua_ = ua.random



my_path_ = './data/all'
year_ = ''


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

print(f'start...\n')


y_ = 2023

a = 'data\\collect\\'
n = os.path.join(os.getcwd(), os.path.normpath(a))

with open(os.path.join(n, f'collect_{y_}.json'), 'r', encoding='utf-8') as set_:
    set_data = json.load(set_)

len_ = len(set_data)
count_sid = 0

print(f'Find: {len_} sids!')
err_sids = []

for i in set_data:
    sid = i['sid']
    event = i['event']
    count_sid += 1

    print(f'\n\t[{count_sid} of {len_}]   SID: {sid} _______ EVENT: {event}')
    # sid = 6640

    url_start_ = f'https://www.nrchadata.com/pdf/news/prod/ShowResultsDetails.asp?sid={sid}'

    with requests.Session() as session:
        response = session.get(url=url_start_, headers=headers, timeout=(1, 2))

        soup = BeautifulSoup(response.text, 'lxml')

        try:
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
                    my_makedirs(f'{my_path_}/{year_}_TEST')



                    data_ = datetime.datetime.strptime(data__, '%m/%d/%Y').strftime('%Y%m%d')
                    name__ = str(xx[0:-1])

                    name__ = f'{str(xx[0:-1])}' \
                        .replace(":", "") \
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

                    my_makedirs(f'{my_path_}/{year_}_TEST/{full_name_}')

            items_ = []
            titles = soup.find_all('span', class_='bodyTextBold')#.text

            for i in titles:
                file_name = i.text

            all__ = soup.find_all('table')[1]
            col_ = all__.find_all('td', class_='bodyTextBold')

            colums_ = []
            colums_sd = []

            for i in col_:
                colums_.append(i.text)
                colums_sd.append(i.text)

            colums_sd.insert(2, 'Sire')
            colums_sd.insert(3, 'Dam')

            # print(f'{len(col_)} === {colums_}')

            events_ = all__.find_all('span', class_='bodyTextBold')

            trs_ = all__.find_all('tr')

            ttt = 0
            file_name_old_ = ''
            file_name_ = ''

            wr_ = False

            for i in trs_:
                try:
                    events_ = i.find('span', class_='bodyTextBold')
                    wr_ = True
                    file_name_old_ = file_name_
                    file_name_ = events_.text \
                        .replace(":", "") \
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

                    if ttt != 0:

                        with open(f'{my_path_}/{year_}_TEST/{full_name_}/{file_name_old_}.json', 'w', encoding='utf-8') as file:
                            json.dump(info_, file, indent=4, ensure_ascii=False)
                        info_ = []
                        wr_ = False

                    ttt = 1
                    info_ = []

                    print(f'\t\t--->>> {file_name_}')

                except:
                    www = i.find_all('td', class_='bodyText')

                    value_ = []
                    bool_sd_ = False

                    for c, eee in enumerate(www):
                        if c == 1:
                            tmp__ = eee.text
                            # script_ = str(re.findall('\((.*?)\)', str(tmp_))). \
                            #     replace("['", ""). \
                            #     replace("']", "")#.split('%2C')
                            # print(script_)
                            try:
                                tmp_ = tmp__.split('(')
                                # Horse name
                                ele_ = tmp_[0]
                                # Sire & Dam
                                tmp2__ = str(tmp_[1]).replace(')', '').split(' X ')
                                Sire_ = tmp2__[0]
                                Dam_ = tmp2__[1]

                                bool_sd_ = True
                                value_.append(ele_)
                                value_.append(Sire_)
                                value_.append(Dam_)
                            except:
                                value_.append(ele_)
                        else:
                            ele_ = eee.text
                            if ele_ == '-':
                                ele_ = 'NONE'

                            value_.append(ele_)

                    tr_ = []
                    if bool_sd_ == True:
                        tr_ = dict(zip(colums_sd, value_))
                    else:
                        tr_ = dict(zip(colums_, value_))
                    info_.append(tr_)
            if wr_ == True:
                wr_ = False
                with open(f'{my_path_}/{year_}_TEST/{full_name_}/{file_name_old_}.json', 'w', encoding='utf-8') as file:
                    json.dump(info_, file, indent=4, ensure_ascii=False)
        except:
            err_sids.append(
                {
                    "err_sid": sid
                }
            )
            print(f'\t\t! ! ! ! !   ___ ERROR ___   !!!!!')

with open(f'{my_path_}/err_sids.json', 'w', encoding='utf-8') as file:
    json.dump(err_sids, file, indent=4, ensure_ascii=False)

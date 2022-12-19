import requests
from bs4 import BeautifulSoup
import lxml

import json

from fake_useragent import UserAgent

import datetime
import os

# from random import randrange
ua = UserAgent()
ua_ = ua.random



def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)



# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "User-Agent": f'{ua}'  # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,
#     # like Gecko) Chrome/96.0.4664.45 Safari/537.36"
# }

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

id_ = 6993

url_start_ = f'https://www.nrchadata.com/pdf/news/prod/ShowResultsDetails.asp?sid={id_}'

with requests.Session() as session:
    response = session.get(url=url_start_, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')
    name__ = soup.find('span')#.split('<br>')

    print(name__)

    for i, x in enumerate(name__):
        if i == 0:
            print(f'{i} ---> {x}')

            xx = str(x).split(' - ')
            data__ = (xx[-1]).strip()
            dir_y__ = data__.split('/')[-1]

            print(data__)

            # print(datetime.datetime.strptime(data_, '%Y-%m-%d %H:%M:%S').strftime('%m/%d %a %H:%M'))
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


            full_name_ = f'{data_}_{name__}'
            print(full_name_)
            # for y in xx:
            #     print(y)

    items_ = []
    titles = soup.find_all('span', class_='bodyTextBold')#.text

    for i in titles:
        file_name = i.text
        # items_.append(i)

    file_name__ = '123'

    col__ = soup.find_all('table')[1]
    col_ = col__.find('tr')#.find_all('td', class_='bodyTextBold')
    print(col_)
    for i in col_:
        print(i.text)



    # dirr_ = f'{dir_y__}/{id_}_{full_name_}'
    # my_makedirs(dirr_)
    #
    # with open(f'{dirr_}/{file_name__}.json', 'w', encoding='utf-8') as file:
    #     json.dump(items_, file, indent=4, ensure_ascii=False)


    # strong__ = soup.find('div', id='panel_contacts').find_all('strong')

breakpoint()











# print(ua_)
#
# response = requests.get(f'{url_start_}', headers=headers)
#
# # printing request cookies
# print(response.cookies.get_dict())


print(url_start_)


client = requests.session()

# Retrieve the CSRF token first
client.get(url_start_)

php__ = client.cookies
# php_ = php__['PHPSESSID']
print(php__)
print(php__.get_dict())



breakpoint()
#
tok__ = json.loads(response.text)
tok_ = tok__['access']
# print(tok_)

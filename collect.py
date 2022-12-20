import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime


url_ = 'https://www.nrcha.com/show-results/'
current_year = datetime.now().year



for y_ in range(2000, current_year + 2):

    info_ = []

    events = []
    e_date = []
    sids = []


    print(f':: {y_} ::')

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,vi;q=0.5,pt;q=0.4,ka;q=0.3',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Origin': 'null',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'showyear': f'{y_}',
    }

    with requests.Session() as session:
        # response = session.get(url=url_, headers=headers)
        response = requests.post('https://www.nrchadata.com/pdf/news/prod/ShowResults.asp', headers=headers, data=data)
        # print(f'{y_} ---> {response}')
        soup = BeautifulSoup(response.text, 'lxml')
        items_ = soup.find_all('span', class_='bodyTextBoldMed')#.split('<br>')

        for i in items_:
            sid = str(re.findall(r'[0-9]+', i.find('a').get('href'))).replace("['", "").replace("']", "")

            sids.append(
                {
                    "sid": sid
                }
            )
            events.append(
                {
                    "event": i.text
                }
            )

        items_date_ = soup.find_all('span', class_='bodyText')

        for i in items_date_:
            date__ = i.text
            date_ = date__.split(" -- ")[-1]

            print(f'\t---> {date_}')

            e_date.append(
                {
                    "date": date_
                }
            )

        # tr_ = []
        # tr_ = dict(zip(items, items_date, sids))
        # info_.append(tr_)

        for i, x in enumerate(events):
            info_.append(
                {
                    "sid": sids[i]["sid"],
                    "event": x["event"],
                    "date": e_date[i]["date"]
                }
            )

    with open(f'./data/collect/collect_{y_}.json', 'w', encoding='utf-8') as file:
        json.dump(info_, file, indent=4, ensure_ascii=False)

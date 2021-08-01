import requests
from bs4 import BeautifulSoup
import os
import sys
import threading
import time
import schedule
from lxml import etree
import json

sys.path.append(os.path.join(sys.path[0], '../../'))
link = 'https://ncov.moh.gov.vn/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}
r = requests.get(link, headers=headers, verify=False)
soup = BeautifulSoup(r.text, 'html.parser')
table_data = soup.find(id="sailorTable")
tr_data = table_data.find_all('tr')
cityList = []


def get_data():
    for row in tr_data[1:]:
        td_data = row.find_all('td')
        city_name = td_data[0].text
        total_cases = td_data[1].text
        today_cases = td_data[2].text
        deaths = td_data[3].text
        str = {'city_name': city_name, 'totalCases': total_cases, 'today_cases': today_cases, 'deaths': deaths}
        cityList.append(str)

    # dom = etree.HTML(str(soup)) dt = dom.xpath('/html/body/div[1]/div[2]/section/div/div/div/div/div[
    # 1]/section/div/div[2]/div/section[1]/div[2]/div[2]/div/div[3]/div/div[1]') print(dt)
    # you can use for if u want :D 
    total_data = soup.find_all("div", class_="row mt-5")
    data_vn = total_data[0].find_all('span')
    data_world = total_data[1].find_all('span')
    overview_data = {'vietnam': {'totalCase': data_vn[0].text, 'infectious': data_vn[1].text, 'cured': data_vn[2].text,
                                 'death': data_vn[3].text},
                     'world': {'totalCase': data_world[0].text, 'infectious': data_world[1].text,
                               'cured': data_world[2].text,
                               'death': data_world[3].text}}

    print(f'{overview_data} \n \n {cityList}')


def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()


schedule.every(10).seconds.do(run_threaded, get_data)

while True:
    schedule.run_pending()
    time.sleep(1)

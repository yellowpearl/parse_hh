import sys
import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
vacancy_name = "Performance marketing manager"
pages = 5
base_url = f'https://hh.ru/search/vacancy?area=1&area=2&area=3&area=41&area=237&area=53&area=130&area=1454&search_period=30&text={vacancy_name}&page='
file_list = open('Performance marketing manager.txt', 'w')

def hh_parse(base_url, headers):
    zero = 0
    while pages > zero:
        print(zero)
        zero = str(zero)
        session = requests.Session()
        request_full = session.get(base_url + zero, headers=headers)
        if request_full.status_code == 200:
            soup = bs(request_full.content, 'html.parser')
            vacancies = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
            for vacancy in vacancies:
                title = vacancy.find('a', attrs = {'data-qa': 'vacancy-serp__vacancy-title'}).text
                try:
                    slash_index = title.index('/')
                    name_index = title.index(vacancy_name)
                    if name_index < slash_index:
                        alt_vacancy_name = title[slash_index+1:]
                    else:
                        alt_vacancy_name = title[:slash_index]
                except:
                        alt_vacancy_name = None
                if alt_vacancy_name != None:
                    print(alt_vacancy_name)
                    file_list.write(alt_vacancy_name+'\n')
            zero = int(zero)+1
        else:
            print("Error in page", zero)

hh_parse(base_url, headers)



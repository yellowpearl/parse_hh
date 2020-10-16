import sys
import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
vacancy_list = """Продакт-менеджер
Продукт-менеджер
Product Manager
Продакт Менеджер
Менеджер продукта
Менеджер по продукту
Product Marketing Manager
Product Owner
Продуктолог"""
pages = 5


def hh_parse(base_url, headers):
    for name in vacancy_list:
        base_url = f'https://hh.ru/search/vacancy?area=1&area=2&area=3&area=41&area=237&area=53&area=130&area=1454&search_period=30&text={name}&page='
        zero = 0
        while pages > zero:
            zero = str(zero)
            session = requests.Session()
            request_full = session.get(base_url + zero, headers=headers)
            if request_full.status_code == 200:
                soup = bs(request_full.content, 'html.parser')
                vacancies = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
                for vacancy in vacancies:
                    vacancy_href = soup.find("a", href=True)['href']
                    vacancy_href = vacancy_href[:vacancy_href.index('?')]
                    vacancy_request = session.get(vacancy_href, headers=headers)
                    if request_full.status_code == 200:
                        vacancy_soup = bs(vacancy_request.content, 'html.parser')
                        # Получаем название профессии и альтернативные названия
                        vacancy_title = vacancy_soup.find('h1', attrs={'data-qa': 'vacancy-title'}).text
                        try:
                            slash_index = vacancy_title.index('/')
                            name_index = vacancy_title.index(vacancy_name)
                            if name_index < slash_index:
                                alt_vacancy_name = vacancy_title[slash_index:]
                            else:
                                alt_vacancy_name = vacancy_title[:slash_index]
                        except:
                            alt_vacancy_name = None
                        # Получаем зп вакансии
                        vacancy_salary = vacancy_soup.find('p', attrs={'class': 'vacancy-salary'}).text
                        if vacancy_salary == "з/п не указана":
                            vacancy_salary = None
                        # проверить будет ли выдавать зп

                        vacancy_full_text = vacancy_soup.find('div', attrs={'data-qa': 'vacancy-description'}).text
                        try:
                            duties_index = vacancy_full_text.index('бязанности') - 1
                            vacancy_info = vacancy_full_text[:duties_index]
                            try:
                                requirements_index = vacancy_full_text.index('ребования') - 1
                                vacancy_duties = vacancy_full_text[duties_index:requirements_index]
                                try:
                                    conditions_index = vacancy_full_text.index('словия') - 1
                                    vacancy_requirements = vacancy_full_text[requirements_index:conditions_index]
                                    vacancy_conditions = vacancy_full_text[conditions_index:]
                                except:
                                    vacancy_conditions = ""
                                    vacancy_requirements = ""
                            except:
                                vacancy_duties = ""
                                vacancy_requirements = ""
                                vacancy_conditions = ""
                        except:
                            vacancy_info = vacancy_full_text
                            vacancy_requirements = ""
                            vacancy_conditions = ""
                            vacancy_duties = ""

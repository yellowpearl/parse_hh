import sys
import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
vacancy_list = ["Бренд-менеджер"]
pages = 40



file_inf = open('inf.txt', 'w')
file_duties = open('duties.txt', 'w')
file_requirements = open('requirements.txt', 'w')
file_conditions = open('conditions.txt', 'w')
file_keys = open('keys.txt', 'w')

file_inf_two = open('inf_two.txt', 'w')
file_duties_two = open('duties_two.txt', 'w')
file_requirements_two = open('requirements_two.txt', 'w')
file_conditions_two = open('conditions_two.txt', 'w')
file_keys_two = open('keys_two.txt', 'w')


def hh_parse(headers):
    for name in vacancy_list:
        base_url = f'https://hh.ru/search/vacancy?area=1&area=2&area=3&area=41&area=237&area=53&area=130&area=1454&search_period=30&text={name}&only_with_salary=true&salary=100000&from=cluster_compensation&showClusters=true&page='
        zero = 0
        print('############')
        print(name)
        while pages > zero:
            zero = str(zero)
            session = requests.Session()
            request_full = session.get(base_url + zero, headers=headers)
            print(zero)
            if request_full.status_code == 200:
                soup = bs(request_full.content, 'html.parser')
                vacancies = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
                for vacancy in vacancies:
                    # Вычисляем зп
                    compensation = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                    try:
                        ind = compensation.index('-')
                        compensation = int(compensation[:ind-4]+'000')
                    except:
                        compensation = compensation[3:]
                        compensation = int(compensation[:compensation.index("\xa0")]+'000')

                    # Определяем входит ли в промежуток 100 000 - 200 000
                    if compensation < 100000:
                        continue
                    elif compensation < 200000:
                        group = 1
                    elif compensation >= 200000:
                        group = 2

                    # Находим ссылку на вакансию
                    vacancy_href = vacancy.find("a", attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                    vacancy_href = vacancy_href[:vacancy_href.index('?')]


                    vacancy_request = session.get(vacancy_href, headers=headers)
                    if request_full.status_code == 200:
                        vacancy_soup = bs(vacancy_request.content, 'html.parser')


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

                        keys = vacancy_soup.find_all('div', attrs={'data-qa': 'bloko-tag bloko-tag_inline skills-element'})
                        print(len(keys))
                        vacancy_keys = ''
                        for key in keys:
                            text_key = key.find('span', attrs={'data-qa': 'bloko-tag__text'}).text
                            vacancy_keys = vacancy_keys + text_key + ' '

                        if group == 1:
                            file_keys.write(vacancy_keys)
                        else:
                            file_keys_two.write(vacancy_keys)


                        if group == 1:
                            file_inf.write(vacancy_info+' ')
                            file_duties.write(vacancy_duties + ' ')
                            file_requirements.write(vacancy_requirements + ' ')
                            file_conditions.write(vacancy_conditions + ' ')
                        else:
                            file_inf_two.write(vacancy_info + ' ')
                            file_duties_two.write(vacancy_duties + ' ')
                            file_requirements_two.write(vacancy_requirements + ' ')
                            file_conditions_two.write(vacancy_conditions + ' ')


                zero = int(zero) + 1
            else:
                print("Error in page", zero)
        print('############')

hh_parse(headers)
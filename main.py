import requests
from pprint import pprint
from bs4 import BeautifulSoup
from fake_headers import Headers
import json


def get_headers():
    return Headers(browser='firefox', os='win').generate()


HOST = 'https://spb.hh.ru/search/vacancy?area=1&area=2&search_field=name&search_field=company_name' \
       '&search_field=description&enable_snippets=true&text=python'
hh_html = requests.get(HOST, headers=get_headers()).text
soup = BeautifulSoup(hh_html, features='lxml')
vacancies = soup.find_all("div", class_="serp-item")

vacancy_description = []
for vacancy in vacancies:
    description = vacancy.find(class_='vacancy-serp-item__layout')
    description_text = description.find(class_='g-user-content').text
    if 'Django' in description_text or 'Flask' in description_text:
        vacancy_description.append(vacancy)


vacancy_list = []
for item in vacancy_description:
    title = item.find('a', class_='serp-item__title')
    link_tag = item.find('a', class_='serp-item__title')
    link = link_tag['href']
    salary_link = item.find('span', attrs={'data-qa': "vacancy-serp__vacancy-compensation"})
    salary = salary_link.text.replace('\u202f', '')
    company = item.find('a', class_='bloko-link bloko-link_kind-tertiary')
    city = item.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address', 'class': 'bloko-text'})
    vacancy_list.append({
        'Вакансия': title.text,
        'Ссылка': link,
        'Зарплата': salary,
        'Компания': company.text,
        'Город': city.text

    })

pprint(vacancy_description)
pprint(vacancy_list)


with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancy_list, f, ensure_ascii=False)

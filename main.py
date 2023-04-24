import re
import requests
from bs4 import BeautifulSoup
import json


def get_headers():
    return {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) '
                                                                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                       'Chrome/70.0.3538.67 Safari/537.36 '
                                                                       'OPR/56.0.3051.104'}


if __name__ == '__main__':
    url = 'https://hh.ru/search/vacancy?text=Python&salary=&area=1&area=2&ored_clusters=true'
    hh_list_html = requests.get(url, headers=get_headers()).text
    hh_list_soup = BeautifulSoup(hh_list_html, 'html.parser')
    main_content = hh_list_soup.find('div', id='a11y-main-content')
    vacancies = main_content.find_all('a', class_='serp-item__title')
    url_pattern = re.compile(r'(https?://\S+)\"')
    keys_pattern = re.compile(r'Вjango|Flask', re.I)
    vacancy_title_pattern = re.compile(r'<h1[^>]*>(.*?)<\/h1>')
    company_title_pattern = re.compile(r'<span[^>]*>(.*?)<\/span>')
    salary_pattern = re.compile(r'>(.*?)<')
    final_data = []
    for vacancy in vacancies:
        vacancy_url = ''.join(url_pattern.findall(str(vacancy)))
        vacancy_html = requests.get(vacancy_url, headers=get_headers()).text
        vacancy_soup = BeautifulSoup(vacancy_html, 'html.parser')
        vacancy_content = vacancy_soup.find_all('div', class_='g-user-content')
        if keys_pattern.findall(str(vacancy_content)):
            vacancy_title_temp = vacancy_soup.find('h1', {'data-qa': 'vacancy-title'})
            vacancy_title = vacancy_title_pattern.findall(str(vacancy_title_temp))[0]
            company_title_temp = vacancy_soup.find('span', {'data-qa': 'bloko-header-2'})
            company_title = company_title_pattern.findall(str(company_title_temp))[0]
            company_title = company_title.replace('<!-- -->', '')
            salary_temp = vacancy_soup.find('span', {'data-qa': 'vacancy-salary-compensation-type-net'})
            salary = salary_pattern.findall(str(salary_temp))
            salary = ''.join(salary)
            final_data.append(
                {'vacancy_title': vacancy_title, 'company_title': company_title, 'salary': salary, 'url': vacancy_url})
            salary = salary if salary != '' else 'Не указана'
            print(vacancy_title)
            print(company_title)
            print(salary)
            print(url)
        else:
            pass
    with open('output_file.json', 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(final_data, indent=4))

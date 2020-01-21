from itertools import count
from terminaltables import AsciiTable
from dotenv import load_dotenv
import os
import requests


def predict_salary(salary_from, salary_to, currency):
    if currency != 'rub' and currency != 'RUR':
        pass
    else:
        if salary_from and salary_to is not None:
            average_salary = (salary_from + salary_to) / 2
            return average_salary
        elif not salary_to:
            average_salary = salary_from * 1.2
            return average_salary
        elif not salary_from:
            average_salary = salary_to * 0.8
            return average_salary


def get_sj_api(url, headers, name):
    average_all = []
    per_page = 0
    for page in count(0):
        response = requests.get(url=url, headers=headers,
                                params={'keyword': name, 'count': 20, 'town': 4, 'page': page})
        response.raise_for_status()
        response_api = response.json()
        pages = response_api['total'] / 20
        per_page += 1
        if page >= pages:
            break

        for item in response_api['objects']:
            average_all.append(predict_salary(item['payment_from'], item['payment_to'], item['currency']))

    average_salary = sum(average_all) / len(average_all)

    vacancy_data = {"vacancies_found": response_api['total'],
                    "vacancies_processed": len(average_all),
                    "average_salary": int(average_salary)}
    return vacancy_data


def get_hh_api(base_url, headers, name):
    vacancies = []
    average_all = []
    for page in count(0):
        page_response = requests.get(url=base_url, headers=headers,
                                     params={'text': name, 'area': 1, 'per_page': 100, 'period': 30,
                                             'page': page})
        page_response.raise_for_status()
        page_data = page_response.json()
        if page >= 19:
            break
        vacancies.append(page_data['items'])

    for vacancy in vacancies:
        for item in vacancy:
            if item['salary'] is not None:
                average_all.append(predict_salary(item['salary']['from'], item['salary']['to'],
                                                     item['salary']['currency']))
    average_clear = list(filter(None, average_all))
    average_all = sum(average_clear) / len(average_all)
    vacancy_data = {"vacancies_found": page_data['found'], "vacancies_processed": len(average_all),
                    "average_salary": int(average_all)}
    return vacancy_data


def main():
    load_dotenv(verbose=True)
    secret_key = os.getenv('SJ_SECRET_KEY')
    base_url_sj = 'https://api.superjob.ru/2.30/vacancies'
    base_url_hh = 'https://api.hh.ru/vacancies'
    headers_sj = {'X-Api-App-Id': secret_key}
    headers_hh = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    names = 'python', 'c', 'c#', 'c++', 'java', 'javascript', 'ruby', 'go', '1c'
    direct_sj = {}
    direct_hh = {}

    for name in names:
        direct_sj[name] = get_sj_api(base_url_sj, headers_sj, name)
        direct_hh[name] = get_hh_api(base_url_hh, headers_hh, name)

    title = 'SuperJob Moscow'
    VACANCY_TABLE = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
        ['python', direct_sj['python']['vacancies_found'], direct_sj['python']['vacancies_processed'],
         direct_sj['python']['average_salary']],
        ['c', direct_sj['c']['vacancies_found'], direct_sj['c']['vacancies_processed'],
         direct_sj['c']['average_salary']],
        ['c#', direct_sj['c#']['vacancies_found'], direct_sj['c#']['vacancies_processed'],
         direct_sj['c#']['average_salary']],
        ['c++', direct_sj['c++']['vacancies_found'], direct_sj['c++']['vacancies_processed'],
         direct_sj['c++']['average_salary']],
        ['java', direct_sj['java']['vacancies_found'], direct_sj['java']['vacancies_processed'],
         direct_sj['java']['average_salary']],
        ['javascript', direct_sj['javascript']['vacancies_found'], direct_sj['javascript']['vacancies_processed'],
         direct_sj['javascript']['average_salary']],
        ['ruby', direct_sj['ruby']['vacancies_found'], direct_sj['ruby']['vacancies_processed'],
         direct_sj['ruby']['average_salary']],
        ['go', direct_sj['go']['vacancies_found'], direct_sj['go']['vacancies_processed'],
         direct_sj['go']['average_salary']],
        ['1c', direct_sj['1c']['vacancies_found'], direct_sj['1c']['vacancies_processed'],
         direct_sj['1c']['average_salary']],
    ]
    table_instance = AsciiTable(VACANCY_TABLE, title)
    print(table_instance.table)

    title = 'Headhunter Moscow'
    VACANCY_TABLE = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
        ['python', direct_hh['python']['vacancies_found'], direct_hh['python']['vacancies_processed'],
         direct_hh['python']['average_salary']],
        ['c', direct_hh['c']['vacancies_found'], direct_hh['c']['vacancies_processed'],
         direct_hh['c']['average_salary']],
        ['c#', direct_hh['c#']['vacancies_found'], direct_hh['c#']['vacancies_processed'],
         direct_hh['c#']['average_salary']],
        ['c++', direct_hh['c++']['vacancies_found'], direct_hh['c++']['vacancies_processed'],
         direct_hh['c++']['average_salary']],
        ['java', direct_hh['java']['vacancies_found'], direct_hh['java']['vacancies_processed'],
         direct_hh['java']['average_salary']],
        ['javascript', direct_hh['javascript']['vacancies_found'], direct_hh['javascript']['vacancies_processed'],
         direct_hh['javascript']['average_salary']],
        ['ruby', direct_hh['ruby']['vacancies_found'], direct_hh['ruby']['vacancies_processed'],
         direct_hh['ruby']['average_salary']],
        ['go', direct_hh['go']['vacancies_found'], direct_hh['go']['vacancies_processed'],
         direct_hh['go']['average_salary']],
        ['1c', direct_hh['1c']['vacancies_found'], direct_hh['1c']['vacancies_processed'],
         direct_hh['1c']['average_salary']],
    ]

    table_instance = AsciiTable(VACANCY_TABLE, title)
    print(table_instance.table)


if __name__ == '__main__':
    main()

from itertools import count
from terminaltables import AsciiTable
from dotenv import load_dotenv
import os
import requests


def predict_salary(salary_from, salary_to, currency):
    if not currency == 'rub' and not currency == 'RUR':
        return
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
    all_average_salary = []
    per_page = 0
    for page in count(0):
        response = requests.get(url=url, headers=headers,
                                params={'keyword': name, 'count': 20, 'town': 4, 'page': page})
        response.raise_for_status()
        api_response = response.json()
        pages = api_response['total'] / 20
        per_page += 1
        if page >= pages:
            break

        for item in api_response['objects']:
            all_average_salary.append(predict_salary(item['payment_from'], item['payment_to'], item['currency']))

    average_salary = sum(all_average_salary) / len(all_average_salary)

    vacancy_data = {"vacancies_found": api_response['total'],
                    "vacancies_processed": len(all_average_salary),
                    "average_salary": int(average_salary)}
    return vacancy_data


def get_hh_api(base_url, headers, name):
    vacancies = []
    average_salary = []
    for page in count(0):
        page_response = requests.get(url=base_url, headers=headers,
                                     params={'text': name, 'area': 1, 'per_page': 100, 'period': 30,
                                             'page': page})
        page_response.raise_for_status()
        api_response = page_response.json()
        if page >= 19:
            break
        vacancies.append(api_response['items'])

    for vacancy in vacancies:
        for item in vacancy:
            if item['salary'] is not None:
                average_salary.append(predict_salary(item['salary']['from'], item['salary']['to'],
                                                     item['salary']['currency']))
    average_clear = list(filter(None, average_salary))
    all_average_salary = sum(average_clear) / len(average_salary)
    vacancy_data = {"vacancies_found": api_response['found'], "vacancies_processed": len(average_salary),
                    "average_salary": int(all_average_salary)}
    return vacancy_data


def main():
    load_dotenv(verbose=True)
    secret_key = os.getenv('SJ_SECRET_KEY')
    base_url_sj = 'https://api.superjob.ru/2.30/vacancies'
    base_url_hh = 'https://api.hh.ru/vacancies'
    headers_sj = {'X-Api-App-Id': secret_key}
    headers_hh = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    languages = ['python', 'c', 'c#', 'c++', 'java', 'javascript', 'ruby', 'go', '1c']
    direct_sj = {}
    direct_hh = {}

    vacancy_sj_table = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    vacancy_hh_table = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]

    for language in languages:
        direct_sj[language] = get_sj_api(base_url_sj, headers_sj, language)
        vacancy_sj_table.append(
            [language, direct_sj[language]['vacancies_found'], direct_sj[language]['vacancies_processed'],
             direct_sj[language]['average_salary']])
        direct_hh[language] = get_hh_api(base_url_hh, headers_hh, language)
        vacancy_hh_table.append(
            [language, direct_hh[language]['vacancies_found'], direct_hh[language]['vacancies_processed'],
             direct_hh[language]['average_salary']])

    sj_title = 'SuperJob Moscow'
    hh_title = 'Headhunter Moscow'

    table_instance = AsciiTable(vacancy_sj_table, sj_title)
    print(table_instance.table)

    table_instance = AsciiTable(vacancy_hh_table, hh_title)
    print(table_instance.table)


if __name__ == '__main__':
    main()

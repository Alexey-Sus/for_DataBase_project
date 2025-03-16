import os

import dotenv

from class_DBManager import DBManager
from data_to_db import create_database_and_tables
from get_data_API import HHEmployerAPI, HHVacancyAPI
from refactor_API_data import create_shortened_list_of_vacancies

dotenv.load_dotenv()

host = str(os.getenv("HOST"))
port = str(os.getenv("PORT"))
database = str(os.getenv("DATABASE"))
user_name = str(os.getenv("USER_NAME"))
password = str(os.getenv("PASSWORD"))

# создаем общий экземпляр класса для тестирования и вывода на экран соотв. данных
class_DB = DBManager()

# экземпляры классов для получения данных по API:

hh_vac = HHVacancyAPI()
hh_empl = HHEmployerAPI()

vacancies: list = create_shortened_list_of_vacancies(hh_vac.get_vacancies())
employers: list = hh_empl.get_employers()

create_database_and_tables(
    database, user_name, password, host, port, vacancies, employers
)
print('Список компаний и количество открытых вакансий в них: ')
print(class_DB.get_companies_and_vacancies_count())
print()

print('Список вакансий (компания, должность, URL): ')
print(class_DB.get_all_vacancies())
print()

print('Средняя зарплата по вакансиям: ')
print(class_DB.get_avg_salary())
print()

print('Вакансии с зарплатой выше средней: ')
print(class_DB.get_vacancies_with_higher_salary())
print()

print(class_DB.get_vacancies_with_keyword())

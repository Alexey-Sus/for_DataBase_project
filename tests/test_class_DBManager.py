from src.class_DBManager import DBManager
import os
import dotenv

dotenv.load_dotenv()

host = str(os.getenv("HOST"))
port = str(os.getenv("PORT"))
database = str(os.getenv("DATABASE"))
user_name = str(os.getenv("USER_NAME"))
password = str(os.getenv("PASSWORD"))

def test_get_companies_and_vacancies_count():
    ''' Функция для тестирования метода поиска вакансий в БД: название компании
     и количество открытых вакансий по ней '''

    class_inst_1 = DBManager(host, port, database, user_name, password)
    s_input_1:str = class_inst_1.get_companies_and_vacancies_count()

    start_marker: str = "5. "
    end_marker: str = "6. "

    start_index: int = s_input_1.find(start_marker)
    end_index: int = s_input_1.find(end_marker)

    start_position: int = start_index + len(start_marker)
    extracted_string: str = s_input_1[start_position:end_index].strip()
    assert extracted_string == "'Адильахунова', вакансий: 1."

def test_get_all_vacancies():
    ''' Функция для тестирования метода поиска вакансий в БД: название компании,
     должность и URL вакансии '''

    class_inst_2 = DBManager(host, port, database, user_name, password)
    s_input_2: str = class_inst_2.get_all_vacancies()

    start_marker: str = "1. "
    end_marker: str = "2. "

    start_index: int = s_input_2.find(start_marker)
    end_index: int = s_input_2.find(end_marker)

    start_position: int = start_index + len(start_marker)
    extracted_string: str = s_input_2[start_position:end_index].strip()
    assert extracted_string == ("'Easy Recruit', должность: Кладовщик на склад Премиум товаров, "
                                "URL вакансии: https://hh.ru/vacancy/118905953")

def test_get_avg_salary():
    ''' Функция для тестирования метода вычисления средней зарплаты '''

    class_inst_3 = DBManager(host, port, database, user_name, password)
    assert class_inst_3.get_avg_salary() == '1174134 руб.'

def test_get_vacancies_with_higher_salary():
    ''' Функция для тестирования метода поиска вакансий с зарплатой выше средней '''

    class_inst_4 = DBManager(host, port, database, user_name, password)
    assert class_inst_4.get_vacancies_with_higher_salary() == ("1. 'Водитель персональный', зарплата: 5000000\n"
                                                                "2. 'Водитель в туризме', зарплата: 5000000\n")

def test_get_vacancies_with_keyword():
    ''' Функция для тестирования метода поиска вакансий по ключевому слову. Запрашивает ввод ключевого слова
     два раза: в первый раз для тестирования вводим "Оператор", а второй - "Президент" '''

    class_inst_5 = DBManager(host, port, database, user_name, password)
    expected_string_1: str = ("Вакансии со словом \"Оператор\" в названии: \n1. Оператор call-центра, "
                            "компания: \"АО Асакабанк\", URL вакансии: https://hh.ru/vacancy/118165551\n")

    expected_string_2: str = "Вакансий со словом 'Президент' не найдено."

    assert class_inst_5.get_vacancies_with_keyword() == expected_string_1
    assert class_inst_5.get_vacancies_with_keyword() == expected_string_2





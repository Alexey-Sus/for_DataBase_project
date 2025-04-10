import psycopg2
import os
import dotenv

dotenv.load_dotenv()

host = str(os.getenv("HOST"))
port = str(os.getenv("PORT"))
database = str(os.getenv("DATABASE"))
user_name = str(os.getenv("USER_NAME"))
password = str(os.getenv("PASSWORD"))

class DBManager:
    """Класс для подключения к БД и получения из неё некоторой информации
    В классе соединение с БД открывается в методе __init__ и закрывается только
    в методе, который вызывается последним, поскольку необходимо выполнить по
    очереди все методы, и для них соединение должно оставаться открытым."""

    def __init__(self, host, port, database, user_name, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user_name
        self.password = password

        try:
            self.conn = psycopg2.connect(
                dbname=self.database, user=self.user, password=self.password,
                host=self.host, port=self.port
            )
            self.cursor = self.conn.cursor()

        except psycopg2.Error as err:
            print(f"Error connecting to database {self.database}: {err}")
            self.conn = None
            self.cursor = None

    def get_companies_and_vacancies_count(self) -> str:
        """Получение списка всех компаний и количества
        вакансий у каждой компании"""
        # query: str = 'SELECT name, open_vacancies FROM public."EMPLOYERS"'

        query: str = ('SELECT v.employer_name, e.open_vacancies FROM public."EMPLOYERS" '
                      'AS e JOIN public."VACANCIES" AS v ON v.employer_id = e.employer_id')

        self.cursor.execute(query)

        results_interm = self.cursor.fetchall()
        index: int = 0
        new_str: str = ''
        for result in results_interm:
            index += 1
            new_str += (str(index) + '. ' + "'" + str(result[0]) +
                        "'" + ', вакансий: ' + str(result[1]) + '. ' '\n')
        self.conn.commit()
        return new_str

    def get_all_vacancies(self) -> str:
        """Получение списка всех вакансий с указанием названия компании,
        названия вакансии и ссылки на вакансию"""

        query: str = ('SELECT e.name, v.title, v.vacancy_url FROM public."VACANCIES" AS v JOIN public."EMPLOYERS" AS e'
                      ' ON v.employer_id = e.employer_id')

        self.cursor.execute(query)
        results_interm = self.cursor.fetchall()
        index: int = 0
        new_str = ''
        for result in results_interm:
            index += 1
            new_str += (str(index) + '. ' + "'" + str(result[0]) + "'" + ', должность: '
                        + str(result[1]) + ', URL вакансии: ' + str(result[2]) + '\n')

        self.conn.commit()
        return new_str

    def get_avg_salary(self) -> str:
        """Получение средней зарплаты по вакансиям"""
        query: str = 'SELECT AVG(salary) AS average_salary FROM public."VACANCIES";'

        self.cursor.execute(query)
        results = self.cursor.fetchall()
        self.conn.commit()
        return str(int(results[0][0])) + ' руб.'

    def get_vacancies_with_higher_salary(self) -> str:
        """Получение списка всех вакансий, у которых зарплата выше
        средней по всем вакансиям"""
        query: str = """SELECT title, salary
                    FROM public."VACANCIES"
                    WHERE salary > (SELECT AVG(salary) FROM public."VACANCIES");"""

        self.cursor.execute(query)
        results_interm = self.cursor.fetchall()
        index: int = 0
        new_str = ''
        for result in results_interm:
            index += 1
            new_str += (str(index) + '. ' + "'" + str(result[0]) + "'" + ", зарплата: " + str(result[1]) + '\n')

        self.conn.commit()
        return new_str

    def get_vacancies_with_keyword(self) -> str:
        """Получение списка всех вакансий, в названии которых содержатся
        переданные в метод слова, например, Python"""
        self.keyword = str(
            input("Введите слово или слова для поиска в названии вакансии: ")
        )
        query: str = 'SELECT TITLE, EMPLOYER_NAME, VACANCY_URL FROM public."VACANCIES" WHERE TITLE LIKE %s'
        pattern: str = f"%{self.keyword}%"
        self.cursor.execute(query, (pattern,))

        results_interm = self.cursor.fetchall()
        self.conn.commit()
        # self.cursor.close()
        # self.conn.close()
        if results_interm:
            index: int = 0
            new_str = ''
            for result in results_interm:
                index += 1
                new_str += (str(index) + '. ' + str(result[0])
                            + ', компания: "' + str(result[1])
                            + '", URL вакансии: ' + str(result[2]) + '\n')
            return f'Вакансии со словом "{self.keyword}" в названии: ' + "\n" + new_str
        else:
            return f"Вакансий со словом '{self.keyword}' не найдено."
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    s = DBManager(host, port, database, user_name, password)
    print(s.get_companies_and_vacancies_count())
    print()
    print(s.get_all_vacancies())
    print()
    print(s.get_avg_salary())
    print()
    print(s.get_vacancies_with_higher_salary())
    print()
    print(s.get_vacancies_with_keyword())
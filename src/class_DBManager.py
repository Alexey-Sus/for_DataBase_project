import psycopg2

class DBManager:
    """Класс для подключения к БД и получения из неё некоторой информации
    В классе соединение с БД открывается в методе __init__ и закрывается только
    в методе, который вызывается последним, поскольку необходимо выполнить по
    очереди все методы, и для них соединение должно оставаться открытым."""

    def __init__(
        self,
        dbname="ttttt",
        user="postgres",
        password="ghtytGFD45DFVGT",
        host="localhost",
        port="5432",
    ):
        """Инициализация экземпляров класса сразу с параметрами подключения к БД"""
        try:
            self.conn = psycopg2.connect(
                dbname=dbname, user=user, password=password,
                host=host, port=port
            )
            self.cursor = self.conn.cursor()

        except psycopg2.Error as err:
            print(f"Error connecting to database {dbname}: {err}")
            self.conn = None
            self.cursor = None

    def get_companies_and_vacancies_count(self) -> str:
        """Получение списка всех компаний и количества
        вакансий у каждой компании"""
        query: str = 'SELECT name, open_vacancies FROM public."EMPLOYERS"'

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

        query: str = 'SELECT employer_name, title, vacancy_url FROM public."VACANCIES"'

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
        self.cursor.close()
        self.conn.close()
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


if __name__ == "__main__":
    s = DBManager()
    print(s.get_companies_and_vacancies_count())
    print()
    print(s.get_all_vacancies())
    print()
    print(s.get_avg_salary())
    print()
    print(s.get_vacancies_with_higher_salary())
    print()
    print(s.get_vacancies_with_keyword())
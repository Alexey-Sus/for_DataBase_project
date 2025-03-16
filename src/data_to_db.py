from builtins import len, list, print

import psycopg2

from get_data_API import HHEmployerAPI, HHVacancyAPI
from refactor_API_data import create_shortened_list_of_vacancies


def create_database_and_tables(dbname: str, user: str, password: str, host: str, port: str, vac_list: list,
                               empl_list: list) -> str:
    """Функция создает базу данных, если она еще не создана, и две таблицы в ней. Заполняет таблицы
    данными из списка вакансий и списка работодателей. Если БД создана, ф-ия создает в ней 2 таблицы
    и заносит в нее данные из списков."""

    try:
        conn = psycopg2.connect(
            dbname="postgres",  # подключаемся к заведомо существующей базе данных, чтобы проверить наличие других БД
            user=user,
            password=password,
            host=host,
            port=port,
        )
        conn.autocommit = True

        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
        exists = cur.fetchone() is not None

        if not exists:
            cur.execute(f"CREATE DATABASE {dbname}")
            cur.close()  # закрываем соединение с базой данных postgres, чтобы открыть соединение с другой БД
            conn.close()  # закрываем соединение с базой данных postgres, чтобы открыть соединение с другой БД

            conn = psycopg2.connect(
                dbname=dbname,
                # подключаемся к заведомо существующей базе данных, чтобы проверить наличие других БД
                user=user,
                password=password,
                host=host,
                port=port,
            )
            conn.autocommit = True
            cur = conn.cursor()

            if vac_list:
                column_defs: str = ""
                for key in vac_list[0].keys():
                    if str(key) == "salary":
                        column_defs = column_defs + " " + key + " " + "INT,"
                    else:
                        column_defs = column_defs + " " + key + " " + "TEXT,"

                column_defs = column_defs[1: len(column_defs) - 1]
                columns = list(vac_list[0].keys())

                create_table_query = (
                    f'CREATE TABLE IF NOT EXISTS "VACANCIES" ({column_defs})'
                )
                cur.execute(create_table_query)

                for vacancy in vac_list:
                    values = []

                    for col in columns:
                        values.append(str(vacancy[col]))

                    placeholders = ", ".join(["%s"] * len(columns))
                    insert_query = f'INSERT INTO "VACANCIES" ({(", ").join(columns)}) VALUES ({placeholders})'
                    cur.execute(insert_query, values)

            if empl_list:
                column_defs = ""
                for key in empl_list[0].keys():
                    if str(key) == "open_vacancies":
                        column_defs += " " + key + " " + "INT,"
                    else:
                        column_defs += " " + key + " " + "TEXT,"

                column_defs = column_defs[1: len(column_defs) - 1]
                columns = list(empl_list[0].keys())

                create_table_query = (
                    f'CREATE TABLE IF NOT EXISTS "EMPLOYERS" ({column_defs})'
                )
                cur.execute(create_table_query)

                for empl in empl_list:
                    values = []

                    for col in columns:
                        values.append(str(empl[col]))

                    placeholders = ", ".join(["%s"] * len(columns))
                    insert_query = f'INSERT INTO "EMPLOYERS" ({(", ").join(columns)}) VALUES ({placeholders})'
                    cur.execute(insert_query, values)

            cur.close()
            conn.close()
            return f"Database {dbname} hasnt existed but created AND two tables have been created and populated"

        else:
            conn.close()  # закрываем подключение к общей базе данных и подключаемся к БД,
            # имя которой передали в функцию
            conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
            conn.autocommit = True
            cur = conn.cursor()

            # проверяем, существует ли таблица VACANCIES. Если да, в нее ничего не пишем.
            # это делается для того, чтобы избежать записи одинаковых строк в таблицу
            # при множественном выполнении кода.
            table_exists_query = ("SELECT 1 FROM pg_tables WHERE "
                                  "schemaname = 'public' AND tablename = 'VACANCIES';")
            cur.execute(table_exists_query)
            table_exists = cur.fetchone()

            if not table_exists:
                if vac_list:
                    column_defs = ""
                    for key in vac_list[0].keys():
                        if str(key) == "salary":
                            column_defs = column_defs + " " + key + " " + "INT,"
                        else:
                            column_defs = column_defs + " " + key + " " + "TEXT,"

                    column_defs = column_defs[1: len(column_defs) - 1]
                    columns = list(vac_list[0].keys())

                    create_table_query = (
                        f'CREATE TABLE IF NOT EXISTS "VACANCIES" ({column_defs})'
                    )
                    cur.execute(create_table_query)

                    for vacancy in vac_list:
                        values = []

                        for col in columns:
                            values.append(str(vacancy[col]))

                        placeholders = ", ".join(["%s"] * len(columns))
                        insert_query = f'INSERT INTO "VACANCIES" ({(", ").join(columns)}) VALUES ({placeholders})'
                        cur.execute(insert_query, values)

            # проверяем, существует ли таблица EMPLOYERS. Если да, в нее ничего не пишем.
            # это делается для того, чтобы избежать записи одинаковых строк в таблицу
            # при множественном выполнении кода.
            table_exists_query = ("SELECT 1 FROM pg_tables WHERE "
                                  "schemaname = 'public' AND tablename = 'EMPLOYERS';")
            cur.execute(table_exists_query)
            table_exists = cur.fetchone()

            if not table_exists:
                if empl_list:
                    column_defs = ""
                    for key in empl_list[0].keys():
                        if str(key) == "open_vacancies":
                            column_defs += " " + key + " " + "INT,"
                        else:
                            column_defs += " " + key + " " + "TEXT,"

                    column_defs = column_defs[1: len(column_defs) - 1]
                    columns = list(empl_list[0].keys())

                    create_table_query = (
                        f'CREATE TABLE IF NOT EXISTS "EMPLOYERS" ({column_defs})'
                    )
                    cur.execute(create_table_query)

                    for empl in empl_list:
                        values = []

                        for col in columns:
                            values.append(str(empl[col]))

                        placeholders = ", ".join(["%s"] * len(columns))
                        insert_query = f'INSERT INTO "EMPLOYERS" ({(", ").join(columns)}) VALUES ({placeholders})'
                        cur.execute(insert_query, values)

            cur.close()
            conn.close()
            return f"Database {dbname} HAS EXISTED already AND two tables have been created and populated"

    except psycopg2.Error as e:
        return f"Error checking database existence: {e}"

    # finally:
    #     if conn == True:
    #         conn.close()


if __name__ == "__main__":
    hh_api = HHVacancyAPI()
    hh_empl = HHEmployerAPI()

    # получаем список вакансий в виде словаря, для дальнейшей его передачи в функцию базы данных
    vacancies = hh_api.get_vacancies()
    salaries = create_shortened_list_of_vacancies(vacancies)

    # ...и получаем список работодателей, для передачи его в функцию базы данных
    employers = hh_empl.get_employers()

    # вводим все нужные переменные для подключения к базе данных
    host = "localhost"
    port = "5432"
    database = "ttttt"
    user_name = "postgres"
    password = "ghtytGFD45DFVGT"

    print(
        create_database_and_tables(
            database, user_name, password, host, port, salaries, employers
        )
    )

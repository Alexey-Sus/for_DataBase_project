from src.data_to_db import create_database_and_tables
from src.get_data_API import HHEmployerAPI, HHVacancyAPI
from src.refactor_API_data import create_shortened_list_of_vacancies

import os
import dotenv

dotenv.load_dotenv()

host = str(os.getenv("HOST"))
port = str(os.getenv("PORT"))
database = str(os.getenv("DATABASE"))
user_name = str(os.getenv("USER_NAME"))
password = str(os.getenv("PASSWORD"))

def test_data_to_db():
    empl_inst = HHEmployerAPI()
    vac_inst = HHVacancyAPI()

    vac_list = create_shortened_list_of_vacancies(vac_inst.get_vacancies())
    empl_list = empl_inst.get_employers()

    s = create_database_and_tables(database, user_name, password, host, port, vac_list, empl_list)

    assert s == (f"Database {database} and the two tables HAVE EXISTED already, so no data population"
                        f" has been executed")
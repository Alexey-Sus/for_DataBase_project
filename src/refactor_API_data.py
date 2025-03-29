from builtins import dict, list, len, print, isinstance
from get_data_API import HHVacancyAPI


def create_shortened_list_of_vacancies(vac_list: list) -> list:
    """Функция для выборки из данных API только необходимых данных и создания списка данных на основе этого.
    Данные: title, salary, employer_id, employer_name, requirement, respons-ties, work_format, empl_form
    """

    salaries: list = []

    for vacancy in vac_list:
        dict_sal: dict = {}
        dict_sal["title"] = vacancy.get("name")

        if isinstance(vacancy["salary"], dict):
            dict_sal["salary"] = vacancy.get("salary", {}).get("from", {})
            if isinstance(dict_sal["salary"], int):
                pass
            else:
                dict_sal["salary"] = 0
        else:
            dict_sal["salary"] = 0

        dict_sal["employer_id"] = vacancy.get("employer", {}).get("id", {})
        dict_sal["employer_name"] = vacancy.get("employer", {}).get("name", {})
        dict_sal["requirements"] = vacancy.get("snippet", {}).get("requirement", {})
        dict_sal["responsibilities"] = vacancy.get("snippet", {}).get(
            "responsibility", {}
        )
        dict_sal["vacancy_URL"] = vacancy.get("alternate_url", {})

        if "work_format" in vacancy:
            if len(vacancy["work_format"]) > 0:
                dict_sal["work_format"] = vacancy["work_format"][0].get("name", {})
            else:
                dict_sal["work_format"] = "No Data"
        else:
            dict_sal["work_format"] = "No Data"

        dict_sal["employment_form"] = vacancy.get("employment_form", {}).get("name", {})
        salaries.append(dict_sal)
    return salaries


if __name__ == "__main__":

    # cоздаем экземпляр класса HHVacancyAPI
    hh_api = HHVacancyAPI()
    vacancies: list = create_shortened_list_of_vacancies(hh_api.get_vacancies())

    print("Список вакансий:")
    for vacancy in vacancies:
        print(vacancy)

    print(create_shortened_list_of_vacancies({}))

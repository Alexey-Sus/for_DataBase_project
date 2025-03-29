from abc import ABC, abstractmethod
from builtins import dict, list, str

import requests


class AbstractVacEmplAPI(ABC):
    """Абстрактный класс для наследования другими классами"""

    @abstractmethod
    def get_vacancies(self) -> list:
        """Шаблон для метода получения вакансий - исп-ся в дочернем классе"""
        pass

    @abstractmethod
    def get_employers(self) -> list:
        """Шаблон для метода получения данных о работодателе - для дочернего класса"""
        pass


class HHVacancyAPI(AbstractVacEmplAPI):
    """Класс для получения вакансий по API hh.ru. Наследуется от AbstractVacEmplAPI"""

    def get_employers(self):
        pass

    def get_vacancies(self) -> list:
        """Метод для получения raw-списка вакансий от hh.ru"""

        url = "https://api.hh.ru/vacancies?per_page=10"
        response = requests.get(url)
        if response.status_code == 200:
            vacancies = response.json()
            return vacancies.get("items", [])
        return []


class HHEmployerAPI(AbstractVacEmplAPI):
    """Класс для получения данных работод. по API hh.ru. Наследуется от AbstractVacancyAPI"""

    def get_vacancies(self):
        pass

    def get_employers(self) -> list:
        """Метод для получения raw-словарика данных по работодателям от hh.ru"""

        list_empl_ids: list[str] =['540381', '4128276', '1781787', '9513229', '10952595', '3093585',
                                   '3959796', '827187', '11545019']

        list_empl: list = []

        for id in list_empl_ids:

            url = "https://api.hh.ru/employers/" + id
            response = requests.get(url)
            if response.status_code == 200:
                employer = response.json()

                empl_dict: dict = {}

                empl_dict["employer_id"] = employer.get("id")
                empl_dict["name"] = employer.get("name")
                empl_dict["type"] = employer.get("type")
                empl_dict["open_vacancies"] = employer.get("open_vacancies")
                list_empl.append(empl_dict)


        return list_empl


if __name__ == "__main__":
    hh_empl = HHEmployerAPI()
    print(hh_empl.get_employers())
    print()

    hh_vac = HHVacancyAPI()
    print(hh_vac.get_vacancies())

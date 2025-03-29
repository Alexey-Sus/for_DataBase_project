from src.refactor_API_data import create_shortened_list_of_vacancies
from src.get_data_API import HHVacancyAPI

def test_test_create_shortened_list_of_vacancies():

    class_inst = HHVacancyAPI()
    vacancies: list = class_inst.get_vacancies()

    string_to_compare: str = 'Кладовщик на склад Премиум товаров'

    assert create_shortened_list_of_vacancies(vacancies)[0].get('title') == string_to_compare
    assert create_shortened_list_of_vacancies([]) == []
    assert create_shortened_list_of_vacancies({}) == []




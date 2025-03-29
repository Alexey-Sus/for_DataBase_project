from src.get_data_API import HHEmployerAPI, HHVacancyAPI

def test_get_data_API():

    class_inst_empl = HHEmployerAPI()
    class_inst_vac = HHVacancyAPI()

    assert class_inst_empl.get_employers()[0].get('name') == 'Easy Recruit'
    assert class_inst_vac.get_vacancies()[0].get('area').get('name') == 'Дмитров (Московская область)'
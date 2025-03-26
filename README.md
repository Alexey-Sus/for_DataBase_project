This is a project for a homework related to databases.

What is inside:

1. get_data_API.py module: it connects to the hh.ru API and extracts some data on vacancies and companies.
2. refactor_API_data.py: this module shortens the list of vacancies obtained in the get_data_API.py module
   to make it easier to read and simpler.
3. data_to_db.py. This module creates a database and two tables in it locally: tables 'VACANCIES' and 'EMPLOYERS'.
   Then it populates the two tables with the lists of vacancies and companies, respectively, which were obtained during
   steps 1 to 2.
4. class_DBManager.py: this module extracts some data from the two PostreSQL tables, according to the instructions set out
   in the initial description of the task. The operations are done with standard SQL queries.
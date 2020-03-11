from connector import Connect
from configurator import Configurator
from executor import Execute


def run(data):
    """Собираем все вместе, реализован только первый тестовый случай, когда хотим подсчитать
    число строк в таблицах"""
    data_connect = Configurator(data)
    if data_connect.get_test_case():
        db = data_connect.get_database()
        sv = data_connect.get_server()
        connection = Connect(sv, db, data)
        connection.queries_count()
        x = Execute(data)
        x.parse_test_files()


if __name__ == '__main__':
    run('row_count')

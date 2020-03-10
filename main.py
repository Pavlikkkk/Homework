from connector import Connect
from configurator import Configurator
from executor import Execute
from report import Result


def run():
    data_connect = Configurator()
    db = data_connect.get_database()
    sv = data_connect.get_server()
    connection = Connect(sv, db)
    connection.queries_count()

    x = Execute()
    x.parse_test_files()


if __name__ == '__main__':
    run()
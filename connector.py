import pyodbc
from configurator import Configurator
import json


class Connect(Configurator):
    """Подключается к mssql, наследует все от конфигуратора"""

    def __init__(self, server, database, test_case):
        """коннектится к mssql через pyodbc"""
        super().__init__(test_case)
        try:
            self.server = server
            self.database = database
            self.trusted_con = 'yes'
            self.conn = pyodbc.connect('Driver={SQL Server};'
                                       'Server=' + self.server + ';'
                                       'Database=' + self.database + ';'
                                       'Trusted_Connection=' + self.trusted_con + ';')
            self.list = {}
            self.tables = self.queries_source()
            self.output_directory = Configurator.get_output_directory(self)
            self.cursor = self.conn.cursor()
        except pyodbc.DatabaseError as err:
            print('problem with connection DB')

    def queries_source(self):
        """Находит нужные нам таблицы в системной таблице mssql"""
        cursor = self.conn.cursor()
        cursor.execute(
            "select top(3) SCHEMA_NAME(schema_id), name, schema_id from sys.all_objects s where s.type = 'U' and "
            "schema_id > 8")
        tables = cursor.fetchall()
        return tables

    def queries_count(self):
        """Подсчитывает кол-во строк во всех таблицах и
        возвращает результат в json фаил"""
        # cursor = self.conn.cursor()
        for i in range(len(self.tables)):
            self.cursor.execute("select count(*) from {}.{}".format(self.tables[i][0], self.tables[i][1]))
            res = self.cursor.fetchone()
            self.list.update({self.tables[i][1]: res[0]})
        with open(self.output_directory, 'w') as output:
            json.dump(self.list, output)
        return 'Json file was created in {}'.format(self.output_directory)


if __name__ == '__main__':
    x = Connect(r'EPBYGOMW001A\SQL17', 'AdventureWorks2017', 'row_count')
    print(x.queries_count())

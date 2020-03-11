import os
import json
from configurator import Configurator
import logging


def logger_decorator(method):
    """Создает лог фаил и записывает туда результат метода """

    def wrapper(self):
        logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s", filename="result/result.log",
                            level=logging.INFO)
        logging.info("Test started")
        method(self)
        logging.info("Test finished")
        return "Log file was added"

    return wrapper


class Execute(Configurator):
    """Выполняет проверку"""

    def __init__(self, test_case):
        super().__init__(test_case)
        self.list_files = []
        self.directory = Configurator.get_directory(self)  # r'd:/Python_framework/test_files/'
        self.output_directory = Configurator.get_output_directory(self)

    @logger_decorator
    def parse_test_files(self):
        """Сравнивает json file из db с тестовым json """
        try:
            with open(self.output_directory) as out:
                data = json.load(out)
            for j, v in data.items():
                for i in os.listdir(self.directory):
                    with open(os.path.join(self.directory, i)) as f:
                        file = json.load(f)
                    for k, s in file.items():
                        if j == file[k]['table'] and v == int(s['expected_result']):
                            logging.info('Success for {}, actual result: {}, '
                                         'expected result {}'.format(file[k]['table'], v, s['expected_result']))
                        elif j == file[k]['table'] and v != int(s['expected_result']):
                            logging.info('Fail for {}, actual result: {}, '
                                         'expected result {}'.format(file[k]['table'], v, s['expected_result']))

        except Exception as e:
            logging.info(e)


if __name__ == '__main__':
    x = Execute('row_count')

    print(x.parse_test_files())

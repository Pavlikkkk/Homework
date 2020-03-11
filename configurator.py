import json


class Configurator:

    def __init__(self, test_case):
        with open('config.json') as f:
            self.config = json.load(f)
        self.test_case = test_case

    def get_database(self):
        return self.config[self.test_case]['database']

    def get_server(self):
        return self.config[self.test_case]['server']

    def get_directory(self):
        return self.config[self.test_case]['directory']

    def get_output_directory(self):
        return self.config[self.test_case]['output_directory']

    def get_test_case(self):
        return self.config[self.test_case]


if __name__ == '__main__':
    x = Configurator('row_count')
    print(x.get_test_case())



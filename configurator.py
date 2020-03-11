import json


class Configurator:

    def __init__(self):
        with open('config.json') as f:
            self.config = json.load(f)

    def get_database(self):
        return self.config['dev']['database']

    def get_server(self):
        return self.config['dev']['server']

    def get_directory(self):
        return self.config['dev']['directory']

    def get_output_directory(self):
        return self.config['dev']['output_directory']


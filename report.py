import logging
from executor import Execute


class Result:
    def __init__(self):
        logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s", filename="result/result.log",
                            level=logging.INFO)

    def Logging(self):
        logging.info("Test started")
        res = Execute()
        res.parse_test_files()
        logging.info("Test finished")


if __name__ == '__main__':
    x = Result()
    x.Logging()

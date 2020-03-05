#!/usr/bin/env python

import pyodbc
import os
import shutil as sh
from pathlib import Path
from xml.dom import minidom
import collections
import re


class ReadFiles:
    """ Только читает файлы в указанной директории"""

    def __init__(self, directory, directory_files_incorrect):
        self.directory = directory
        self.filtering = []
        self.directory_files_incorrect = directory_files_incorrect
        self.list_for_insert = []

    def check_move_files(self):
        """Проверяет формат fb2 и убирает несоответсвующие файлы в другую папку"""
        try:
            global a
            p = Path(self.directory_files_incorrect)
            p.mkdir(exist_ok=True)  # позволяет избежать исключения если папка существует
            for i in os.listdir(self.directory):
                if i.endswith('.fb2'):
                    a = os.path.join(self.directory, i)
                else:
                    a = os.path.join(self.directory, i)
                    sh.move(a, os.path.join(p, i))
            return 'Files were checked, incorrect files were removed in {}'.format(self.directory_files_incorrect)
        except Exception as e:
            print(e)


class ConnectionDB:
    """коннектится к mssql через pyodbc"""

    def __init__(self):
        self.server = r'EPBYGOMW001A\SQL17'
        self.database = 'AdventureWorks2017'
        self.trusted_con = 'yes'
        self.conn = pyodbc.connect('Driver={SQL Server};'
                                   'Server=' + self.server + ';'
                                                             'Database=' + self.database + ';'
                                                                                           'Trusted_Connection=' + self.trusted_con + ';')


class ParseFiles(ReadFiles, ConnectionDB):
    """ Читает и парсит файлы в указанной директории"""

    def __init__(self, directory, directory_files_incorrect):
        ReadFiles.__init__(self, directory, directory_files_incorrect)
        ConnectionDB.__init__(self)

    def parser_xml(self):
        """Парсит фаил и достает book_name, number_of_paragraph, number_of_words,
         number_of_letters, words_with_capital_letters, words_in_lowercase,
         word, count, count_uppercase"""
        try:
            d_lower = {}
            d_upper = {}

            self.check_move_files()  # чтобы не делать сначало проверку, а потом парсинг
            for i in os.listdir(self.directory):
                path = os.path.join(self.directory, i)
                tree = minidom.parse(path)
                tag = tree.getElementsByTagName('book-title')[0]
                book_name = tag.firstChild.data
                paragraph = tree.getElementsByTagName('body')[0]
                counter = collections.Counter()
                for i in paragraph.childNodes:
                    counter[i.nodeName] += 1
                # исходил из того, что каждая секция это параграф, просто подсчитал секции
                count_paragraph = counter['section']

                count_words = 0
                count_words2 = collections.Counter()
                counter_letters = 0
                counter_upper_words = 0
                count_up_word = collections.Counter()
                counter_lower_words = 0

                words = tree.getElementsByTagName('p')

                for i in words:
                    exp = re.findall(r'[^<emphasis>]\w+', str(i.firstChild.nodeValue))
                    for each_word in exp:
                        count_words += 1
                        count_words2[each_word] += 1
                        counter_letters += len(each_word)
                    exp2 = re.findall(r'[А-Я]\w+', str(i.firstChild.nodeValue))
                    for each_up_word in exp2:
                        counter_upper_words += 1
                        count_up_word[each_up_word] += 1
                    exp3 = re.findall(r'(?<= )+[а-я]+\b', str(i.firstChild.nodeValue))
                    for each_low_word in exp3:
                        counter_lower_words += 1

                for key, value in count_words2.items():  # данные из counter переношу в dictionary
                    d_lower[key] = value

                for key, value in count_up_word.items():
                    d_upper[key] = value

                cnt_lo = [(key, value) for key, value in d_lower.items()]  # создаю список для буд вставки
                cnt_up = [(key, value) for key, value in d_upper.items()]

                self.list_for_insert.append(book_name)
                self.list_for_insert.append(count_paragraph)
                self.list_for_insert.append(count_words)
                self.list_for_insert.append(counter_letters)
                self.list_for_insert.append(counter_upper_words)
                self.list_for_insert.append(counter_lower_words)
        except Exception as e:
            print(e)

        # таблицы заранее создал в mssql

        try:
            cursor = self.conn.cursor()
            cursor.execute("insert into AdventureWorks2017.dbo.homework1("
                           "book_name, count_paragraph, count_words, count_letter, "
                           "count_upper, count_lower) VALUES(?,?,?,?,?,?)",
                           self.list_for_insert[0], self.list_for_insert[1], self.list_for_insert[2],
                           self.list_for_insert[3], self.list_for_insert[4], self.list_for_insert[5])

            cursor.executemany("insert into AdventureWorks2017.dbo.homework1_2(word,counts) VALUES(?,?)", cnt_up)
            cursor.executemany("insert into AdventureWorks2017.dbo.homework1_2(word, counts ) VALUES(?,?)", cnt_lo)
            self.conn.commit()

        except pyodbc.DatabaseError as err:
            self.conn.rollback()
            print('Failed to insert data')
        finally:
            self.conn.close()

        return self.list_for_insert, cnt_up, cnt_lo


if __name__ == '__main__':
    x = ParseFiles(r'd:\Python_hometask\input_files', r'd:/Python_hometask/incorrect_input_folder/')

    print(x.parser_xml())

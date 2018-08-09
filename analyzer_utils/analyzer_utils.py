# coding: utf-8

import os.path
from os import mkdir
from datetime import datetime
from nltk import pos_tag


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word], tagset='universal')
    return pos_info[0][1] == 'VERB'


def split_snake_case_name_to_words(name):
    return [n for n in name.split('_') if n]


class Logger:
    '''
    For creating and dumping logs
    '''
    __logger_instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__logger_instance is None:
            cls.__logger_instance = object.__new__(cls, *args, **kwargs)
        return cls.__logger_instance

    def __init__(self):
        self.temp_file_name = Logger._get_temp_file_name()

    def _dump_message(self, text_msg, type_msg):
        with open(self.temp_file_name, mode='a', encoding='utf-8') as file_handler:
            file_handler.write('{}: {}\n'.format(type_msg, text_msg))

    def info(self, message):
        self._dump_message(Logger._get_text_message(message), 'INFO')

    def warning(self, message):
        self._dump_message(Logger._get_text_message(message), 'WARN')

    @classmethod
    def _get_text_message(cls, message):
        return '{} - {}'.format(datetime.now().strftime('%H:%M:%S'), message)

    @classmethod
    def _get_temp_file_name(cls):
        base_path = os.path.dirname(os.path.dirname(__file__))
        temp_path = os.path.join(base_path, 'logs')
        file_name = 'analyzer_log_{}.txt'.format(datetime.now().strftime('%Y_%m_%d'))
        if not os.path.exists(temp_path):
            mkdir(temp_path)
        return os.path.join(temp_path, file_name)

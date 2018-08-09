# coding: utf-8

import os
import ast
import sys
import collections
from optparse import OptionParser
from analyzer_utils import analyzer_utils as utils
from nltk import download
download('averaged_perceptron_tagger')
download('universal_tagset')


def get_trees(path):
    logger = utils.Logger()
    file_names = get_file_names_list_in_path(path)
    trees = []
    for file_name in file_names:
        try:
            with open(file_name, 'r', encoding='utf-8') as attempt_handler:
                main_file_content = attempt_handler.read()
            trees.append(ast.parse(main_file_content))
        except (SyntaxError, UnicodeDecodeError) as e:
            logger.warning('{}: {}'.format(os.path.abspath(file_name), e))
    return trees


def get_file_names_list_in_path(path):
    file_names = []
    for dir_name, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                file_names.append(os.path.join(dir_name, file))
    logger = utils.Logger()
    logger.info('total {} files in path {}'.format(len(file_names), os.path.abspath(path)))
    return file_names


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_all_function_names(tree):
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def get_names_in_path(path, func_names_getter):
    trees = get_trees(path)
    return [f for f in utils.flat([func_names_getter(t) for t in trees]) if not (f.startswith('__') and f.endswith('__'))]


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if utils.is_verb(word)]


def get_all_words_in_path(path):
    attribute_names = get_names_in_path(path, get_all_names)
    return utils.flat([utils.split_snake_case_name_to_words(attribute_name) for attribute_name in attribute_names])


def get_top_verbs_in_path(path, top_size=None):
    func_names = get_names_in_path(path, get_all_function_names)
    verbs = utils.flat([get_verbs_from_function_name(function_name) for function_name in func_names])
    return collections.Counter(verbs).most_common(top_size)


def get_top_functions_names_in_path(path, top_size=None):
    func_names = get_names_in_path(path, get_all_function_names)
    return collections.Counter(func_names).most_common(top_size)


def main(path_list, top_size=None):
    logger = utils.Logger()
    for path in path_list:
        verbs = get_top_verbs_in_path(path, top_size)
        message = '{}:\n    total {} words, {} unique'.format(os.path.abspath(path), len(verbs), len(set(verbs)))
        logger.info(message)
        print(message)
        for word, occurrence in verbs:
            message = 'word: {}, occurrence: {}'.format(word, occurrence)
            logger.info(message)
            print(message)


if __name__ == '__main__':
    argument_val = sys.argv
    opt_parser = OptionParser()
    opt_parser.add_option("-s", "--size", dest="top_size",
                          help="size of most common results from the request", type="int",
                          default=None)

    options, arguments = opt_parser.parse_args(argument_val)
    main(arguments, top_size=options.top_size)

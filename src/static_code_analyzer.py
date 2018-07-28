import ast
import os
import collections

from nltk import pos_tag


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def get_trees(path, with_file_names=False, with_file_content=False):
    file_names = []
    trees = []
    for dir_name, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                file_names.append(os.path.join(dir_name, file))
                if len(file_names) == 100:
                    break
    print('total %s files' % len(file_names))
    for file_name in file_names:
        with open(file_name, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            tree = None
        if with_file_names:
            if with_file_content:
                trees.append((file_name, main_file_content, tree))
            else:
                trees.append((file_name, tree))
        else:
            trees.append(tree)
    print('trees generated')
    return trees


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_all_function_names(tree):
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def get_names_in_path(path, func_names_getter):
    trees = get_trees(path)
    return [f for f in flat([func_names_getter(t) for t in trees]) if not (f.startswith('__') and f.endswith('__'))]


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_all_words_in_path(path):
    attribute_names = get_names_in_path(path, get_all_names)

    def split_snake_case_name_to_words(name):
        return [n for n in name.split('_') if n]

    return flat([split_snake_case_name_to_words(attribute_name) for attribute_name in attribute_names])


def get_top_verbs_in_path(path, top_size=10):
    func_names = get_names_in_path(path, get_all_function_names)
    print('functions extracted')
    verbs = flat([get_verbs_from_function_name(function_name) for function_name in func_names])
    return collections.Counter(verbs).most_common(top_size)


def get_top_functions_names_in_path(path, top_size=10):
    func_names = get_names_in_path(path, get_all_function_names)
    return collections.Counter(func_names).most_common(top_size)


if __name__ == '__main__':
    wds = []
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]
    for project in projects:
        __path = os.path.join('.', project)
        wds += get_top_verbs_in_path(__path)

    __top_size = 200
    print('total %s words, %s unique' % (len(wds), len(set(wds))))
    for _word, _occurrence in collections.Counter(wds).most_common(__top_size):
        print(_word, _occurrence)

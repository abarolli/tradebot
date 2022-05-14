import os
from typing import Any, Callable, Iterable, Mapping
from ruamel.yaml import YAML


def read(file_path:str, fn:Callable=None) -> Any:
    '''
    'file_path' represents the file to be read.
    'fn' is an optional function that will have the raw file
    contents passed to it. The functions return value is what
    will be returned, rather than the raw data.
    '''
    abs_path = os.path.abspath(file_path)
    with open(abs_path) as _file:
        data = _file.read()
    
    if fn:
        return fn(data)

    return data


def join(*args:Iterable[str]) -> str:
    '''
    Joins and normalizes a sequence of string paths
    '''
    return os.path.normpath(os.path.join(*args))


def yml_to_dict(data:str) -> dict:
    yaml = YAML()
    return yaml.load(data)


def update_yml(_file:str, new_data:Mapping[str, str]):
    yaml = YAML()
    _file = os.path.normpath(os.path.abspath(_file))
    with open(_file, 'w') as out_file:
        yaml.dump(new_data, out_file)
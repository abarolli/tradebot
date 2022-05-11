import os
from typing import Any, Callable, Iterable
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
    return os.path.normpath(os.path.join(*args))


def yml_to_dict(data:str) -> dict:
    yaml = YAML()
    return yaml.load(data)
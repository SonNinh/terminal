#!/usr/bin/env python3
from glob import glob


def globbing(string):
    """
    take a string, split it up, the first element is command, next are argument
    @parameter: string
    @return: string
    """
    token_list = string.split()
    command = token_list[0]
    for token in token_list[1:]:
        path_name_list = glob(token)
        for path_name in path_name_list:
            command += '\n' + path_name
    return command

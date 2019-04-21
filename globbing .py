#!/usr/bin/env python3
from re import findall, match, split
from glob import glob


def get_token_list(input_from_command_line):
    """
    get input string from command and split it up into tokens.
    A token is a none-space string if it begin with a word
    Else, if it begin with a [backquote, single quote, double quote], it will
    end with the next [backquote, single quote, double quote]
    @para: string
    @return: list
    """
    token = "[^ ]*[`\'\"][^ ].*?[`\'\"][^ ]*|[^ ]*"
    token_list = findall(token, input_from_command_line)
    while '' in token_list:
        token_list.remove('')
    return token_list



def get_possible_name(path_name_list):
    path_name_dictionary = {}
    for path_name in path_name_list:
        path_name_dictionary[path_name] = '\n'.join(glob(path_name))
    return path_name_dictionary


def main():
    args = "echo \"asddasd\""
    print(get_token_list(args))


if __name__ == '__main__':
    main()

from dollar_sign import *
from back_slash import *
from single_quote import *
from double_quote import *
from anything_else import *
from sys import stdout
from globbing import *


def check_dollar(string):
    """
    check if there's a dollar in string and whether it still working
    @parameter: string
    @return: Bol
    """
    string = str(string)
    for index, value in enumerate(string):
        if value == '$':
            if check_if_terminated_by_back_slash(index, string) is False:
                return True
    return False


def handle_string_in_double(working_area):
    """
    handle string in double_quote 1 time
    @parameter: string
    @return: string
    """
    object_list = []
    string = ''
    flag = 0
    while working_area != '':
        if working_area[0] == '\\':
            data = create_a_back_slash_object(working_area)
            try:
                object = data[0]
                string = string + '\"' + object.parsed_string + '\"'
            except TypeError:
                return None
        elif working_area[0] == '$':
            data = create_a_dollar_sign_object(working_area)
            try:
                object = data[0]
                if '$' in object.parsed_string:
                    string = string + object.parsed_string
                else:
                    string = string + '\"' + object.parsed_string + '\"'
            except TypeError:
                string = string + '\"' + data + '\"'
                return None
        else:
            data = create_an_anything_else_object(working_area, flag='d')
            try:
                object = data[0]
                string = string + '\"' + object.parsed_string + '\"'
            except TypeError:
                return None
        try:
            object_list.append([0])
            working_area = data[1]
        except IndexError:
            return None
    return string


def loop_in_double(working_area):
    """
    loop in double_quote to handle all unparsed metacharactor
    @parameter: string
    @return: string
    """
    while True:
        buffer = working_area
        data = handle_string_in_double(working_area)
        working_area = data
        if buffer != working_area:
            break
    return working_area



def handle_string(working_area):
    """
    try to create object, if there're only anything_else object
    are created, return the message to anounce that this is the last
    level to dig in
    @parameter: string
    @return: list
    """
    flag = 0
    object_list = []
    parsed_string = ''
    while working_area != '':
        if working_area[0] == '\'':
            name = '\''
            data = create_a_single_quote_object(working_area)
            try:
                parsed_string = parsed_string + '\'' + data[0].parsed_string + '\''
            except TypeError:
                return '>'
            flag += 1
        elif working_area[0] == '\"':
            name = '\"'
            data = create_a_double_quote_object(working_area)
            try:
                string_in_double_quote = loop_in_double(data[0].parsed_string)
                parsed_string = parsed_string + string_in_double_quote
            except TypeError:
                return '>'
            flag += 1
        elif working_area[0] == '\\':
            data = create_a_back_slash_object(working_area)
            try:
                parsed_string = parsed_string + '\'' + data[0].parsed_string + '\''
            except TypeError:
                return '>'
            flag += 1
        elif working_area[0] == '$':
            name = '}'
            data = create_a_dollar_sign_object(working_area)
            if check_dollar(data[0].parsed_string) is False:
                try:
                    parsed_string = parsed_string + '\'' + data[0].parsed_string + '\''
                except TypeError:
                    return '>'
            else:
                try:
                    parsed_string = parsed_string + data[0].parsed_string
                except TypeError:
                    return '>'
            flag += 1
        else:
            data = create_an_anything_else_object(working_area, flag='f')
            try:
                parsed_string = parsed_string + '\'' + data[0].parsed_string + '\''
            except TypeError:
                return '>'
        object_list.append(data[0])
        working_area = data[1]
    return parsed_string, object_list


def get_dollar_object_number(object_list):
    """
    get the object list, return number of dollar_sign
    @parameter: list
    @return: int
    """
    dollar_sign_number = 0
    for object in object_list:
        if object.name == 'dollar_sign':
            dollar_sign_number += 1
    return dollar_sign_number


def remove_all_single_and_double_quote(working_area):
    """
    take the string after parsing, remove all single and double quote
    return the string
    @parameter: string
    @return: string
    """
    parsed_string = ''
    object_list = []
    while working_area != '':
        if working_area[0] == '\'':
            data = create_a_single_quote_object(working_area)
            object_list.append(data[0])
            working_area = data[1]
        elif working_area[0] == '\"':
            data = create_a_double_quote_object(working_area)
            object_list.append(data[0])
            working_area = data[1]
        else:
            break
    for object in object_list:
        parsed_string = parsed_string + object.parsed_string
    return parsed_string


def handle_assignment_command(string):
    """
    take command and return if it's a assignment or not
    @parameter: string
    @return: Bol
    """
    pattern = findall('[a-zA-Z]*=[a-zA-Z0-9]*', string)
    if pattern:
        return True
    return False


def handle_input(working_area):
    """
    loop in string to handle metacharactor
    @parameter: string
    @return: string
    """
    try:
        if working_area != '':
            first_token = working_area.split(' ')[0]
            if handle_assignment_command(first_token) is False:
                while True:
                    data = handle_string(working_area)
                    working_area = data[0]
                    if get_dollar_object_number(data[1]) == 0:
                        break
                return globbing(remove_all_single_and_double_quote(working_area))
            else:
                open_and_write_to_a_file(working_area)
                return ''
        return ''
    except Exception:
        return '>'

x=input()
print(handle_input(x))

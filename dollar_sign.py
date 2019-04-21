from re import search
from os import environ
from double_quote import check_if_terminated_by_back_slash
from parameter_dictionary import *

class Dollar_sign:
    def __init__(self, unparsed_string):
        """
        unparsed_string : $qwejkqwhe or ${qweqwe : nbnfbmfd}
        variables is list of variable which come from asign statement
        """
        self.name = 'dollar_sign'
        self.unparsed_string = unparsed_string
        self.string_type = self.remove_dollar_sign()
        self.tokens = self.get_tokens(self.unparsed_string)
        self.parameter = self.tokens[0]
        self.operator = self.tokens[1]
        self.word = self.tokens[2]
        self.parameter_status = self.get_parameter_status(self.parameter)
        self.parameter_value = self.get_parameter_value(self.parameter,
                                                        self.parameter_status)
        self.parsed_string = self.get_parsed_string(self.tokens,
                                                    self.parameter_status,
                                                    self.parameter_value)
        if self.parsed_string == None:
            self.parsed_string = ''

    def get_parsed_string(self, tokens, parameter_status, parameter_value):
        """
        get the final value after parse the string input base on parameter's status
        @para: string, string
        @return: string
        """
        parameter = tokens[0]
        operator = tokens[1]
        word = tokens[2]
        if word is not None:
            return self.handle_expansion(tokens,
                                         parameter_status,
                                         parameter_value)
        else:
            return parameter_value

    def remove_dollar_sign(self):
        """
        modify the unparsed string, remove the bracket from string, return
        it type and value
        type 1 :  ${le:=anh} ${leanh}
        type 2 :  $leanh
        after modify:
        type 1 : le:=anh leanh
        type 2 : leanh
        """
        if self.unparsed_string[1] == '{':
            self.unparsed_string = self.unparsed_string[2:-1]
            return '1'
        else:
            self.unparsed_string = self.unparsed_string[1:]
            return '2'

    def get_tokens(self, unparsed_string):
        """
        divide string into 3 part: parameter, word, and operator
        @parameter: string
        @return: tuple
        """
        try:
            parameter = search('.*?[:#%+-=?]', unparsed_string).group()[:-1]
            mark = len(parameter)
            if unparsed_string[mark] == ':':
                if unparsed_string[mark + 1] in ['+', '-', '=', '?']:
                    word = unparsed_string[mark + 2:]
                    operator = unparsed_string[mark:mark + 2]
                else:
                    word = unparsed_string[mark + 1:]
                    operator = unparsed_string[mark]
            elif unparsed_string[mark] in ['%', '#']:
                if unparsed_string[mark + 1] == unparsed_string[mark]:
                    word = unparsed_string[mark + 2:]
                    operator = unparsed_string[mark:mark + 2]
                else:
                    word = unparsed_string[mark + 1:]
                    operator = unparsed_string[mark]
            else:
                word = unparsed_string[mark + 1:]
                operator = unparsed_string[mark]
            return parameter, operator, word
        except AttributeError:
            parameter = unparsed_string
            operator = None
            word = None
            return parameter, operator, word

    def get_parameter_status(self, parameter):
        """
        Check parameter and return it's status.
        If the status is Set and Not Null, return its value
        @parameter: string
        @return: string
        """
        parameter_dictionary = get_parameter_dictionary()
        if parameter not in environ.keys():
            if parameter not in parameter_dictionary.keys():
                return 'Unset'
            else:
                if parameter_dictionary[parameter] == '':
                    return 'Set But Null'
                else:
                    value = parameter_dictionary[parameter]
                    return 'Set and Not Null'
        else:
            if environ[parameter] == '':
                return 'Set But Null'
            else:
                value = environ[parameter]
                return 'Set and Not Null'

    def get_parameter_value(self, parameter, parameter_status):
        """
        take a parameter, find in environment and variable_dictionary, return
        its value
        @parameter: string
        @return: string
        """
        parameter_dictionary = get_parameter_dictionary()
        if parameter_status != 'Unset':
            try:
                return environ[parameter]
            except KeyError:
                return parameter_dictionary[parameter]
        else:
            return None

    def handle_expansion(self, tokens, parameter_status, parameter_value):
        parameter = tokens[0]
        operator = tokens[1]
        word = tokens[2]
        if operator == ':-':
            if parameter_status == 'Set But Null':
                return word
            elif parameter_status == 'Unset':
                return word
            else:
                return parameter_value
        elif operator == '-':
            if parameter_status == 'Set and Not Null':
                return parameter_value
            elif parameter_status == 'Set But Null':
                return None
            elif parameter_status == 'Unset':
                return word
        elif operator == ':=':
            if parameter_status == 'Set and Not Null':
                return parameter_value
            elif parameter_status == 'Set But Null':
                open_and_write_to_a_file(self.parameter, word)
                return word
            elif parameter_status == 'Unset':
                open_and_write_to_a_file(self.parameter + '=' + word)
                return word
        elif operator == '=':
            if parameter_status == 'Set and Not Null':
                return parameter_value
            elif parameter_status == 'Set But Null':
                return None
            elif parameter_status == 'Unset':
                open_and_write_to_a_file(self.parameter + '=' + word)
                return word
        elif operator == ':?':
            if parameter_status == 'Set and Not Null':
                return parameter_value
            elif parameter_status == 'Set But Null':
                return 'Error'
            elif parameter_status == 'Unset':
                return 'Error'
        elif operator == '?':
            if parameter_status == 'Set and Not Null':
                return parameter_value
            elif parameter_status == 'Set But Null':
                return None
            elif parameter_status == 'Unset':
                return 'Error'
        elif operator == ':+':
            if parameter_status == 'Set and Not Null':
                return word
            elif parameter_status == 'Set But Null':
                return None
            elif parameter_status == 'Unset':
                return None
        elif operator == '+':
            if parameter_status == 'Set and Not Null':
                return word
            elif parameter_status == 'Set But Null':
                return word
            elif parameter_status == 'Unset':
                return None


def handle_bracket(working_area):
    """
    create a object that has bracket
    @parameter: string
    @return: object, string
    """
    left_flag = 1
    right_flag = 0
    string = working_area[2:]
    for index, value in enumerate(string):
        if value == '}':
            if check_if_terminated_by_back_slash(index, string) is False:
                right_flag += 1
        elif value == '{':
            left_flag += 1
        if left_flag == right_flag:
            unparsed_string = working_area[:index + 3]
            new_working_area = working_area[index + 3:]
            dollar = Dollar_sign(unparsed_string)
            return dollar, new_working_area


def handle_no_bracket(working_area):
    """
    create a object that has no bracket
    @parameter: string
    @return: object, string
    """
    for index, value in enumerate(working_area[1:]):
        if value in ['`', '\'', '\"', '$', '*', '?',
                     '\\', ' ', '[', ']', '', '{', '}']:
            unparsed_string = working_area[:index + 1]
            new_working_area = working_area[index + 1:]
            dollar = Dollar_sign(unparsed_string)
            return dollar, new_working_area
    unparsed_string = working_area
    dollar = Dollar_sign(unparsed_string)
    return dollar, ''


def create_a_dollar_sign_object(working_area):
    try:
        if working_area[1] == '{':
            return handle_bracket(working_area)
        else:
            return handle_no_bracket(working_area)
    except IndexError:
        return '$'

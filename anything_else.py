class Anything_else:
    def __init__(self, unparsed_string):
        self.name = 'anything_else'
        self.unparsed_string = unparsed_string
        self.parsed_string = self.unparsed_string


def create_an_anything_else_object(working_area, flag):
    if flag == 'd':
        stop_flag = ['\"', '\\', '$']
    else:
        stop_flag = ['`', '\'', '\"', '\\', '$', '']
    for index, value in enumerate(working_area):
        if index == len(working_area) - 1:
            anything_else = Anything_else(working_area)
            return anything_else, ''
        if value in stop_flag:
            anything_else = Anything_else(working_area[:index])
            new_working_area = working_area[index:]
            return anything_else, new_working_area

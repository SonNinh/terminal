class Double_quote:
    def __init__(self, unparsed_string):
        self.name = 'double_quote'
        self.unparsed_string = unparsed_string
        self.parsed_string = self.unparsed_string[1:-1]


def check_if_terminated_by_back_slash(current, working_area):
    """
    only used for the second double quote
    """
    current -= 1
    flag = 0
    while current >= 0:
        if working_area[current] == '\\':
            flag += 1
            current -= 1
        else:
            break
    if flag % 2 == 1:
        return True
    return False


def create_a_double_quote_object(working_area):
    """
    create a double quote object, new_working_area and return a new
    working_area
    """
    flag = 0
    for index, value in enumerate(working_area[1:]):
        if value == '\"':
            if check_if_terminated_by_back_slash(index, working_area[1:]) is False:
                if flag == 0:
                    new_working_area = working_area[index + 2:]
                    double_quote = Double_quote(working_area[0:index + 2])
                    return double_quote, new_working_area
    return False

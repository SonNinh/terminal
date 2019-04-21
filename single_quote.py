class Single_quote:
    def __init__(self, unparsed_string):
        self.name = 'single_quote'
        self.unparsed_string = unparsed_string
        self.parsed_string = self.unparsed_string[1:-1]


def create_a_single_quote_object(working_area):
    """
    take a working_area and return a new working_area
    first element often is a sing quote or space
    """
    for index, value in enumerate(working_area[1:]):
        if value == '\'':
            new_working_area = working_area[index + 2:]
            unparsed_string = working_area[0:index + 2]
            return Single_quote(unparsed_string), new_working_area

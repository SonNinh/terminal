class Back_slash:
    def __init__(self, unparsed_string):
        self.name = 'back_slash'
        self.unparsed_string = unparsed_string
        self.parsed_string = self.unparsed_string[1:]

    def handle_input(self):
        pass


def create_a_back_slash_object(working_area):
    """
    create a new back slash object an return new working_area
    if there's no charactor after the Back_slash, return Error
    """
    try:
        new_working_area = working_area[2:]
        return Back_slash(working_area[0:2]), new_working_area
    except IndexError:
        new_working_area = working_area[1:]
        return Back_slash(working_area[0]), new_working_area

from re import findall


def open_and_write_to_a_file(string):
    data = findall('[a-zA-Z]*=[a-zA-Z0-9]*', string)
    data = data[0].split('=')
    parameter = data[0]
    value = data[1]
    parameter_dictionary = get_parameter_dictionary()
    parameter_dictionary[parameter] = value
    f = open('variable_dictionary', 'w+')
    for item in parameter_dictionary.items():
        f.write(item[0] + '=' + item[1] + '\n')
    f.close()


def get_parameter_dictionary():
    parameter_dictionary = {}
    f = open('variable_dictionary', 'r')
    data = f.read()
    line_list = findall('[a-zA-Z]*=[a-zA-Z0-9]*', data)
    for line in line_list:
        line = line.split('=')
        parameter_dictionary[line[0]] = line[1]
    f.close()
    return parameter_dictionary

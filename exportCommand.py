from os import environ


def getVariableAndValue(varAndVal):
    # split varAndVal into variable's name and its value
    posOfEqual = varAndVal.find('=')
    if posOfEqual < 0:
        # if there is no '='
        variable = varAndVal
        value = ''
    elif posOfEqual == len(varAndVal)-1:
        # if '=' is at the end
        variable = varAndVal[:posOfEqual]
        value = ''
    else:
        # if '=' is at the begining or the middle
        variable = varAndVal[:posOfEqual]
        value = varAndVal[posOfEqual+1:]

    return variable, value


def export(inputMessage):
    '''
    @param:
        inputMessage: list of all args, without command name 'exit'
    '''
    for arg in inputMessage:
        variable, value = getVariableAndValue(arg)

        if variable:
            # if variable is not none
            if variable[0] >= '0' and variable[0] <= '9':
                # the first character of variable is numeric
                return "export: `{}\': not a valid identifie".format(arg)
            else:
                environ[variable] = value
        else:
            return "export: `{}\': not a valid identifie".format(arg)

    return ''

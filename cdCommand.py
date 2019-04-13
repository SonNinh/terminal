import os


def isExistedFile(pathName):
    return os.path.isfile(pathName)


def isExistedDir(pathName):
    return os.path.isdir(pathName)


def analysePath(inputMessage):
    targetRealPath = os.environ['PWD']
    targetPath = inputMessage[0]
    lsOfStepPaths = targetPath.split('/')
    error = ''

    if lsOfStepPaths[-1] == '':
        lsOfStepPaths.pop(-1)

    for i, step in enumerate(lsOfStepPaths):
        if step == '~' and i == 0:
            # '~' cannot be in the middle or the end of the target path
            try:
                targetRealPath = os.environ['HOME']
            except KeyError:
                error = 'intek-sh: cd: HOME not set'
        elif step == '':
            targetRealPath = '/'
        elif step == '..':
            targetRealPath = os.path.dirname(targetRealPath)
        elif step == '.':
            pass
        elif isExistedDir(os.path.join(targetRealPath, step)):
            targetRealPath = os.path.join(targetRealPath, step)
        elif isExistedFile(os.path.join(targetRealPath, step)):
            targetRealPath = os.environ['PWD']
            error = 'intek-sh: cd: {}: Not a directory'.format(targetPath)
            break
        else:
            targetRealPath = os.environ['PWD']
            error = 'intek-sh: cd: {}: No such file or directory'.format(targetPath)
            break

    return targetRealPath, error


def chDir(inputMessage):
    '''
    @param:
        inputMessage: all input args without command name
        printErr: flag for error inform
    @ return:
        targetRealPath: the path which need to go to
        successfulFlag: True if change directory successfully, else False
    '''
    targetRealPath = os.environ['PWD']
    if inputMessage:
        # if there is at least 1 argument
        targetRealPath, error = analysePath(inputMessage)
    else:
        # if no argument
        try:
            targetRealPath = os.environ['HOME']
            error = ''
        except KeyError:
            # if environmet variable HOME was deleted
            error = 'intek-sh: cd: HOME not set'

    os.environ['PWD'] = targetRealPath
    os.chdir(targetRealPath)
    return error

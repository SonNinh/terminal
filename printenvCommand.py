from os import environ


def printEnv(lsOfArgs):
    if lsOfArgs:
        for arg in lsOfArgs:
            try:
                yield environ[arg] + '\n'
            except Exception:
                pass
    else:
        for env in environ:
            yield (env + '=' + environ[env] + '\n')

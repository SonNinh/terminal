from os import environ


def unset(lsOfUnset):
    for var in lsOfUnset:
        try:
            del environ[var]
        except KeyError:
            pass

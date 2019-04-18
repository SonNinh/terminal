
from re import findall, match, split
from glob import glob, iglob
from os import path
from os import environ

def complete(args, pos_cursor_str, environ):
    str_for_dynamic = ''
    len_of_input = len(args)
    start_idx = None
    ls_of_possible = []

    
    for i in range(pos_cursor_str-1, -len_of_input-1, -1):
        if args[i] == " ":
            if i != -1:
                if pos_cursor_str != 0:
                    str_for_dynamic = args[i+1:pos_cursor_str] + '*'
                else:
                    str_for_dynamic = args[i+1:] + '*'
                start_idx = i+1
                break
            else:
                str_for_dynamic = '*'
                break
        else:
            start_idx = -len(args)

    if pos_cursor_str != 0:
        str_for_parse = args[:pos_cursor_str]
    else:
        str_for_parse = args[:]
        
    ls_of_args = str_for_parse.split()
    if ls_of_args:
        if len(ls_of_args) == 1 and str_for_dynamic != '*':
            # search command in PATH
            str_for_dynamic = str_for_parse.strip() + '*'
            if 'PATH' in environ:
                for env_path in environ['PATH'].split(':'):
                    for cmd in iglob(path.join(env_path, str_for_dynamic)):
                        ls_of_possible.append(cmd[len(env_path)+1:])
        else:
            # search in cuurent directory
            for path_name in iglob(str_for_dynamic):
                if ls_of_args[0] == 'cd':
                    if path.isdir(path_name):
                        ls_of_possible.append(path_name + '/')
                else:
                    ls_of_possible.append(path_name)
    complt_str = ''
    if len(ls_of_possible) == 1:
        complt_str = ls_of_possible[0]
        ls_of_possible.clear()
    elif len(ls_of_possible) > 1:
        break_out = False
        try:
            for idx, ch in enumerate(ls_of_possible[0]):
                for pos in ls_of_possible[1:]:
                    if ch != pos[idx]:
                        break_out = True
                        break
                if break_out:
                    break
                complt_str += ch
        except IndexError:
            pass
    return start_idx, ls_of_possible, complt_str


# if __name__ == '__main__':
#     # asd = input()
#     print(complete("print ", 0, environ))

import collections
import argparse
import random
import re

from colorama import Fore, Style


COLOR_LIST = [
        [ n for n in range(31, 37 + 1) ],
        [ n for n in range(90, 97 + 1) ]
    ]
VIOLET = [
        'elif', 'if', 'else', 'try', 'except', 'pass', 'return', 'with', 'def', 'while', 'for', 'in'
    ]

BLUE = [
        'print', 'open', 'enumerate', 'len'
    ]

def file_IO(fpath: str) -> list:
    with open(fpath, 'rt', encoding='utf-8') as f:
        data = f.readlines()

    return data


def function_display(fpath: str, func: str) -> None:
    data = file_IO(fpath)

    ok = False
    for idx, i in enumerate(data):
        i = i.replace('\n', '')
        if f'def {func}' in i:
            i = i.replace(f'{func}',
                          f'{Fore.GREEN}{func}{Style.RESET_ALL}')
            ok = True
        if '# endfunction' in i:
            ok = False

        if ok:
            for built in VIOLET:
                if built == 'in' and ('print' in i or 'join' in i):
                    continue
                if built == 'if' and ('hexlify' in i):
                    continue
                i = i.replace(built, f'\033[35m{built}\033[0m')
            for built in BLUE:
                i = i.replace(built, f'\033[34m{built}\033[0m')
            prn = ''
            single_chk = True
            double_chk = True
            for offset, c in enumerate(i):
                if c == '\'' and single_chk:
                    prn += '\033[33m'
                    prn += c
                    single_chk = False
                elif c == '\'' and not single_chk:
                    prn += c
                    prn += '\033[0m'
                    single_chk = True
                elif c == '"' and double_chk:
                    prn += '\033[33m'
                    prn += c
                    double_chk = False
                elif c == '"' and not double_chk:
                    prn += c
                    prn += '\033[0m'
                    double_chk = True
                else:
                    prn += c

            for offset, c in enumerate(prn):
                if c == '\'' and single_chk:
                    single_chk = False
                elif c == '\'' and not single_chk:
                    single_chk = True

                if not single_chk:
                    if prn[offset:offset + 12] == '\x1b[35mfor\x1b[0m':
                        prn = prn.replace('\x1b[35mfor\x1b[0m', 'for')
            print(idx, prn)
            

def function_call_display(fpath:str, func: str) -> None:
    data = file_IO(fpath)

    for idx, i in enumerate(data):
        if func in i and not 'def' in i:
            print(idx, i.replace('\n', '').strip(), '\n')


def variable_display(fpath: str, var: str) -> None:
    data = file_IO(fpath)

    function_color = collections.defaultdict(int)
    function_color['None'] = 31
    function = 'None'
    for idx, i in enumerate(data):
        if not re.match(r'^def[ ][A-Za-z0-9_]*', i) is None:
            function = re.match(r'^def[ ][A-Za-z0-9_]*', i).group().split(' ')[1]
            if not function in function_color:
                x = random.randint(0, 1)
                y = random.randint(0, len(COLOR_LIST[x]) - 1)
                function_color[function] = COLOR_LIST[x][y]

        if 'if __name__' in i:
            function = 'Main'
            if not function in function_color:
                x = random.randint(0, 1)
                y = random.randint(0, len(COLOR_LIST[x]) - 1)
                function_color[function] = COLOR_LIST[x][y]

        if '# endfunction' in i:
            function = 'None'
            print()

        if var in i:
            i = i.replace('\n', '').replace(var,
                                            f'{Fore.YELLOW}{var}{Style.RESET_ALL}')
            print(idx, f'-> \033[{function_color[function]}m{function}\033[0m ->', i.strip())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='file path', required=True)
    parser.add_argument('-fn', help='function name', required=False)
    parser.add_argument('-fc', help='function name', required=False)
    parser.add_argument('-vn', help='variable name', required=False)

    args = parser.parse_args()

    if args.fn:
        function_display(args.f, args.fn)
    elif args.fc:
        function_call_display(args.f, args.fc)
    else:
        variable_display(args.f, args.vn)
    

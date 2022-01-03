import oletools.olevba as vba

import argparse
import hashlib
import sys
import os


def parse(file: str) -> None:

    v = vba.VBA_Parser(file)
    if not v.detect_vba_macros():
        print('Macro is not detect')
        return None

    macro = v.extract_all_macros()
    print('Macro is detect!!!')
    print(f'Macro Path: {macro[0][1]}')
    
    try:
        file_name = file.split('.')[0]
    except Exception as e:
        file_name = file

    with open(f'{file_name}.vba.zz', 'w') as f:
        f.write(macro[0][3])

    file_size = os.path.getsize(f'{file_name}.vba.zz')
    md5 = hashlib.md5(macro[0][3].encode('utf-8')).hexdigest()
    sha256 = hashlib.sha256(macro[0][3].encode('utf-8')).hexdigest()
    sha512 = hashlib.sha512(macro[0][3].encode('utf-8')).hexdigest()

    print(f'[+] {macro[0][3]}')
    print('-----'*5+'\n')
    print(f'[+] {file_name}.vba.zz Stored')
    print(f'[+] {round(file_size/1024,0)}kb')
    print(f'[+] Macro Path: {macro[0][1]}')
    print(f'[+] md5: {md5}')
    print(f'[+] sha256: {sha256}')
    print(f'[+] sha512: {sha512}\n')
        

def main() -> int:

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='File Path', required=True)
    args_p = parser.parse_args()

    parse(args_p.f)

    return 0


if __name__ == '__main__':
    main()


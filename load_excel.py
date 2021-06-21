import mysql.connector
import argparse
import openpyxl
import sys
import re
import os


def db_check(args, conn) -> str:

    SQL = 'USE '

    if args.d is not None:
        SQL += str(args.d)

        cur = conn.cursor()

        try:
            cur.execute(SQL)
        except Exception as e:
            CREATE_DB = 'CREATE DATABASE {}'.format(args.d)
            cur.execute(CREATE_DB)
            print('[-] ' + str(sys.exc_info()[0] ) + str(e))
        
        conn.commit()

        return args.d

    else:
        pattern = re.compile('\w*.xlsx')
        file_name = pattern.findall(args.f)[0] .split('.')[0] 

        CREATE_DB = 'CREATE DATABASE {}'.format(file_name)
        
        cur = conn.cursor()

        try:
            cur.execute(CREATE_DB)
            print('[+] ' + str(CREATE_DB))
        except Exception as e:
            print('[-] ' + str(sys.exc_info()[0] ) + str(e))

        conn.commit()

        return file_name


def row_size(sheet, head_list) -> int:

    rows = 2
    columns = 1

    while True:
        check = 0

        for idx, i in enumerate(range(len(head_list))):
            if sheet.cell(row=rows, column=columns).value == None:
                check += 1

        if check == len(head_list):
            break
        else:
            rows += 1
            columns = 1
    
    return rows - 2


def excel_parse(args, conn, DB_name) -> int:
   
    wb = openpyxl.load_workbook(args.f)
    sheet = wb.active
    sheet_name = wb.sheetnames

    head_list = list()
    content_list = list()

    rows = 1
    columns = 1
    
    if (sheet.cell(row=1, column=1).value == None):
        return 1
    else:
        while sheet.cell(row=1, column=columns).value != None:
            head_list.append(sheet.cell(row=1, column=columns).value)
            columns += 1
            
    print(head_list)

    check = row_size(sheet, head_list)

    print(check)

    data_type = list()
    
    rows = 2 
    columns = 1
    for idx, i in enumerate(range(len(head_list))):
        int_check = 1 
        for j in range(check):
            try:
                int(sheet.cell(row=rows, column=columns).value)
            except Exception as e:
                int_check = 0
                break
            rows += 1

        if int_check == 1:
            data_type.append('int')
        else:
            max_size = 256
            for j in range(check):
                if max_size < len(sheet.cell(row=rows, column=columns).value):
                    max_size = len(sheet.cell(row=rows, column=columns).value)

            type_string = 'varchar({})'.format(int(max_size*1.2))
            data_type.append(type_string) 

        rows = 2
        columns += 1

    print(data_type)

    CREATE_TABLE_SQL = 'CREATE TABLE {}.{} ('.format(DB_name, sheet_name[0])

    cur = conn.cursor()
    
    for idx, head in enumerate(head_list):
        if idx == (len(head_list)-1):
            CREATE_TABLE_SQL += '{} {})'.format(head, data_type[idx])
        else:
            CREATE_TABLE_SQL += '{} {}, '.format(head, data_type[idx])

    try:
        cur.execute(CREATE_TABLE_SQL)
        print('[+] ' + str(CREATE_TABLE_SQL))
    except Exception as e:
        print('[-] ' + str(sys.exc_info()[0]) + str(e))

    conn.commit()

    rows = 2
    columns = 1

    for type_idx, i in enumerate(range(check)):
        INSERT_SQL = 'INSERT INTO {}.{} VALUES('.format(DB_name, sheet_name[0])
        check = 0
        for idx, j in enumerate(range(len(head_list))):
            if idx == (len(head_list) - 1):
                INSERT_SQL += '\'{}\')'.format(sheet.cell(row=rows, column=columns).value)
            else:
                INSERT_SQL += '\'{}\', '.format(sheet.cell(row=rows, column=columns).value)

            columns += 1

        else:
            try:
                cur.execute(INSERT_SQL)
                print('[+] ' + str(INSERT_SQL))
            except Exception as e:
                print('[-] ' + str(sys.exc_info()[0]) + str(e))
            rows += 1
            columns = 1

    conn.commit()
    wb.close()
    
    return 0


def mysql_connect(args):

    try:
        conn = mysql.connector.connect(
            host = args.host,
            port = args.port,
            user = args.u,
            passwd = args.p
        ) 
    except Exception as e:
        print('Connect Error')
   
    DB_name = db_check(args, conn) 
    excel_parse(args, conn, DB_name)
    
    conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='host', required=True)
    parser.add_argument('--port', help='Default 3306', default=3306, required=False)
    parser.add_argument('-u', help='User', required=True)
    parser.add_argument('-p', help='Password', required=True)
    parser.add_argument('-d', help='Select DB', required=False)
    parser.add_argument('-t', help='Table Name Default excel file name', required=False)
    parser.add_argument('-f', help='excel file path', required=True)

    args = parser.parse_args()

    mysql_connect(args)


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

    SQL = 'CREATE TABLE {}.{} ('.format(DB_name, sheet_name[0] )

    print(SQL)

    cur = conn.cursor()

    try:
        cur.execute(SQL)
        print('[+] ' + str(SQL))
    except Exception as e:
        print('[-] ' + str(sys.exc_info()[0] ) + str(e))

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


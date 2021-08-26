import requests
import hashlib
import sqlite3
import py7zr
import time
import os

cuckoo_API = "Bearer <cuckoo API>"

url_send_file = "http://192.168.106.128:8090/tasks/create/file"
header = {"Authorization" : cuckoo_API}
dir_path = "./"


def status_print(file_name):
    print(file_name, end=' ', flush=True)
    for t in range(1, 10+1):
        print("{}% ".format(t*10), end='', flush=True)
        time.sleep(30)
    print()


def file_extract():
    file_list = os.listdir(dir_path)

    for file in file_list:
        try:
            with py7zr.SevenZipFile(file, mode='r', password="<password>") as z:
                z.extractall()
        except:
            continue


def file_transfer():
    file_lists = os.listdir(dir_path)

    for file in file_lists:
        status = "{} ".format(file)
        try:
            extension = file.split('.')[1]

            if extension == "exe":
                f = open(file, "rb")
                f_data = f.read()

                res = requests.post(url_send_file, headers=header, files={"file":
                                (str(hashlib.sha256(f_data).hexdigest()) + '.' +
                                 extension, f_data)})

                f.close()

                print(res.json()["task_id"], end=' ')
                status_print(file)

        except:
            f = open(file, "rb")
            f_data = f.read()

            res = requests.post(url_send_file, headers=header, files={"file":
                            (str(hashlib.sha256(f_data).hexdigest()), f_data)})

            f.close()

            print(res.json()["task_id"], end=' ')
            status_print(file)


def report_download():

    for idx in range(1, 471+1):
        url = f'http://192.168.106.128:8090/tasks/report/{i}'

        res = requests.get(url, headers=header)
        
        file_name = res.json()['target']['file']['sha256']

        with open(f'{file_name}.json', 'w') as f:
            json.dump(res.json(), f, indent=4)

        print(f'[+] {file_name}')


if __name__=="__main__":
    file_extract()
    file_transfer()


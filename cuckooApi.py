import hashlib
import json
import os
import time

import py7zr
import requests


base_url = 'http://192.168.106.133:8090/'
create_url = f'{base_url}tasks/create/file'
download_url = f'{base_url}tasks/report'
delete_url = f'{base_url}tasks/delete'

directory_path = 'E:\\sample\\cfromAtoFAsterisk'
download_path = 'E:\\t'

header = {'Authorization': 'Bearer 3C-Y5VP4D-E-pGb1vM5BJw'}


def status_sleep(status_id):
    print(status_id, end=' ', flush=True)
    for t in range(1, 10 + 1):
        print("{}% ".format(t * 10), end='', flush=True)
        time.sleep(27)
    print()


def file_extract():
    password = 'infected'

    file_list = os.listdir(directory_path)

    for file in file_list:
        try:
            with py7zr.SevenZipFile(file, mode='r', password=password) as z:
                z.extractall(path=f'{directory_path}')
            os.remove(file)
        except Exception as e:
            print(e)


def report_create():
    file_list = os.listdir(directory_path)
    cnt = 0
    status_id = []
    for fi in file_list:
        if ('main.py' in fi) or ('.7z' in fi):
            continue

        if '.exe' in fi:
            with open(f'{directory_path}\\{fi}', 'rb') as f:
                data = f.read()

                res = requests.post(url=create_url, headers=header,
                                    files={'file': (str(hashlib.sha256(data).hexdigest()) + '.exe', data)})

                task_id = res.json()['task_id']
        else:
            with open(f'{directory_path}\\{fi}', 'rb') as f:
                data = f.read()

                res = requests.post(url=create_url, headers=header,
                                    files={'file': (str(hashlib.sha256(data).hexdigest()), data)})

                task_id = res.json()['task_id']
        cnt += 1
        status_id.append(task_id)

        if (cnt % 2) == 0:
            status_sleep(status_id)
            report_download(status_id)
            cnt = 0
            status_id = []


def report_download(status_id):

    for idx in status_id:
        send_url = f'{download_url}/{idx}'

        res = requests.get(url=send_url, headers=header)

        try:
            file_name = res.json()['target']['file']['sha256']
        except Exception as e:
            continue

        with open(f'{download_path}\\{file_name}.json', 'w') as f:
            json.dump(res.json(), f, indent=4)

        report_delete(idx)


def report_delete(task_id):

    send_url = f'{delete_url}/{task_id}'

    res = requests.get(url=send_url, headers=header)

    try:
        print(res.json()['status'])
    except Exception as e:
        pass


if __name__ == '__main__':
    file_extract()
    report_create()

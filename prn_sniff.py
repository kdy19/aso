from scapy.all import *

import collections
import threading
import logging
import time
import sys
import os
import re


IP_COLLECT = collections.defaultdict(int)
MANAGE_IP = list()
PORT_LIST = []


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    

def count_time():

    global IP_COLLECT
    global MANAGE_IP
    
    while True:
        try:
            for ip in IP_COLLECT.keys():
                if IP_COLLECT[ip] < 10:
                    MANAGE_IP.append(ip)
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)


def reset_time():

    global IP_COLLECT
    global MANAGE_IP
    
    while True:
        time.sleep(5)

        IP_COLLECT = collections.defaultdict(int)
        MANAGE_IP = list()
        

def print_pkt(pkt):

    global IP_COLLECT

    try:
        if pkt['TCP'].dport == 80:
            if pkt['Raw'].load:
                data = str(pkt['Raw'].load.decode('ascii'))
                data = data.split('\r\n')[0]
                
                if re.match('^GET', data):
                    IP_COLLECT[pkt['IP'].src] += 1
                    if pkt['IP'].src in MANAGE_IP:
                        log_fmt = f'{data.split(" ")[1]} '
                        log_fmt += f'{bcolors.FAIL}{pkt["IP"].src}:{pkt["TCP"].sport}{bcolors.ENDC}'
                        log_fmt += f' -> {pkt["TCP"].dport}'
                        logging.info(log_fmt)
                        
                    else:
                        log_fmt = f'{data.split(" ")[1]} '
                        log_fmt += f'{pkt["IP"].src}:{pkt["TCP"].sport}'
                        log_fmt += f' -> {pkt["TCP"].dport}'
                        logging.info(log_fmt)
                        
                elif re.match('^POST', data):
                    IP_COLLECT[pkt['IP'].src] += 1

                    data = str(pkt['Raw'].load.decode('ascii'))
                    data = data.split('\r\n')[-1]
                    
                    if pkt['IP'].src in MANAGE_IP:
                        log_fmt = f'{data} '
                        log_fmt += f'{bcolors.FAIL}{pkt["IP"].src}:{pkt["TCP"].sport}{bcolors.ENDC}'
                        log_fmt += f' -> {pkt["TCP"].dport}'
                        logging.info(log_fmt)

                    else:
                        log_fmt = f'{data} '
                        log_fmt += f'{pkt["IP"].src}:{pkt["TCP"].sport}'
                        log_fmt += f' -> {pkt["TCP"].dport}'
                        logging.info(log_fmt)

                else:
                    pass
                
    except Exception as e:
        pass
    

def main():
    sniff(prn=print_pkt, filter='tcp', store=0)
    

if __name__ == '__main__':

    fmt = '%(asctime)s: %(message)s'
    logging.basicConfig(format=fmt, level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    try:
        os.mkdir('./log/')
    except OSError as e:
        logging.info(e)
    
    t1 = threading.Thread(target=main, args=())
    t2 = threading.Thread(target=count_time, args=())
    t3 = threading.Thread(target=reset_time, args=())
    
    t1.start()
    t2.start()
    t3.start()
    
    t1.join()
    t2.join()
    t3.join()

from scapy.all import *
import collections
import argparse
import requests
import datetime
import folium
import json
import sys


def init(path) -> dict:

    ip_dict = collections.defaultdict(int)

    try:
        packets = rdpcap(path)
    except Exception as e:
        sys,exit(-1)        

    for packet in packets:
        try:
            ip_dict[packet['IP'].src] += 1
            ip_dict[packet['IP'].dst] += 1
        except Exception as e:
            pass

    return ip_dict


def create_json(time, ip_dict) -> None:

    dump_json = {}
    
    for ip in ip_dict.keys():
        url = f'https://ipinfo.io/{ip}?token='
        res = requests.get(url).json()

        dump_json[ip] = {}
        dump_json[ip] = res
        dump_json[ip]['count'] = ip_dict[ip]

    with open(str(time) + '.json', 'w') as f:
        json.dump(dump_json, f, indent=4)


def visualization_loc(time):

    with open(str(time) + '.json', 'r') as f:
        data = json.load(f)

    m = folium.Map(
        location = [36.5053542, 127.7043419],
        zoom_start = 8
    )

    for ip in data:
        try:
            folium.Marker(
                location = data[ip]['loc'].split(','),
                popup=str(ip) + ': ' + str(data[ip]['count']),
                icon=folium.Icon(color='red',icon='star')
            ).add_to(m)
        except Exception as e:
            pass

    m.save(str(time) + '.html')


if __name__ == '__main__':

    time = datetime.datetime.now().strftime('%Y-%m-%d')

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='[file path]', required=True)
    args = parser.parse_args()

    ip_dict = init(args.f)
    print(ip_dict)
    print(len(ip_dict))
    create_json(time, ip_dict)
    visualization_loc(time)

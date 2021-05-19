from scapy.all import *
import time
import sys
import os

def show_packet(packet) -> None:

    f = open('C:\\Users\\kdy\\Desktop\\8000.log', 'a')

    try:
        if packet[TCP].payload:
            if packet[IP].dport == 8000:
                string = "{} [HTTP] src={} {}\n".format(time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                    packet[IP].src,
                    "\n".join(packet.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n")))

                print("\n".join(packet.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n")))

                f.write(string)

    except Exception as e:
        print(sys.exc_info()[0], e)
        f.close()

    try:
        f.close()
    except Exception as e:
        print(sys.exc_info()[0], e)


if __name__ == "__main__":
    sniff(filter='tcp', prn=show_packet, store=0, count=0)

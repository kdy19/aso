from scapy.all import *
import time
import sys
import os

def show_packet(packet) -> None:
	
	try:
		if (packet[IP].dst == '192.168.0.5') and (packet[TCP].dport == 22):
			string = '{}  {}:{} -> {}:{}  [SSH]'.format(time.strftime(
				'%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
				packet[IP].src, packet[IP].sport,
				packet[IP].dst, packet[IP].dport)
			print(string)

		elif (packet[IP].dst == '192.168.0.5') and (packet[TCP].dport == 80):
			string = '{}  {}:{} -> {}:{}  [HTTP] flags: {}'.format(time.strftime(
				'%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
				packet[IP].src, packet[IP].sport,
				packet[IP].dst, packet[IP].dport,
				packet[TCP].flags)
			print(string)

		elif (packet[IP].dst == '192.168.0.5') and (packet[TCP].dport == 443):
			string = '{}  {}:{} -> {}:{}  [HTTPS] flags: {}'.format(time.strftime(
				'%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
				packet[IP].src, packet[IP].sport,
				packet[IP].dst, packet[IP].dport,
				packet[TCP].flags)
			print(string)

		else:
			pass

	except Exception as e:
		print(sys.exc_info()[0], e)


if __name__ == "__main__":
    sniff(filter='tcp', prn=show_packet, store=0, count=10)

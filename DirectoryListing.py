from bs4 import BeautifulSoup
import urllib.request
import argparse
import requests
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def dfs(url, depth):
	if depth > 15:
		return

	res = requests.get(url, verify=False)
	soup = BeautifulSoup(res.text, 'html.parser')

	file_list = soup.findAll('a')

	for fi in file_list:
		name = fi.get('href')
		text = fi.get_text().strip()

		if name[0] == '?' or text == 'Parent Directory':
			continue

		if name[-1] == '/':
			dfs(url + name, depth + 1)
		else:
			print(url + name)

parser = argparse.ArgumentParser()

parser.add_argument('-u', type=str, required=True)

args = parser.parse_args()

res = requests.get(args.u, verify=False)
soup = BeautifulSoup(res.text, 'html.parser')

file_list = soup.findAll('a')

for fi in file_list:
	name = fi.get('href')
	text = fi.get_text().strip()

	if name[0] == '?' or text == 'Parent Directory':
		continue

	if name[-1] == '/':
		dfs(args.u + name, 0)
	else:
		print(args.u + name)

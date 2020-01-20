#!/usr/bin/python
# encoding: utf-8

import sys
import getopt
import requests

class ZoomEye(object):
	def __init__(self, username=None, password=None):
		self.username = username
		self.password = password
		self.token = ""
		self.zoomeye_login_api = "https://api.zoomeye.org/user/login"
		self.zoomeye_search_api = "https://api.zoomeye.org/host/search"

	def login(self):
		login_data = '{{"username":"{0}", "password":"{1}"}}'.format(self.username, self.password)
		resp = requests.post(self.zoomeye_login_api, data=login_data)
		if resp and resp.status_code == 200 and 'access_token' in resp.json():
			self.token = resp.json().get('access_token')
			print("\033[0;32m[+] --------Login Success--------\033[0m")
		else:
			print("\033[0;31m[-] The Account's Password Maybe is Error!!!\033[0m")
			exit()
		return self.token;

	def search(self, keywords, notidc = False, filename = "hosts.txt"):
		self.keywords = keywords

		headers = {
			"Authorization": "JWT {}".format(self.token)
		}
		# query 20 pages
		for i in range(500):
			page = i
			print("\033[0;32m[+] Page={}\033[0m".format(page))
			result = []
			params = {
				"query": self.keywords,
				"page": page
			}
			resp = requests.get(self.zoomeye_search_api, params=params, headers=headers)
			if resp and resp.status_code == 200 and 'matches' in resp.json():
				matches = resp.json().get('matches')
				result = matches
				if notidc == False:
					ip_port(result, filename)
				else:
					ip_port_notidc(result, filename)
			else:
				print("\033[0;31m[-] The page maybe is not exist!!!\033[0m")
				print("\033[0;31m[-] status_code is {}\033[0m".format(resp.status_code))
				exit()

def ip_port(data, filename):
	global flag
	f = open(filename, "a")
	if data:
		for i in data:
			if "200 OK" not in str(i):
				continue
			else:
				url = str(i.get('ip'))+":"+str(i.get("portinfo").get("port"))
				print(url)
				f.write(url+"\n")
				flag += 1
		print("\033[0;32m[+] {} hosts saved in {}.\033[0m".format(flag, filename))
		f.close()
	else:
		print("\033[0;31m[-] Change Another Account!!!\033[0m")
		exit()

def ip_port_notidc(data, filename):
	global flag
	f = open(filename, "a")
	if data:
		for i in data:
			if "'idc': 'IDC'" in str(i):
				# print("this is idc")
				continue
			elif "200 OK" not in str(i):
				continue
			else:	
				url = str(i.get('ip'))+":"+str(i.get("portinfo").get("port"))
				print(url)
				f.write(url+"\n")
				flag += 1
		print("\033[0;32m[+] {} hosts saved in {}.\033[0m".format(flag, filename))
		f.close()
	else:
		print("\033[0;31m[-] Change Another Account!!!\033[0m")
		exit()

def main():
	opts, args = getopt.getopt(sys.argv[1:], "hnu:p:q:o:", ["help","notidc"])
	username = ""
	password = ""
	keywords = ""
	#resource = "host"
	notidc 	 = False
	for_help = """
  Options:
  -u			zoomeye's username
  -p			zoomeye's password
  -q			the keywords for query
  -o 			export to file, default hosts.txt
  -n, --notIDC		host not in IDC
  -h, --help		for help

  Some country code: KR,IN,CA,JP,RU,VN,PH,MY,ID,TH,MM,PK,KZ,IR,SA,BR,MX,DK,DE,FR,EXT.

  Usage: python3 ZoomeyeSearch.py -u foo@foo.com -p yourpassword -q "jboss country:KR -o xx_host.txt"        # all host
  Usage: python3 ZoomeyeSearch.py -u foo@foo.com -p yourpassword -n -q "jboss country:KR -o xx_host.txt"     # besides IDC
  Usage: python3 ZoomeyeSearch.py -u foo@foo.com -p yourpassword -n -q "port:3306 country:KR -o xx_host.txt"
  ext.
	"""
	if len(sys.argv) <= 4:
			print(for_help)
			exit()

	for opt,value in opts:
		if opt == '-u':
			username = value
		if opt == '-p':
			password = value
		if opt == '-q':
			keywords = value
		if opt == '-o':
			filename = value
		if opt == '-n' or opt == '--notidc':
			notidc = True
		if opt == '-h' or opt == '--help':
			print(for_help)

	print("Start Search......")
	zoomeye = ZoomEye()
	zoomeye.username = username
	zoomeye.password = password
	zoomeye.login()
	zoomeye.search(keywords, notidc, filename)

if __name__ == "__main__":
	global flag
	flag = 0
	main()
	#print(flag)
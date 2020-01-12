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
		return self.token;

	def search(self, keywords, notidc = False):
		self.keywords = keywords

		headers = {
			"Authorization": "JWT {}".format(self.token)
		}
		# query 20 pages
		for i in range(50):
			page = i
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
					ip_port(result)
				else:
					ip_port_notidc(result)

def ip_port(data):
	global flag
	if data:
		for i in data:
			if "200 OK" not in str(i):
				continue
			else:
				print(str(i.get('ip'))+":"+str(i.get("portinfo").get("port")), i.get('geoinfo').get('country').get('code'))
				#flag += 1

def ip_port_notidc(data):
	global flag
	if data:
		for i in data:
			if "'idc': 'IDC'" in str(i):
				# print("this is idc")
				continue
			elif "200 OK" not in str(i):
				continue
			else:	
				print(str(i.get('ip'))+":"+str(i.get("portinfo").get("port")), i.get('geoinfo').get('country').get('code'))
				#flag += 1

def zoomeye_search():
	opts, args = getopt.getopt(sys.argv[1:], "hnu:p:q:r:", ["help","notidc"])
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
  -c			country, the default is kr
  -r			host or web, the default is host
  -n, --notIDC		host not in IDC
  -h, --help		for help

  Some country code: KR,IN,CA,JP,RU,VN,PH,MY,ID,TH,MM,PK,KZ,IR,SA,BR,MX,DK,DE,FR,EXT.

  Usage: python3 ZoomeyeSearch.py -u foo@foo.com -p yourpassword -q "jboss country:KR"        # all host
  Usage: python3 ZoomeyeSearch.py -u foo@foo.com -p yourpassword -n -q "jboss country:KR"     # besides IDC
  Usage: python3 ZoomeyeSearch.py -u foo@foo.com -p yourpassword -n -q "port:3306 country:KR"
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
		#if opt == '-r':
		#	resource = value
		if opt == '-n' or opt == '--notidc':
			notidc = True
		if opt == '-h' or opt == '--help':
			print(for_help)

	zoomeye = ZoomEye()
	zoomeye.username = username
	zoomeye.password = password
	zoomeye.login()
	zoomeye.search(keywords, notidc)

if __name__ == "__main__":
	#global flag
	#flag = 0
	zoomeye_search()
	#print(flag)

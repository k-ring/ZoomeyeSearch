# ZoomeyeSearch.py

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

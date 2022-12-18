import requests
from bs4 import BeautifulSoup
d1=0
URL = 'https://www.hltv.org/matches'
URL1 = 'https://dota2.ru/esport/matches/'


reqs = requests.get(URL1)
soup = BeautifulSoup(reqs.text,'lxml')
d=[line.getText()for line in soup.find_all('div',class_='time')]
dt2=0
while dt2<(len(d)/2)-1:
	print(str(d[dt2].replace('Ч',' Ч')))
	dt2+=1


#res = requests.get(URL)
#soup = BeautifulSoup(res.text,'lxml')
##c = [soup.find_all('a',class_='mlink'.find_all('Матч'))]
#c = [line.getText()for line in soup.find_all('a',class_='mlink')]
#i=0
##while i<len(c):
##	if c[i]=='\n':
##			del c[i]
#while i<20:
#	print(c[i].replace('\n',' '))
#	i+=1
##c=[c for c in soup.find('a',class_='mlink').text]
##c=[line.rstrip() for line in c]class_='mlink'
##print(soup.prettify())
##res.raise_for_status()
##print(res)
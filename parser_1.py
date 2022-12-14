import requests
from bs4 import BeautifulSoup
i=0
URL = 'https://www.hltv.org/matches'
reqs = requests.get(URL)
soup = BeautifulSoup(reqs.text,'lxml')
c=[line.getText()for line in soup.find_all('div',class_='matchTeams text-ellipsis')]
while i<len(c):
	print(c[i].replace('\n','-'))
	i+=1






#URL = 'https://game-tournaments.com/csgo/matches'
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
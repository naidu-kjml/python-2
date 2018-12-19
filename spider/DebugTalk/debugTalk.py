#__author__:xjming
import requests,csv
from bs4 import BeautifulSoup

base_url = 'https://debugtalk.com/'
def request(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text,'lxml')
	sections = soup.find_all('section',class_='post')
	for sec in sections:
		title = sec.find('a')['title'].replace(u'\u23a1', u' ')
		link = 'https://debugtalk.com'+sec.find('a')['href'].replace(u'\xa0', u' ')
		time = sec.find('time').get_text().replace(u'\xa0', u' ')
		l = [title,link,time]
		print(title)
		with open('debugtalk.csv','a',newline='')as f:
			writer = csv.writer(f)
			try:
				writer.writerow(l)
			except:
				print('error!!!')

if __name__=='__main__':
	for i in range(1,11):
		if i == 1:
			request(base_url)
		else:
			request(base_url+'page/'+str(i))
import requests,csv
from bs4 import BeautifulSoup

bash_url = 'http://www.testclass.net/page/'
headers = {
	"User_Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
	"Referer" : "http://www.baidu.com"
}

def request(url):
	response = requests.get(url,headers=headers)
	response.encoding = 'utf-8'
	soup = BeautifulSoup(response.text,'lxml')
	titles = soup.find('ol',class_='post-list').find_all('li',class_='post-stub')
	for t in titles:
		title = t.find('h4').text
		link = t.find('a')['href']
		time = t.find('time').text
		l = [title,link,time]
		with open('chonshi.csv','a',newline='')as f:
			writer = csv.writer(f)
			writer.writerow(l)
	
if __name__=='__main__':
	print('catch first page')
	url = 'http://www.testclass.net'
	request(url)
	for i in range(2,9):
		url = bash_url+str(i)
		print('catch %dth page'%i)
		request(url)
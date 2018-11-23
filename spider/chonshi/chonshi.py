import requests,time,random,os,csv
from bs4 import BeautifulSoup

bash_url = 'http://www.cnblogs.com/fnng/default.aspx?page='
headers = {
	"User_Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
	"Referer" : "http://www.baidu.com"
}

def request(url):
	respon = requests.get(url,headers=headers)
#print(respon.text)
	respon.encoding = 'utf-8'
	soup = BeautifulSoup(respon.text,'lxml')
	titles = soup.find_all('div',class_='post post-list-item')

	for title in titles:
		caption = title.find('h2').text.replace(u'\xa0', u'')
		caption = caption.replace('\n','')
		link = title.find('h2').find('a')['href']
		time = title.find('small').text
		l = [caption,link,time]
		with open('chonshi.csv','a',newline='')as f:
			writer = csv.writer(f)
			writer.writerow(l)
		
if __name__=='__main__':
	for i in range(1,22):
		print('catching %dth page'%i)
		url = bash_url+str(i)
		request(url)

	
	

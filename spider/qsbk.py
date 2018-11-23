from bs4 import BeautifulSoup
import requests,os

url = "https://cuiqingcai.com/"

start_html = requests.get(url)

soup = BeautifulSoup(start_html.text,'lxml')

article_list = soup.find_all('article',class_='excerpt')

for article in article_list:
	link = article.find('h2').find('a')['href']
	title = article.find('h2').find('a')['title']
	print(link,title)
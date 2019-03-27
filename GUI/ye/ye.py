#!//usr/bin/env python
#-*-coding:utf-8 -*-
import os,requests,json,socket,shutil
from bs4 import BeautifulSoup
from urllib.request import urlretrieve


class Ye(object):
	def __init__(self, page, url, leibie):
		self.pageIndex = page
		self.url = url
		self.leibie = leibie

	def get_link(self, url, picname):
		socket.setdefaulttimeout(5.0)
		header= {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
		proxies={"http":"http//61.135.217.7", "https":"182.47.67.102"}
		r=requests.get(url)
		content=r.text
		soup=BeautifulSoup(content,'lxml')
		divs=soup.find('input',{'name':'copy_sel'})
		link=divs.get('value')
		#d={picname:link}
	#	f=open(r'%s\link.json'%self.path,'a')
	#	json.dump(d,f)
		#f.close()
		image=soup.find("img", {"class": "img"}).get("src")
		try:
			urlretrieve(image,r'%s\%s.jpg'%(self.path,picname))
		except HttpError as e:
			print(e.code)
		except socket.timeout:
			print('保存第%s页图片$s失败'%(self.pageIndex,picname))
		with open(r'%s\link.txt'%self.path,'a') as f:
			f.write(link+'\n')
		print('保存第%s页图片%s成功'%(self.pageIndex, picname))
			
			
	
	def get_urllist(self):
		url_init = self.url
		url_list = []
		url = r'%s/%s/index-%s.html' % (url_init, self.leibie, self.pageIndex)
		#url = url_init
		header= {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
		proxies={"http":"http//61.135.217.7", "https":"182.47.67.102"}
		r=requests.get(url)
		r.encoding = 'utf-8'
		content=r.text
		soup=BeautifulSoup(content,'lxml')
		tbody=soup.find_all('tbody')
		trs=tbody[1].find_all('tr',{'bgcolor':'#f5fef7'})
		for t in trs:
			url={}
			td=t.find('td')
			i=td.find('a')
			url['theme']=i.text
			url['url']=url_init+i.get('href')
			url_list.append(url)
		return url_list
	
	def start(self,progressBar):
		urllist=self.get_urllist()
		self.path=str(self.pageIndex)
		if os.path.exists(self.path):
			shutil.rmtree(self.path)
		os.mkdir(self.path)
		picname=1
		sum = len(urllist)
		for l in urllist:
			url=l['url']
			try:
				progressBar.setProperty("value", (100/sum)*picname)
				if (100/sum)*picname>98:
					progressBar.setProperty("value", 100)
				self.get_link(url,picname)
			except:
				print('第%d页面不存在'%picname)
				sum = sum+1
				continue
			picname=picname+1
				
				
		#print('第%s加载完成'%self.pageIndex)

if __name__=='__main__':
	y = Ye(str(1))
	y.start()
from qsbk.items import QsbkItem
from .sql import Sql
import requests,re,os

class QsbkPipeline(object):
    def process_item(self,item,spider):
        author=item['author']
        qs_type=item['qs_type']
        content=item['content']
        l=item['l']
        Sql.insert_qs(author,qs_type,content,l)
        print('开始保持糗事')
        print(item['thumb'])
        if re.match(r'https://pic.*?',item['thumb']):
            url=str(item['thumb'])
            picname=re.split('/',url)[-1]
            r=requests.get(url)
            if not os.path.exists('img'):
                os.makedirs('img')
            with open('img/'+picname, 'wb') as file:
                file.write(r.content)

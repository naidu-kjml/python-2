import requests

#api链接
api_url = "http://dev.kdlapi.com/api/getproxy/?orderid=965102959536478&num=100&protocol=1&method=2&an_ha=1&sep=1"

r = requests.get(api_url)

print(r.status_code) #获取Reponse的返回码

if r.status_code == 200:
    print(r.content.decode('utf-8')) #获取API返回内容
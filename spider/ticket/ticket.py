import requests

url = 'http://www.tianhebus.com/cn/BusSchedule.aspx?&terminal=%u8549%u5CAD&date=2019-04-04'

respons = requests.get(url)
print(respons.text)
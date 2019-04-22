from requests_html import HTMLSession

session = HTMLSession()
r = session.get('https://www.baidu.com')
r.html.render()
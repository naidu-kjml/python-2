import re

s = r'<a href='' onclick=flow_view(1636338,2224)>第7步：绩效反馈<'
res = re.match('.*?第(\d)步',s)
print(res.group(1))
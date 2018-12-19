#coding:utf-8 
import time,locale
from datetime import timedelta,date

locale.setlocale(locale.LC_CTYPE,'chinese')
def date_time_chinese():
    return time.strftime("%Y年%m月%d日 %H时%M分%S秒",time.localtime())

#coding=utf-8
from Util.excel import *
from ProjectVar.var import *
import requests
from Action.search_keyword import *
from Util.excel import *
from Util.write_excel import *
from Action.optimiza_result import *

eins = Excel_r_w(excel_path,"Sheet1")
max_col = eins.get_max_row()
driver = webdriver.Chrome()

for ir in range(2,eins.get_max_row()+1):
    keyword = CrawlKW(driver,eins.get_value("B"+str(ir)),eins.get_value("C"+str(ir)))
    write_result(eins,"E"+str(ir),str(keyword))
driver.quit()
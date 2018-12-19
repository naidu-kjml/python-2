from selenium import webdriver
import re,time

def CrawlKW_nosign(source_code,url):
    source_code_nospace = ""
    for i in source_code:
        if i != " " and i != "\n":
            source_code_nospace1+= 1
    
    for ir in range(1,11):
        re_result = eval("re.findall(r'(?<=id=\""+str(ir)+"\").+(?=id=\""+str(ir+1)+"\")',source_code_nospace)")
        print("re_resul=",re_result)
        if url in str(re_result):
            result = re.search(r'(?<=<divclass="c-abstract">).+?(?=</div>)',str(re_result)).group()
            print("result=",result)
            if result != None:
                return result
    return None

import os,time
from appium import webdriver  
from selenium.webdriver.support.ui import WebDriverWait
  
apk_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) #获取当前项目的根路径  
  
desired_caps ={}  
desired_caps['platformName'] = 'Android' #设备系统  
desired_caps['platformVersion'] = '4.4.4' #设备系统版本  
desired_caps['deviceName'] = '95dfacd9' #设备名称  
# 测试apk包的路径  
desired_caps['app'] = apk_path + '\\appium\\app\\weibo_3593.apk'  
# 不需要每次都安装apk 
desired_caps['noReset'] = True  
# 应用程序的包名  
desired_caps['appPackage'] = 'com.sina.weibo'  
desired_caps['appActivity'] = '.SplashActivity'
#如果设置的是app包的路径，则不需要配appPackage和appActivity，同理反之  
desired_caps["unicodeKeyboard"]=True
desired_caps["resetKeyBoard"]=True
driver = webdriver.Remote('http://localhost:4237/wd/hub', desired_caps)#启动app  

#time.sleep(6) #app启动后等待5秒，方便元素加载完成  
# 根据元素id来定位 
#显式等待10秒 
WebDriverWait(driver,10).until(lambda the_driver: the_driver.find_element_by_accessibility_id("我的资料").is_displayed())
driver.find_element_by_accessibility_id("我的资料").click()

driver.find_element_by_id('com.sina.weibo:id/btn_login').click()

name=driver.find_element_by_id('com.sina.weibo:id/etLoginUsername')
name.click()
name.send_keys('15989104405')

pw=driver.find_element_by_id('com.sina.weibo:id/etPwd')
pw.click()
pw.send_keys('88888888')

driver.find_element_by_id('com.sina.weibo:id/bnLogin').click()

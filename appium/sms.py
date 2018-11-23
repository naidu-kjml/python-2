import os,time
from appium import webdriver  
from selenium.webdriver.support.ui import WebDriverWait
  
apk_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) #获取当前项目的根路径  
  
desired_caps ={}  
desired_caps['platformName'] = 'Android' #设备系统  
desired_caps['platformVersion'] = '4.4.4' #设备系统版本  
desired_caps['deviceName'] = '95dfacd9' #设备名称  
# 测试apk包的路径  
#desired_caps['app'] = apk_path + '\\appium\\app\\weibo_3593.apk'  
# 不需要每次都安装apk 
desired_caps['noReset'] = True  
# 应用程序的包名  
desired_caps['appPackage'] = 'com.android.mms'  
desired_caps['appActivity'] = '.ui.MmsTabActivity'
#如果设置的是app包的路径，则不需要配appPackage和appActivity，同理反之  
desired_caps["unicodeKeyboard"]=True
desired_caps["resetKeyBoard"]=True
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)#启动app  

WebDriverWait(driver,10).until(lambda the_driver: the_driver.find_element_by_accessibility_id("写短信").is_displayed())
driver.find_element_by_accessibility_id("写短信").click()

rec = driver.find_element_by_id('com.android.mms:id/recipients_editor')
rec.click()
rec.send_keys('13610177835')
try:
	WebDriverWait(driver,1).until(lambda the_driver: the_driver.find_element_by_accessibility_id("确认").is_displayed())
	driver.find_element_by_accessibility_id("确认").click()
except TimeoutException:
	pass
finally:
	con = driver.find_element_by_id('com.android.mms:id/embedded_text_editor')
	con.click()
	con.send_keys('捏爆炸')
	driver.find_element_by_accessibility_id('发送短信').click()
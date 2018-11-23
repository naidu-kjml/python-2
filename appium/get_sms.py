import subprocess
import os

print("开始程序")
fhandle = open(r"D:\aa.txt", "a")  
p = subprocess.Popen("adb shell su -c'cp data/data/com.android.providers.telephony/databases/mmssms.db /sdcard&&exit&&exit'",stdout=fhandle).stdout


print("取出数据库")
os.system("adb pull /sdcard/mmssms.db")
print("结束")
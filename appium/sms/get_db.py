import subprocess
import os

fhandle = open(r"D:\aa.txt", "a")  
p = subprocess.Popen("adb shell su -c'cp data/data/com.android.providers.telephony/databases/mmssms.db /sdcard&&exit&&exit'",stdout=fhandle).stdout
os.system("adb pull /sdcard/mmssms.db")

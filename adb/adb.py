#-*-coding:utf-8 -*-
import subprocess
def getDevicesInfo():
    out = subprocess.Popen('adb devices',shell=True,stdout=subprocess.PIPE)
    deviceslist = out.stdout.read().splitlines()
    serial_nos = []
    if len(deviceslist) > 2:
        for item in deviceslist:
            print(item)
            if 'List' in item:
                continue
            elif 'no permissions' in item:
                continue
            elif item.strip() == '':
                continue
            else:
                serial_nos.append(item.split()[0])
                pass
            pass
        return serial_nos
    else:
        return -1

def getPid(device,process):
    cmd = "adb -s %s shell ps | grep %s"%(device,process)
    out = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    infos = out.stdout.read().splitlines()
    print(infos)
    pidlist = []
    if len(infos) >= 1:
        for i in infos:
            pid = i.split()[1]
            if pid not in pidlist:
                pidlist.append(pid)
        return pidlist
    else:
        return -1

def stopMonkey(devices):
    if (devices):
        pidList = getPid(devices,'monkey')
        if (pidList == -1):
            pass
        else:
            for index in range(len(pidList)):
                try:
                    cmd = 'adb -s %s shell kill %s'%(devices,pidList[index])
                    subprocess.Popen(cmd,shell=True)
                    pass
                except:
                    pass
            pass
        pass
    pass



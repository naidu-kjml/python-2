#!/usr/bin/env python3

import itchat

#产生二维码
itchat.auto_login()
#定义用户的昵称
send_userid='CI'
#查找用户的userid
itcaht_user_name = itchat.search_friends(name=send_userid)[0]['UserName']
#利用send_msg发送消息
itchat.send_msg('这是一个测试',toUserName=itcaht_user_name)
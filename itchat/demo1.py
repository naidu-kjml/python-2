import itchat,time


@itchat.msg_register(itchat.content.TEXT)
def reply_msg(msg):
	id = ['@1eaa07b4363da13f703feefdb47a45517086b1c3279d9775833d11affb6ee3cc', '@4482ad5122ff6a679f32658a6e08f4e66973d28208188b78aeea99787adb29cd']
	if msg['FromUserName'] not in id:
		itchat.send_msg('%s\n正在忙，稍后回复。。。'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg['FromUserName'])

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()

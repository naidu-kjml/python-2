#coding=utf8
import requests,random,time
import itchat

apikeys = ['4d11f722608446ff872a101ea93aac45','1945773322d04b509d12a8d2602768e6','6c072fc78f664a7fb61a546f8d82bfb9','32bd33f3941c4d448f9f5b6c84bb6f24','c6d596340ef24093811b7b75350b2603']

def get_response(msg):
	# 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
	# 构造了要发送给服务器的数据
	apiUrl = 'http://www.tuling123.com/openapi/api'
	data = {
		'key'	 : apikeys[random.randint(1,3)],
		'info'	 : msg,
		'userid' : 'wechat-robot',
	}
	try:
		r = requests.post(apiUrl, data=data).json()
		# 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
		return r.get('text')
	# 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
	# 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
	except:
		# 将会返回一个None
		return

# 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
	# 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
	defaultReply = 'I received: ' + msg['Text']
	# 如果图灵Key出现问题，那么reply将会是None
	reply = get_response(msg['Text'])+'（小助手）'
	# a or b的意思是，如果a有内容，那么返回a，否则返回b
	# 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
	time.sleep(random.randint(1,3))
	return reply or defaultReply

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload=True)
itchat.run()

from locust import HttpLocust,TaskSet,task

class UserBehavior(TaskSet):
	def on_start(self):
		self.index = 0
	@task
	def baidu_index(self):
	#	url = self.locust.data[self.index]
	#	print('vist url:%s'%url)
	#	self.index = (self.index + 1) % len(self.locust.data)
		con=self.client.get("/")
		#print(con.text)

class WebSiteUser(HttpLocust):
	task_set=UserBehavior
	#data = ['14410','14411','14412']
from locust import task,HttpLocust,TaskSet

class UserBehavior(TaskSet):
	@task
	def errcode(self):
		url = '/errcode.php?ErrCode=14410'
		self.client.get(url)

class websiteUser(HttpLocust):
	task_set = UserBehavior
	host='http://errcode.cf'

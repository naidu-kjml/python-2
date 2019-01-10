from locust import task, HttpLocust, TaskSet
import queue
import random


class UserBehavior(TaskSet):
	@task
	def face_regist(self):
		data = self.locust.user_data_queue.get()
		url = '/guns-admin/face/registPicture'
		files = dict(picture=('face1.jpg', open(r'C:\Users\xjming9\Desktop\face1.JPG', 'rb'), 'image/jpeg', {}),
					 idcardFront=('face1.jpg', open(r'C:\Users\xjming9\Desktop\face1.JPG', 'rb'), 'image/jpeg', {}),
					 idcardBack=('face2.jpg', open(r'C:\Users\xjming9\Desktop\face1.JPG', 'rb'), 'image/jpeg', {}))
		payload = {
			'userId': data['userId'],
			'userName': '林七',
			'ver': '01',
			'sign': '4C3CA90C359389F9FA34E822994A6016',
			'sex': '2',
			'requestDate': '20180920022108',
			'registerType': '1',
			'idcardType': '2',
			'idcardEndtime': '20180920',
			'idcardBegintime': '20180720'
		}
		self.client.post(url, data=payload, files=files)


class WebsiteUser(HttpLocust):
	task_set = UserBehavior
	host = 'http://10.252.176.5:8080'
	user_data_queue = queue.Queue()
	for index in range(10000):
		data = {
			"userId": str(random.randint(123456789123456789, 999999999999999999))
		}
		user_data_queue.put_nowait(data)

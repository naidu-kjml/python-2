from datetime import datetime
import functools

def metric(fun):
	@functools.wraps(fun)
	def wrapper(*args,**kw):
		print(datetime.now())
		return fun(*args,**kw)
	return wrapper
	
@metric
def now():
	print('sssssssss')
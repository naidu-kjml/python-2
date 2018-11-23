import flask
import time

app = flask.Flask(__name__)

@app.route('/')
def index():
	time.sleep(3)
	return 'Hello!'

if __name__ == '__main__':
	app.run(threaded=True)
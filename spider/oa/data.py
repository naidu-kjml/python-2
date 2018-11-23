import mysql.connector

MYSQL_HOSTS = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_PORT = '3306'
MYSQL_DB = 'oa'
def select_bbs():
	cnx = mysql.connector.connect(user=MYSQL_USER,password=MYSQL_PASSWORD,host=MYSQL_HOSTS,database=MYSQL_DB)
	cur = cnx.cursor(buffered=True)
	sql = 'SELECT comment from comment'
	cur.execute(sql)
	values = cur.fetchall()
	with open('data.txt','a') as f:
		for i in values:
			try:
				f.write('%s\n'%i[0])
				print(i[0])
			except:
				continue
	cur.close()
	cnx.close()
	
if __name__=='__main__':
	select_bbs()
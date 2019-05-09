import mysql.connector


MYSQL_HOSTS = '10.252.176.3'
MYSQL_USER = 'testuser'
MYSQL_PASSWORD = 'testuser@1763'
MYSQL_PORT = '3306'
MYSQL_DB = 'inv-app'

cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
cur = cnx.cursor(buffered=True)

def insert(usr_id,title,regis_no,receiver_mail,common,set_default,phone_no):
	sql = 'INSERT INTO title_manage(usr_id,title,regis_no,receiver_mail,common,set_default,phone_no) VALUES (%(usr_id)s,%(title)s,%(regis_no)s,%(receiver_mail)s,%(common)s,%(set_default)s,%(phone_no)s)'
	value = {
		'usr_id':usr_id,
		'title':title,
		'regis_no':regis_no,
		'receiver_mail':receiver_mail,
		'common':common,
		'set_default':set_default,
		'phone_no':phone_no
	}
	cur.execute(sql, value)
	cnx.commit()

if __name__=='__main__':
	for i in range(10):
		insert(i, 'python添加111', '1', '9891@qq.com', 'sqsqsqq', 'e', '2133234234')
import mysql.connector
MYSQL_HOSTS = '10.10.28.121'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'ruqi123456'
MYSQL_PORT = '3306'
MYSQL_DB = 'xjming'

try:
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
    cur = cnx.cursor(buffered=True)
except:
    print("数据库异常")


class Sql:
    @classmethod
    def insert_dr(cls, host, name, phone, city, env, result, time):
        sql = 'INSERT INTO driver_upload(host,name,phone,city,env,result,time) VALUES (%(host)s,%(name)s,%(phone)s,%(city)s,%(env)s,%(result)s,%(time)s)'
        value = {
            'host': host,
            'name': name,
            'phone': phone,
            'city': city,
            'env': env,
            'result': result,
            'time': time
        }
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def select_user(cls, host):
        cur.execute('select * from user where host = %s', (host,))
        values = cur.fetchall()
        return values

    @classmethod
    def update_user(cls, host, phone, time):
        cur.execute('UPDATE user SET phone = %s,time = %s WHERE host=%s', (phone, time, host))
        cnx.commit()

    @classmethod
    def insert_user(cls, host, phone, time):
        sql = 'INSERT INTO user(host,phone,time) VALUES (%(host)s,%(phone)s,%(time)s)'
        value = {
            'host': host,
            'phone': phone,
            'time': time
        }
        cur.execute(sql, value)
        cnx.commit()


if __name__ == "__main__":
    v = Sql.select_user('10.10.31.92')
    print(v)

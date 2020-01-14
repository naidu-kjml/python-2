import pymysql

MYSQL_HOSTS = '10.10.28.121'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'ruqi123456'
MYSQL_PORT = '3306'
MYSQL_DB = 'xjming'


class Sql:
    @classmethod
    def insert_dr(cls, host, name, phone, city, env, result, time):
        cnx = pymysql.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
        cnr = cnx.cursor()
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
        cnr.execute(sql, value)
        cnx.commit()
        cnr.close()
        cnx.close()

    @classmethod
    def select_user(cls, host):
        cnx = pymysql.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
        cnr = cnx.cursor()
        cnr.execute('select * from user where host = %s', (host,))
        values = cnr.fetchall()
        cnr.close()
        cnx.close()
        return values

    @classmethod
    def update_user(cls, host, phone, time):
        cnx = pymysql.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
        cnr = cnx.cursor()
        cnr.execute('UPDATE user SET phone = %s,time = %s WHERE host=%s', (phone, time, host))
        cnx.commit()
        cnr.close()
        cnx.close()

    @classmethod
    def insert_user(cls, host, phone, time):
        cnx = pymysql.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
        cnr = cnx.cursor()
        sql = 'INSERT INTO user(host,phone,time,driver_phone) VALUES (%(host)s,%(phone)s,%(time)s)'
        value = {
            'host': host,
            'phone': phone,
            'time': time
        }
        cnr.execute(sql, value)
        cnx.commit()
        cnr.close()
        cnx.close()

    @classmethod
    def select_assign(cls, client_phone):
        cnx = pymysql.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
        cnr = cnx.cursor()
        cnr.execute('select * from assign where client_phone = %s', (client_phone,))
        values = cnr.fetchall()
        cnr.close()
        cnx.close()
        return values

    @classmethod
    def select_assign1(cls, host):
        cnx = pymysql.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
        cnr = cnx.cursor()
        cnr.execute('select * from assign where host = %s order by time asc', (host,))
        values = cnr.fetchall()
        cnr.close()
        cnx.close()
        return values

    @classmethod
    def insert_assign(cls, host, client_phone, driver_phone, status, time):
        cnx = pymysql.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
        cnr = cnx.cursor()
        sql = 'INSERT INTO assign(host,client_phone,driver_phone,status,time) VALUES (%(host)s,%(client_phone)s,%(driver_phone)s,%(status)s,%(time)s)'
        value = {
            'host': host,
            'client_phone': client_phone,
            'driver_phone': driver_phone,
            'status': status,
            'time': time
        }
        cnr.execute(sql, value)
        cnx.commit()
        cnr.close()
        cnx.close()

    @classmethod
    def update_assign(cls, host, client_phone, driver_phone, status, time):
        cnx = pymysql.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
        cnr = cnx.cursor()
        cnr.execute('UPDATE assign SET host = %s,status = %s,time = %s WHERE client_phone = %s AND driver_phone = %s',
                    (host, status, time, client_phone, driver_phone))
        cnx.commit()
        cnr.close()
        cnx.close()


if __name__ == "__main__":
    values = Sql.select_assign('15989104405')
    for v in values:
        print(v[4])

import mysql.connector
from qsbk import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
cur = cnx.cursor(buffered=True)

class Sql:
    @classmethod
    def insert_qs(cls, author, qs_type, content, l):
        sql = 'INSERT INTO qsbk(author,qs_type,content,l) VALUES (%(author)s,%(qs_type)s,%(content)s,%(l)s)'
        value = {
            'author': author,
            'qs_type': qs_type,
            'content': content,
            'l': l
        }
        cur.execute(sql, value)
        cnx.commit()

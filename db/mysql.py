from sshtunnel import SSHTunnelForwarder
import pymysql
import pandas as pd


# tunnel = SSHTunnelForwarder(('139.59.112.128', 22), ssh_password='7A19f067z'
#                             , ssh_username='root', remote_bind_address=('139.59.112.128', 3306))
# tunnel.start()

class DBHelper:

    def __init__(self):
        self.host = '139.59.112.128'
        self.user = "root"
        self.password = '7A19f067z'
        self.db = "pplotto"

    def __connect__(self):
        self.con = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                   db=self.db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()

    def fetch(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def execute(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        self.__disconnect__()


conn = pymysql.connect(host='139.59.112.128', user='root', passwd='7A19f067z')
data = pd.read_sql_query("SHOW DATABASES;", conn)
info = pd.read_sql_query("SELECT * FROM pplotto.user;", conn)
print(data)
print(info)

conn.close()
# tunnel.close()

# if __name__ == '__main__':

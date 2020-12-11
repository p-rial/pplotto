import pymysql


# tunnel = SSHTunnelForwarder(('139.59.112.128', 22), ssh_password='7A19f067z'
#                             , ssh_username='root', remote_bind_address=('139.59.112.128', 3306))
# tunnel.start()

class DBHelper:

    __instance__ = None

    def __init__(self):
        """ Constructor.
        """
        if DBHelper.__instance__ is None:
            DBHelper.__instance__ = self
            self.host = '139.59.112.128'
            self.user = "root"
            self.password = '7A19f067z'
            self.db = "pplotto"
        else:
            raise Exception("You cannot create another SingletonGovt class")

    @staticmethod
    def get_instance():
        if not DBHelper.__instance__:
            DBHelper()
        return DBHelper.__instance__

    def __connect__(self):
        self.con = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                   db=self.db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()

    # data = pd.read_sql_query("SHOW DATABASES;", self.con)
    def fetch(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

    def execute(self, sql):
        self.cur.execute(sql)


db = DBHelper.get_instance()
db.__connect__()
data = db.fetch("SELECT * FROM pplotto.user;")
db.__disconnect__()
# conn = pymysql.connect(host='139.59.112.128', user='root', passwd='7A19f067z')

print(data, type(data[0]))
# print(info)

# conn.close()
# tunnel.close()

# if __name__ == '__main__':

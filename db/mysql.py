import pymysql
import sys

# tunnel = SSHTunnelForwarder(('139.59.112.128', 22), ssh_password='7A19f067z'
#                             , ssh_username='root', remote_bind_address=('139.59.112.128', 3306))
# tunnel.start()
from pymysql import Error

from models import User


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
            self.__connect__()
        else:
            raise Exception("You cannot create another DBHelper class")

    @staticmethod
    def get_instance():
        if not DBHelper.__instance__:
            DBHelper()
        return DBHelper.__instance__

    def __connect__(self):
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                    db=self.db, cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def __disconnect__(self):
        self.conn.close()

    # data = pd.read_sql_query("SHOW DATABASES;", self.con)
    # def fetch(self, sql):
    #     self.cur.execute(sql)
    #     result = self.cur.fetchall()
    #     return result
    #
    # def execute(self, sql):
    #     self.cur.execute(sql)


# db = DBHelper.get_instance()
# db.__connect__()
# data = db.fetch("SELECT * FROM pplotto.user;")
# db.__disconnect__()


# conn = pymysql.connect(host='139.59.112.128', user='root', passwd='7A19f067z')

def add_user(user: User):
    db = DBHelper.get_instance()

    sql = "INSERT INTO `user` (`username`, `password`, `name`, `surname`, `phone`) " \
          "VALUES(%s, %s, %s, %s, %s);"
    try:
        db.cursor.execute(sql, ({user.username}, {user.password}, {user.name}, {user.surname}, {user.phone}))
        db.conn.commit()
    except Error as e:
        # TODO: Find way to extract error message out
        return f"Error: {sys.exc_info()[1]}"


def submit_nums():
    pass
from typing import List

import pymysql
import sys
from pprint import pprint

# tunnel = SSHTunnelForwarder(('139.59.112.128', 22), ssh_password='7A19f067z'
#                             , ssh_username='root', remote_bind_address=('139.59.112.128', 3306))
# tunnel.start()
from pymysql import Error

from match_num import NumPool
from models import User, LottoNum


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

    # cursorclass = pymysql.cursors.DictCursor
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

    sql = """
          INSERT INTO `user` 
          (`username`, `password`, `name`, `surname`, `phone`)
          VALUES(%s, %s, %s, %s, %s);
    """
    try:
        db.cursor.execute(sql, ({user.username}, {user.password}, {user.name}, {user.surname}, {user.phone}))
        db.conn.commit()
    except Error as e:
        # TODO: Find way to extract error message out
        return f"Error: {sys.exc_info()[1]}"


def is_user_existed(username, password):
    db = DBHelper.get_instance()

    sql = """
          SELECT EXISTS(SELECT username, password from user 
          WHERE username= %s and password= %s) as `is_existed`;  
    """

    try:
        db.cursor.execute(sql, (username, password))
        results = db.cursor.fetchall()
        db.conn.commit()
        return results[0]["is_existed"], None
    except Error as e:
        # TODO: Find way to extract error message out
        return None, f"Error: {sys.exc_info()[1]}"


def submit_nums(username, json_obj):
    db = DBHelper.get_instance()
    # TODO: Execute commit only once ?
    sql_user = """
          SELECT user_id from user 
          where username= %s;  
    """
    db.cursor.execute(sql_user, username)
    user_result = db.cursor.fetchall()
    db.conn.commit()

    if user_result == ():
        return False
    else:
        user_id = user_result[0]["user_id"]

        num_ls = []
        for item in json_obj["numbers"]:
            small_ls = item.split("-") + [user_id]

            num_ls.append(small_ls)

        sql_nums = """
          INSERT INTO `total_num` 
          (`num`, `per_no`, `set_no`, `user_id`)
          VALUES(%s, %s, %s, %s) ON duplicate key update count=count+1; 
        """
        db.cursor.executemany(sql_nums, num_ls)
        db.conn.commit()

    return True


def pool_matching():
    db = DBHelper.get_instance()

    # TODO: Handle case 'total_num' table is empty

    # TODO: Query two times for different per_no for two pools
    """
        Query all number out
    """
    sql_get_all = """
              SELECT num, per_no, set_no, username 
              from total_num inner join user 
              on total_num.user_id = user.user_id;  
        """
    db.cursor.execute(sql_get_all)
    results = db.cursor.fetchall()

    """
        Matching logic perform here
    """
    to_lottoNum: List[LottoNum] = [LottoNum(**item) for item in results]

    total_pool = NumPool(to_lottoNum)

    matched_ls = total_pool.self_match()

    """
        Truncate matched table
    """

    sql_truncate = """
        truncate table matched;
    """
    db.cursor.execute(sql_truncate)

    """
    Save matched result in matched table
    """
    sql_save_matched = """
              INSERT INTO `matched` 
              (`num`, `per_no`, `set_no`, `username`)
              VALUES(%s, %s, %s, %s) ON duplicate key update count=count+1; 
            """

    ls_of_tuple = [obj.to_tuple() for obj in matched_ls]
    db.cursor.executemany(sql_save_matched, ls_of_tuple)

    db.conn.commit()

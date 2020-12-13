import traceback
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
            self.conn = self.to_connect()
        else:
            raise Exception("You cannot create another DBHelper class")

    @staticmethod
    def get_instance():
        if not DBHelper.__instance__:
            DBHelper()
        return DBHelper.__instance__

    # cursorclass = pymysql.cursors.DictCursor
    @staticmethod
    def to_connect():
        return pymysql.connections.Connection(
            host='139.59.112.128', user="root", password='7A19f067z',
            db="pplotto", cursorclass=pymysql.cursors.DictCursor
        )

    def is_connected(self):
        """Check if the server is alive"""
        try:
            self.conn.ping(reconnect=True)
            print("db is connecting")
        except:
            traceback.print_exc()
            self.conn = self.to_connect()
            print("db reconnect")

    def save_changes(self):
        self.conn.commit()

    def query(self, sql, args=None):
        cursor = self.conn.cursor()

        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()
        return results

    def query_many(self, sql, items):
        cursor = self.conn.cursor()

        cursor.executemany(sql, items)
        results = cursor.fetchall()

        cursor.close()
        return results

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
    db.is_connected()
    # cursor = db.conn.cursor()
    sql = """
          INSERT INTO `user` 
          (`username`, `password`, `name`, `surname`, `phone`)
          VALUES(%s, %s, %s, %s, %s);
    """
    try:
        _ = db.query(sql, ({user.username}, {user.password}, {user.name}, {user.surname}, {user.phone}))
        db.save_changes()
    except Error as e:
        # TODO: Find way to extract error message out
        return f"Error: {sys.exc_info()[1]}"


def pool_matching():
    db = DBHelper.get_instance()
    db.is_connected()
    # cursor = db.conn.cursor()
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
    # cursor.execute(sql_get_all)
    results = db.query(sql_get_all)

    if results == ():
        return "Pool is empty!!"

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
    db.query(sql_truncate)

    if not matched_ls:
        db.save_changes()
        return "No Matched"

    """
    Save matched result in matched table
    """
    sql_save_matched = """
              INSERT INTO `matched` 
              (`num`, `per_no`, `set_no`, `username`)
              VALUES(%s, %s, %s, %s) ON duplicate key update count=count+1; 
            """

    ls_of_tuple = [obj.to_tuple() for obj in matched_ls]
    db.query_many(sql_save_matched, ls_of_tuple)

    db.save_changes()

    return "Done"


def is_user_existed(username, password):
    db = DBHelper.get_instance()
    db.is_connected()
    # cursor = db.conn.cursor()
    sql = """
          SELECT EXISTS(SELECT username, password from user 
          WHERE username= %s and password= %s) as `is_existed`;  
    """

    try:
        results = db.query(sql, (username, password))
        db.save_changes()
        return results[0]["is_existed"], None
    except Error as e:
        # TODO: Find way to extract error message out
        return None, f"Error: {sys.exc_info()[1]}"


def submit_nums(username, obj_ls):
    db = DBHelper.get_instance()
    db.is_connected()

    # cursor = db.conn.cursor()
    sql_user = """
          SELECT user_id from user 
          where username= %s;  
    """
    user_result = db.query(sql_user, username)
    # user_result = cursor.fetchall()
    # db.conn.commit()

    if user_result == ():
        return False
    else:
        user_id = user_result[0]["user_id"]

        num_ls = [
            (item["num"], item["per_no"], item["set_no"], user_id)
            for item in obj_ls["numbers"]
        ]

        # for item in json_obj["numbers"]:
        #     small_ls = item.split("-") + [user_id]
        #
        #     num_ls.append(small_ls)

        sql_nums = """
          INSERT INTO `total_num` 
          (`num`, `per_no`, `set_no`, `user_id`)
          VALUES(%s, %s, %s, %s) ON duplicate key update count=count+1; 
        """
        db.query_many(sql_nums, num_ls)
        db.save_changes()

    return True


def remove_nums(username, obj_ls):
    db = DBHelper.get_instance()
    db.is_connected()
    # cursor = db.conn.cursor()

    sql_user = """
              SELECT user_id from user 
              where username= %s;  
        """
    user_result = db.query(sql_user, username)
    # user_result = cursor.fetchall()

    if user_result == ():
        return False
    else:
        # user_id = user_result[0]["user_id"]

        num_ls = [
            (item["num"], item["per_no"], item["set_no"])
            for item in obj_ls["numbers"]
        ]

        sql_nums = """
              DELETE FROM `total_num` 
              WHERE num = %s and per_no = %s and set_no = %s;
            """
        db.query_many(sql_nums, num_ls)
        db.save_changes()

    return True


def get_num_results(username, method: str):
    db = DBHelper.get_instance()
    db.is_connected()
    # cursor = db.conn.cursor()

    sql_matched = """
              SELECT num, per_no, set_no from matched
              where username= %s;  
        """

    sql_unmatched = """
              SELECT t.num, t.per_no, t.set_no
              FROM total_num t
              Inner join user u on t.user_id = u.user_id
              LEFT JOIN matched m ON t.num = m.num and t.set_no = m.set_no
              where m.per_no is null and u.username = %s;
        """

    sql_all = """
                  SELECT num, per_no, set_no from total_num t
                  Inner join user u on t.user_id = u.user_id 
                  where username= %s;  
            """

    sql_dict = {
        "matched": sql_matched,
        "unmatched": sql_unmatched,
        "all": sql_all
    }

    # cursor.execute(sql_dict[method], username)
    # results = cursor.fetchall()
    results = db.query(sql_dict[method], username)

    if results == ():
        return []
    else:
        db.save_changes()

        return results

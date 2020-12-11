import re
from dataclasses import dataclass
from typing import List
import numpy as np
import os
from pprint import pprint


@dataclass
class LottoNum:
    num: str
    per_no: str
    set_no: str


class NumPool:

    def __init__(self, num_ls: List[LottoNum]):
        self.num_ls: List[LottoNum] = num_ls
        self.pool: np.array = np.empty(shape=(20, 10), dtype=object)
        self.size = 0

        for obj in num_ls:

            row_index, col_index = self.get_pool_pos(obj)

            # print(f'Num:{obj.num}-{obj.set_no}, Row:{row_index}, Col:{col_index}')
            if self.pool[row_index][col_index] is None:
                self.pool[row_index][col_index] = f"{obj.num}-{obj.set_no},"
            else:
                self.pool[row_index][col_index] += f"{obj.num}-{obj.set_no},"

            self.size += 1

    def show(self):
        pprint(self.pool)

    def self_match(self):
        matched_ls = []
        for i, obj in enumerate(self.num_ls):

            row_index, col_index = self.get_pool_pos(obj)

            pool_value = self.pool[row_index][col_index]
            for value in NumPool.str_to_list(pool_value):

                value1, value2 = value.split("-")
                if obj.num == value1 and obj.set_no != value2:
                    matched_ls.append(obj)

        return matched_ls

    @staticmethod
    def get_pool_pos(obj: LottoNum):
        set_value = int(obj.set_no)
        if set_value % 5 == 0:
            row_index = int(set_value / 5) - 1
        else:
            row_index = int(set_value / 5)

        col_index = int(obj.num[-1])

        return row_index, col_index

    # TODO: Return as LottoNum obj would be better.
    # self.pool.size < another_pool.size --> For better execution time
    @staticmethod
    def match_pool(small_pool: np.array, big_pool: np.array) -> List[str]:
        matched_ls = []
        for row_index in range(small_pool.shape[0]):
            for col_index in range(small_pool.shape[1]):

                my_value = small_pool[row_index][col_index]
                another_value = big_pool[row_index][col_index]

                if (my_value is None) or (another_value is None):
                    continue
                for num in NumPool.str_to_list(my_value):

                    if num[:4] in another_value:
                        matched_ls.append(num)
        return matched_ls

    @staticmethod
    def match_pool_test(num_obj_ls, num_obj_ls2):
        """
        This method will matched only the 'num', not consider set_no

        :param num_obj_ls: List[LottoNum]
        :param num_obj_ls2: List[LottoNum]
        :return: List[LottoNum]
        """
        matched_ls = []
        for item in num_obj_ls:

            for item2 in num_obj_ls2:

                if item.num == item2.num:
                    matched_ls.append(item)
        return matched_ls

    # TODO: Use 'yield' instead of return
    @staticmethod
    def str_to_list(num_str: str):

        ls = num_str.split(",")
        ls.pop(-1)
        return ls


def main():
    # [1234] - [47] - [05] --> 0=num, 1=per_no, 2=set_no
    """
    Load real mock data
    """
    mock_path = "/Users/prial/Desktop/pplotto/mock_data"
    user_ls: List[LottoNum] = get_obj_ls(os.path.join(mock_path, "user1.txt"))
    user2_ls: List[LottoNum] = get_obj_ls(os.path.join(mock_path, "user2.txt"))
    # user3_ls = get_obj_ls(os.path.join(mock_path, "user3.txt"))
    # user4_ls = get_obj_ls(os.path.join(mock_path, "user4.txt"))
    # user5_ls = get_obj_ls(os.path.join(mock_path, "user5.txt"))

    # uniform_ls = get_obj_ls(os.path.join(mock_path, "uniform.txt"))
    # uniform_pool = NumPool(uniform_ls)

    """
    Instantiate pool obj
    """
    pool = NumPool(user_ls)
    pool2 = NumPool(user2_ls)
    # pool3 = NumPool(user3_ls)
    # pool4 = NumPool(user4_ls)
    # pool5 = NumPool(user5_ls)

    """
    Matching between pools
    """
    matched_ls = NumPool.match_pool(pool.pool, pool2.pool)

    # matched_ls = NumPool.match_pool_test(user_ls, user2_ls)

    # matched_ls = pool2.self_match()


    """
    Printing results out
    """
    pprint(matched_ls)
    print(len(matched_ls))


def get_obj_ls(file_path: str) -> List[LottoNum]:
    temp_file = open(file_path, 'r')

    num_ls = []
    for line in temp_file.readlines():
        ls = ls = re.sub('[\n]', '', line).split('-')
        num_ls.append(LottoNum(num=ls[0], per_no=ls[1], set_no=ls[2]))

    return num_ls


if __name__ == '__main__':
    main()

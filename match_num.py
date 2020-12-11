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

            set_value = int(obj.set_no)
            if set_value % 5 == 0:
                row_index = int(set_value / 5) - 1
            else:
                row_index = int(set_value / 5)

            col_index = int(obj.num[-1])

            # print(f'Num:{obj.num}-{obj.set_no}, Row:{row_index}, Col:{col_index}')
            if self.pool[row_index][col_index] is None:
                self.pool[row_index][col_index] = f"{obj.num}-{obj.set_no},"
            else:
                self.pool[row_index][col_index] += f"{obj.num}-{obj.set_no},"

            self.size += 1

    def show(self):
        pprint(self.pool)

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

    # TODO: Use 'yield' instead of return
    @staticmethod
    def str_to_list(num_str: str):

        temp = num_str.split(",")
        temp.pop(-1)
        return temp


def main():
    # [1234] - [47] - [05] --> 0=num, 1=per_no, 2=set_no
    mock_path = "/Users/prial/Desktop/pplotto/mock_data"
    temp_ls = get_obj_ls(os.path.join(mock_path, "test1.txt"))
    temp2_ls = get_obj_ls(os.path.join(mock_path, "p.txt"))

    # uniform_ls = get_obj_ls(os.path.join(mock_path, "uniform.txt"))
    # uniform_pool = NumPool(uniform_ls)

    pool = NumPool(temp_ls)
    pool2 = NumPool(temp2_ls)
    matched_ls = NumPool.match_pool(pool.pool, pool2.pool)

    print(matched_ls, len(matched_ls))
    for i, row in enumerate(pool2.pool[:]):
        print(f'{i}: {row}')
        print("---------------------")

    # import pdb; pdb.set_trace()


def get_obj_ls(file_path: str):
    temp_file = open(file_path, 'r')

    num_ls = []
    for line in temp_file.readlines():
        ls = ls = re.sub('[\n]', '', line).split('-')
        num_ls.append(LottoNum(num=ls[0], per_no=ls[1], set_no=ls[2]))

    return num_ls


if __name__ == '__main__':
    main()

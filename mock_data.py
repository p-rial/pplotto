from random import choice

import numpy as np
from pprint import pprint
import pickle


# possible pattern is 1 million
def gen_mock_data_random(amount: int):
    num_ls = []

    for _ in range(amount):
        num = ''
        for _ in range(4):
            num += choice('0123456789')
        rand = np.random.randint(low=10, high=50, size=2)

        num_ls.append(f"{num}-{str(rand[0])}-{str(rand[1])}")

    return num_ls


def gen_mock_real_data():
    # per_no = "47"
    f_num = open("/Users/prial/Desktop/pplotto/mock_data/possible_num.txt", "r")
    num_ls = f_num.read().split('\n')

    # Define number of user to mock here
    for i in range(1, 6):
        usr_ls = []
        for _ in range(1000):
            value = choice(num_ls)
            usr_ls.append(value)
            num_ls.remove(value)

        string = '\n'.join(usr_ls)
        with open(f'mock_data/user{i}.txt', 'w') as f:
            f.write(string)

    # for i in range(10000):
    #     num_str = str(i)
    #     if len(num_str) != 4:
    #         num_str = ((4 - len(num_str)) * '0') + num_str
    #
    #     for j in range(1, 51):
    #         set_str = str(j)
    #         if len(set_str) == 1:
    #             set_str = "0" + set_str
    #
    #         num_ls.append(f"{num_str}-{per_no}-{set_str}")

def gen_mock_data_uniform(num: str, per_no: str):
    num_ls = []

    for i in range(1, 101):
        set_no = str(i)
        if len(set_no) == 1:
            set_no = '0' + set_no

        num_ls.append(f"{num}-{per_no}-{set_no}")

    return num_ls


def main():
    pass
    # gen_mock_real_data()
    # string = '\n'.join(mock_ls)
    # with open('mock_data/possible_num.txt', 'w') as f:
    #     f.write(string)

    # mock_uniform_ls = gen_mock_data_uniform("1000", "47")
    # string = '\n'.join(mock_uniform_ls)
    # with open('mock_data/uniform.txt', 'w') as f:
    #     f.write(string)


if __name__ == "__main__":
    main()

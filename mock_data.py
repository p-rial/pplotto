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


def gen_mock_data_uniform(num: str, per_no: str):
    num_ls = []

    for i in range(1, 101):
        set_no = str(i)
        if len(set_no) == 1:
            set_no = '0' + set_no

        num_ls.append(f"{num}-{per_no}-{set_no}")

    return num_ls


def main():
    mock_ls = gen_mock_data_random(500)
    string = '\n'.join(mock_ls)
    with open('mock_data/p.txt', 'w') as f:
        f.write(string)

    # mock_uniform_ls = gen_mock_data_uniform("1000", "47")
    # string = '\n'.join(mock_uniform_ls)
    # with open('mock_data/uniform.txt', 'w') as f:
    #     f.write(string)


if __name__ == "__main__":
    main()

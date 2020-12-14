import json

from flask import Flask, request

from db.mysql import *
from models import User

app = Flask(__name__)


@app.route('/matched', methods=['GET'])
def get_matched():
    username = request.headers["Authorization"]

    results = get_num_results(username, method="matched")
    print(f'{username}-Amount : {len(results)}')
    return {"results": results}


@app.route('/unmatched', methods=['GET'])
def get_unmatched():
    username = request.headers["Authorization"]

    results = get_num_results(username, method="unmatched")
    print(f'{username}-Amount : {len(results)}')
    return {"results": results}


@app.route('/all', methods=['GET'])
def get_all():
    username = request.headers["Authorization"]

    results = get_num_results(username, method="all")
    print(f'{username}-Amount : {len(results)}')
    return {"results": results}


@app.route('/send-num', methods=['POST'])
def send_nums():
    username = request.headers["Authorization"]
    # print(username)
    data = request.get_json()

    status = submit_nums(username, data)

    return {"status": status}


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    result, error = is_user_existed(data["username"], data["password"])
    print(f"Result: {result}, error: {error}")
    if result is None:
        return {"status": error}

    return {"status": bool(result)}


@app.route('/logout', methods=['POST'])
def logout():
    pass


# Only admin can use this api through postman
@app.route('/signup', methods=['POST'])
def sign_up():
    if request.headers["Authorization"] != "pplotto112403":
        return {"status": "Unauthorized"}
    data = request.get_json()
    response: str = add_user(User(**data))
    if response is not None:
        return {"status": response}

    return {"status": True}


# Only admin can use this api through postman
@app.route('/execute-matching', methods=['POST'])
def execute_matching():
    if request.headers["Authorization"] != "pplotto112403":
        return {"status": "Unauthorized"}
    data = request.get_json()

    if data["username"] != "admin1234" or data["password"] != "1234":
        return {"status": "Unauthorized"}

    response = pool_matching()

    return {"status": response}


@app.route('/delete-num', methods=['POST'])
def delete_nums():
    username = request.headers["Authorization"]
    # print(username)
    data = request.get_json()

    status = remove_nums(username, data)

    return {"status": status}


@app.route('/update-info', methods=['PUT'])
def update_info():
    pass


def mock_num_body_request(filename):
    f_num = open(f"/Users/prial/Desktop/pplotto/mock_data/{filename}.txt", "r")
    temp_ls = f_num.read().split('\n')

    num_ls = []
    for item in temp_ls:
        ls = item.split("-")
        num_ls.append({"num": ls[0], "per_no": ls[1], "set_no": ls[2]})

    return {"numbers": num_ls}


if __name__ == '__main__':
    app.run(debug=True)
    # user1 = "p1234"
    # user2 = "pan1234"
    # user3 = "kob1234"
    #
    # user_obj = mock_num_body_request("user3")
    # user2_obj = mock_num_body_request("user4")
    # user3_obj = mock_num_body_request("user5")
    #
    # status = submit_nums(user1, user_obj)
    # status2 = submit_nums(user2, user2_obj)
    # status3 = submit_nums(user3, user3_obj)
    #
    # print(f"Status: {status}, Status2: {status2}, Status3: {status3}")

import json

from flask import Flask, jsonify, request

from db.mysql import *
from models import User

app = Flask(__name__)


@app.route('/matched', methods=['GET'])
def get_matched():
    return request.headers["Authorization"]


@app.route('/unmatched', methods=['GET'])
def get_unmatched():
    return request.headers["Authorization"]


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
    result, error = is_user_existed(data["username"], data["password"])

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
    pass


@app.route('/delete-num', methods=['DEL'])
def delete_nums():
    pass


@app.route('/update-info', methods=['PUT'])
def update_info():
    pass


def mock_num_body_request(filename):
    f_num = open(f"/Users/prial/Desktop/pplotto/mock_data/{filename}.txt", "r")
    num_ls = f_num.read().split('\n')
    return {"numbers": num_ls}


if __name__ == '__main__':
    app.run()
    # user1 = "p1234"
    # user2 = "pan1234"
    #
    # user_obj = mock_num_body_request("user1")
    # user2_obj = mock_num_body_request("user2")
    #
    # status = submit_nums(user1, user_obj)
    # status2 = submit_nums(user2, user2_obj)
    #
    # print(f"Status: {status}, Status2: {status2}")

import json

from flask import Flask, jsonify, request

from db.mysql import add_user
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
    data = request.get_json()
    print(data, type(data))

    return jsonify(data)


@app.route('/login', methods=['POST'])
def login():
    pass


@app.route('/logout', methods=['POST'])
def logout():
    pass


# Only admin can use this api through postman
@app.route('/signup', methods=['POST'])
def sign_up():
    data = request.get_json()
    response: str = add_user(User(**data))
    if response is not None:
        return response

    return data


# Only admin can use this api through postman
@app.route('/execute-matching', methods=['POST'])
def execute_matching():
    pass


@app.route('/delete-num', methods=['DEL'])
def delete_nums():
    pass


@app.route('/update-info', methods=['PUT'])
def update_info():
    pass


if __name__ == '__main__':
    app.run()

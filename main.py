from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)

ACCOUNTS_FILE = "accounts.json"

def read_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "w") as f:
            json.dump({"accounts": []}, f)
    with open(ACCOUNTS_FILE, "r") as f:
        return json.load(f)

def write_accounts(data):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    accounts_data = read_accounts()
    for account in accounts_data["accounts"]:
        if account["username"] == username:
            return jsonify({"status": "error", "message": "Username already exists"}), 400

    accounts_data["accounts"].append({"username": username, "password": password})
    write_accounts(accounts_data)
    return jsonify({"status": "success", "message": "Account created successfully"}), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    accounts_data = read_accounts()
    for account in accounts_data["accounts"]:
        if account["username"] == username and account["password"] == password:
            return jsonify({"status": "success", "message": "Login successful"}), 200

    return jsonify({"status": "error", "message": "Invalid username or password"}), 401


if __name__ == '__main__':
    app.run()

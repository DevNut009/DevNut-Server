from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)

DATA_FILE = "accounts.json"

# Make sure the file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"users": []}, f, indent=4)


@app.route('/')
def home():
    return jsonify({"message": "💻 DevNut Server is running!"})


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    with open(DATA_FILE, "r+") as f:
        accounts = json.load(f)
        # check if user already exists
        for u in accounts["users"]:
            if u["username"] == username:
                return jsonify({"error": "User already exists"}), 400

        accounts["users"].append({"username": username, "password": password})
        f.seek(0)
        json.dump(accounts, f, indent=4)

    return jsonify({"message": f"User '{username}' registered successfully!"})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    with open(DATA_FILE, "r") as f:
        accounts = json.load(f)
        for u in accounts["users"]:
            if u["username"] == username and u["password"] == password:
                return jsonify({"message": "Login successful!"})

    return jsonify({"error": "Invalid username or password"}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

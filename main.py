from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)

ACCOUNTS_FILE = "accounts.json"

# --- Helpers ---
def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "w") as f:
            json.dump([], f)
    with open(ACCOUNTS_FILE, "r") as f:
        return json.load(f)

def save_accounts(data):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Register ---
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"status": "error", "message": "Missing fields"})

    accounts = load_accounts()

    # Check if username or email already exists
    for acc in accounts:
        if acc["username"] == username:
            return jsonify({"status": "error", "message": "Username already exists"})
        if acc["email"] == email:
            return jsonify({"status": "error", "message": "Email already used"})

    # Add new user
    accounts.append({
        "username": username,
        "email": email,
        "password": password
    })
    save_accounts(accounts)

    return jsonify({"status": "success", "message": "Account created successfully!"})

# --- Login ---
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    accounts = load_accounts()

    for acc in accounts:
        if acc["email"] == email and acc["password"] == password:
            return jsonify({
                "status": "success",
                "message": "Login successful!",
                "username": acc["username"]
            })

    return jsonify({"status": "error", "message": "Invalid email or password"})

# --- Run locally for testing ---
if __name__ == "__main__":
    app.run(debug=True)

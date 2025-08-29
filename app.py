from flask import Flask, send_file, request, jsonify
from datetime import datetime

app = Flask(__name__)

db = {
    "users": [],
    "secret_code": "Meow=123$"
}

@app.route("/")
def index():
    return send_file("index.html")  # loads your existing HTML

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username").strip()
    password = data.get("password").strip()

    for u in db["users"]:
        if u["username"] == username:
            return jsonify({"success": False, "msg": "Username already exists"})
        if u["password"] == password:
            return jsonify({"success": False, "msg": "Password already used"})

    user = {"username": username, "password": password, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    db["users"].append(user)
    return jsonify({"success": True, "msg": "Account created successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username").strip()
    password = data.get("password").strip()

    for u in db["users"]:
        if u["username"] == username and u["password"] == password:
            return jsonify({"success": True, "msg": "Login successful"})
    return jsonify({"success": False, "msg": "Invalid username or password"})

@app.route("/secret", methods=["POST"])
def secret():
    data = request.json
    code = data.get("code")
    if code == db["secret_code"]:
        return jsonify({"success": True, "users": db["users"]})
    return jsonify({"success": False, "msg": "Incorrect secret code"})

if __name__ == "__main__":
    app.run(debug=True)

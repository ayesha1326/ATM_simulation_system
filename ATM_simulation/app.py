from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = "secret123"

FILE = "users.json"

def load_users():
    return json.load(open(FILE))

def save_users(users):
    json.dump(users, open(FILE, "w"), indent=4)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        if username in users and users[username]["password"] == password:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Invalid Login"

    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    users = load_users()
    user = users[session["user"]]

    if request.method == "POST":
        action = request.form["action"]
        amount = int(request.form["amount"])

        if action == "deposit" and amount > 0:
            user["balance"] += amount
            user["history"].append(f"Deposited Rs. {amount}")

        elif action == "withdraw" and amount <= user["balance"]:
            user["balance"] -= amount
            user["history"].append(f"Withdrawn Rs. {amount}")

        else:
            user["history"].append("Failed Transaction")

        save_users(users)

    return render_template("dashboard.html", balance=user["balance"], history=user["history"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
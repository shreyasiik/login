from flask import Flask, render_template, request, session, redirect, url_for
import hashlib

app = Flask(__name__)
app.secret_key = "super-secret-key"

VALID_CODES = [
    "0db431a5f590b7959e157f2906a2218c142a516949ee310c99fbb2965c00e5a8",
    "21dfe0cd1f7918b8cfa74a89953d09ad2c5963d042c063a2bd0e730af362e0cb"
]
UNLOCK_CODE = "specialunlockcode"

chat_messages = []  # Stores chat messages globally

def hash_code(code):
    return hashlib.sha256(code.encode()).hexdigest()

@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("locked_out"):
        if request.method == "POST":
            unlock_input = request.form["access_code"].strip()
            if unlock_input == UNLOCK_CODE:
                session.clear()
                return render_template("login.html", success_message="✅ Account unlocked! You can now try again.")
            else:
                return render_template("locked.html", error_message="🔓 Invalid unlock code. Try again.")
        return render_template("locked.html")

    if request.method == "POST":
        user_input = request.form["access_code"].strip()
        if "attempts" not in session:
            session["attempts"] = 0

        hashed_input = hash_code(user_input)

        if hashed_input in VALID_CODES:
            session["authenticated"] = True
            session.pop("attempts", None)

            if hashed_input == VALID_CODES[0]:
                session["username"] = "Mehtaji"
                return render_template("success.html", message="Access Granted, Mehtaji! 😉", video_file="mehta.mp4")
            elif hashed_input == VALID_CODES[1]:
                session["username"] = "Waterfight Loser"
                return render_template("success.html", message="Access Granted, Waterfight Loser! 💦", video_file="waterfight.mp4")
        else:
            session["attempts"] += 1
            if session["attempts"] >= 3:
                session["locked_out"] = True
                return render_template("locked.html", error_message="🚨 You are an imposter. Shreyasi shoots you. 💥")
            else:
                return render_template("login.html", error_message="Invalid code. Try again.")

    return render_template("login.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if not session.get("authenticated"):
        return redirect(url_for("index"))

    if request.method == "POST":
        message = request.form["message"].strip()
        username = session.get("username", "User")
        if message:
            chat_messages.append(f"{username}: {message}")
    return render_template("chat.html", messages=chat_messages)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

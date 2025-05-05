from flask import Flask, render_template, request, session, redirect, url_for 
import eventlet
eventlet.monkey_patch()

from flask_socketio import SocketIO, send
import hashlib

app = Flask(__name__)
app.secret_key = "super-secret-key"

socketio = SocketIO(app, async_mode="eventlet")


chat_messages = []

VALID_CODES = [
    "0db431a5f590b7959e157f2906a2218c142a516949ee310c99fbb2965c00e5a8",
    "21dfe0cd1f7918b8cfa74a89953d09ad2c5963d042c063a2bd0e730af362e0cb"
]
UNLOCK_CODE = "specialunlockcode"

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

        if hashed_input == VALID_CODES[0]:
            session.pop("attempts", None)
            session["logged_in"] = True
            session["username"] = "Mehtaji"
            return render_template("success.html", message="Access Granted, Mehtaji! 😉", video_file="mehta.mp4")

        elif hashed_input == VALID_CODES[1]:
            session.pop("attempts", None)
            session["logged_in"] = True
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

@app.route("/chat")
def chat():
    if not session.get("logged_in"):
        return redirect(url_for("index"))
    return render_template("chat.html", username=session["username"])

@socketio.on("message")
def handle_message(msg):
    user = session.get("username", "Anonymous")
    formatted = f"{user}: {msg}"
    chat_messages.append(formatted)
    send(formatted, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)

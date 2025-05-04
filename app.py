from flask import Flask, render_template, request, session
import hashlib

app = Flask(__name__)
app.secret_key = "super-secret-key"  # Needed for sessions

VALID_CODES = [
    "0db431a5f590b7959e157f2906a2218c142a516949ee310c99fbb2965c00e5a8",
    "21dfe0cd1f7918b8cfa74a89953d09ad2c5963d042c063a2bd0e730af362e0cb"
]
UNLOCK_CODE = "specialunlockcode"

def hash_code(code):
    return hashlib.sha256(code.encode()).hexdigest()

@app.route("/", methods=["GET", "POST"])
def index():
    # Lockout condition
    if session.get("locked_out"):
        if request.method == "POST":
            unlock_input = request.form["access_code"].strip()

            # Check if the unlock code is correct
            if unlock_input == UNLOCK_CODE:
                session.clear()  # Reset the session and attempts
                return render_template("login.html", success_message="✅ Account unlocked! You can now try again.")
            else:
                return render_template("locked.html", error_message="🔓 Invalid unlock code. Try again.")

        return render_template("locked.html")  # If locked out, show locked screen

    if request.method == "POST":
        user_input = request.form["access_code"].strip()

        # Initialize attempts if they are not already
        if "attempts" not in session:
            session["attempts"] = 0

        if hash_code(user_input) in VALID_CODES:
            session.pop("attempts", None)  # Reset attempts if login is successful
            return render_template("success.html")
        else:
            session["attempts"] += 1
            if session["attempts"] >= 3:
                session["locked_out"] = True
                return render_template("locked.html", error_message="🚨 You are an imposter. Shreyasi shoots you. 💥")
            else:
                return render_template("login.html", error_message="Invalid code. Try again.")
    
    return render_template("login.html")

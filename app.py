from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

# List of valid hashed access codes
AUTHORIZED_HASHES = [
    "0db431a5f590b7959e157f2906a2218c142a516949ee310c99fbb2965c00e5a8",  # "ps"
    "21dfe0cd1f7918b8cfa74a89953d09ad2c5963d042c063a2bd0e730af362e0cb"   # second code
]

def hash_code(code):
    return hashlib.sha256(code.encode()).hexdigest()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        access_code = request.form.get("access_code", "").strip()
        if hash_code(access_code) in AUTHORIZED_HASHES:
            return "<h2>Access Granted 😉 Welcome!</h2>"
        else:
            return "<h2>Access Denied 😠 Invalid Code</h2>"
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
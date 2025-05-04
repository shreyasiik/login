from flask import Flask, render_template, request, redirect, url_for
import hashlib

app = Flask(__name__)

# SHA-256 hash of valid access codes
VALID_CODES = [
    "0db431a5f590b7959e157f2906a2218c142a516949ee310c99fbb2965c00e5a8",  
    "21dfe0cd1f7918b8cfa74a89953d09ad2c5963d042c063a2bd0e730af362e0cb"   
]

def hash_code(code):
    """Hashes the access code using SHA-256."""
    return hashlib.sha256(code.encode()).hexdigest()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["access_code"].strip()
        
        # Check if the entered code matches any valid code
        if hash_code(user_input) in VALID_CODES:
            return render_template("success.html")
        else:
            # Return to login page with an error message
            return render_template("login.html", error_message="Invalid access code. Please try again.")
    
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)

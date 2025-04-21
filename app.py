from flask import Flask, render_template, request, redirect, flash, url_for
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

MESSAGES_FILE = "messages.json"

def save_message(data):
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r") as f:
            messages = json.load(f)
    else:
        messages = []

    messages.append(data)
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            flash("Please fill out all fields.")
        else:
            save_message({"name": name, "email": email, "message": message})
            flash("Message sent successfully!")
            return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route("/messages")
def messages():
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r") as f:
            messages = json.load(f)
    else:
        messages = []
    return render_template("messages.html", messages=messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


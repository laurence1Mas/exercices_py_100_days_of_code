
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to our E-Commerce Website!"


if __name__ == "__main__":
    app.run(debug=True)

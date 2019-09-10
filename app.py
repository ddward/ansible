from flask import Flask, render_template
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

@app.route("/")
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

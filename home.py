from flask import Flask, render_template

app = Flask(__name__)

from route.receive_json import app1
app.register_blueprint(app1)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template

app = Flask(__name__)

from route.receive_json import app1
from route.submit_json import app2
app.register_blueprint(app1)
app.register_blueprint(app2)

@app.route("/", methods=["GET"])
def home():
    data = {}
    return render_template("home.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)
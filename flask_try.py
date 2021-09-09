from flask import Flask

app = Flask(__name__)

@app.route("/test/<string:user>/<string:name>/")
def hello_world(user,name):
    return f"<p>Hello, {user} and {name}</p>"

app.run(debug=True)
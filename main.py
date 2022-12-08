from flask import Flask, render_template, request

app = Flask(__name__)

codes = []
last_id = 0

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/getcode", methods=['POST'])
def getcode():
    global last_id
    last_id += 1
    codes.append(last_id)

    return "Code:"+str(last_id)


if __name__ == "__main__":
    app.run("127.0.0.1", 8080)

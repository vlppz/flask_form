from flask import Flask, render_template, request, redirect

app = Flask(__name__)

codes = []
last_id = 0
rooms = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/strgame", methods=['POST'])
def getcode():
    global last_id
    last_id += 1
    codes.append(last_id)
    rooms.update({last_id: {'last_word': 'кот'}})

    return redirect('game.html')


if __name__ == "__main__":
    app.run("127.0.0.1", 8080)

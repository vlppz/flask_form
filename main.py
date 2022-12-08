import random
import string
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

last_id = '0'
rooms = {}


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/start", methods=['POST', 'GET'])
def getcode():
    global last_id
    last_id = ''.join([random.choice(string.ascii_lowercase+string.digits) for _ in range(10)])
    rooms.update({last_id: {'last_word': 'кот'}})

    return redirect(f'/game?code={last_id}')


@app.route('/game', methods=["POST", "GET"])
def game():
    code = request.args['code']
    try:
        room = rooms[code]
    except KeyError:
        return '<h1>Error: No such Room!</h1><br>This room was closed or was never existing'

    return render_template('game.html', code=code)


if __name__ == "__main__":
    app.run("127.0.0.1", 8080)

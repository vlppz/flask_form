import random
import string
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

last_id = '0'
rooms = {'1': {'words': ['кот'], 'users': [], 'host': 'макс'}}
sessions = {}

words2 = ["кот", "собака", "арбуз", "мандарин"]

errors = {
  '100': 'Игрок уже существует!',
  '101': 'Сессия была закрыта!',
  '102': 'Не правильный код комнаты',
  '103': 'Неправильное слово'
}


@app.route("/", methods=['POST', 'GET'])
def main_page():

  return render_template("index.html",
                         error=errors[request.args['error']]
                         if request.args.get('error', False) else '')


@app.route('/close/<session>')
def close(session):
  global rooms
  user = False
  for i in sessions:
    if sessions[i] == session:
      user = i

  roomsz = rooms.copy()
  for i in rooms:
    if user in rooms[i]['users']:
      rooms[i]['users'].remove(user)
      if rooms[i]['host'] == user:
        roomsz.pop(i)

  rooms = roomsz.copy()

  sessions.pop(user)
  return redirect('/')


@app.route("/start", methods=['POST', 'GET'])
def start():
  global last_id
  last_id = ''.join(
    [random.choice(string.ascii_lowercase + string.digits) for _ in range(10)])
  rooms.update({
    last_id: {
      'words': [random.choice(words2)],
      'users': [],
      'host': request.args["name"]
    }
  })

  return redirect(f'/login?code={last_id}&name={request.args["name"]}')


@app.route('/login', methods=["POST", "GET"])
def login():
  code = request.args['code']
  name = request.args['name']
  session_id = ''.join(
    [random.choice(string.ascii_lowercase + string.digits) for _ in range(10)])
  sessions.update({name: session_id})
  try:
    room = rooms[code]
  except KeyError:
    return redirect('/?error=102')
  if name not in room['users']:
    room['users'].append(name)
  else:
    return redirect('/?error=100')
  return redirect(f'/game/{code}?name={name}&session={session_id}')


@app.route('/game/<code>', methods=["POST", "GET"])
def game(code):
  name = request.args['name']
  session = request.args['session']
  if request.args.get('message', False):
    word = request.args.get('message', False)
    lastword = rooms[code]["words"][-1]

    if ((word[0].lower() == lastword[-1].lower())
        and (word.lower() not in rooms[code]["words"])):
      rooms[code]["words"].append(request.args.get('message', False).lower())
      return redirect(f'/game/{code}?name={name}&session={session}')
    else:
      return redirect(f"/game/{code}?name={name}&session={session}&error=103")
  try:
    room = rooms[code]
  except KeyError:
    return '<h1>Ошибка: Не правильный код комнаты</h1><br>Эта комната была закрыта ее хозяином либо никогда не ' \
           'существовала'
  try:
    if sessions[name] == session:
      return render_template('game.html',
                             code=code,
                             name=name,
                             users=room['users'],
                             words=room['words'],
                             session=session,
                             error=errors[request.args['error']]
                             if request.args.get('error', False) else '')
    else:
      return redirect('/')
  except KeyError:
    return redirect('/?error=101')


if __name__ == "__main__":
  app.run("0.0.0.0", 80)

from flask import Flask, render_template, request

app = Flask(__name__)

codes = {}
c = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getcode", methods=['POST'])
def getcode():
    global codes
    global c

    codes.update({request.values.get("usrname"): c})
    c+=1

    print(codes)

    return "Code:"+str(c)

@app.route("/smsg")

if __name__ == "__main__":
    app.run("127.0.0.1", 8080)
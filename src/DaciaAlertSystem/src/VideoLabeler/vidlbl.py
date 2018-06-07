from flask import Flask
from flask import render_template
from flask import request
import vidtest as vid

app = Flask(__name__)

def dict_to_run_params(d):
    i=0
    key_check = "starttime"+str(i)
    times=[]
    while key_check in d:
        times.append(d["starttime"+str(i)])
        times.append(d["endtime"+str(i)])
        i=i+1
        key_check = "starttime"+str(i)
    print(times)
    return d['vidfilepath'],times




@app.route("/")
def hello():
    return render_template("hello.html")

@app.route("/submit",methods=['POST'])
def submit():
    vid.run(dict_to_run_params(request.form.to_dict()))

    return "hello"

#! /usr/bin/python3
from flask import Flask, render_template
 
app = Flask(__name__)

@app.route("/")
def index():
 list_example = [(1,"Alvin"), (2,"Simon"), (3,"Theodore")]
 return render_template("format.html", movies=list_example)
 
if __name__ == "__main__":
 app.run(debug=True ,port=5001)
 app.secret_key = "mysecret1232"

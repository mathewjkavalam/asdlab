#!/usr/bin/python

from flask import Flask,render_template,redirect,request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('homepage', title="imdbClone", h1="IMDBClone")
@app.route('/page1')
def page1():
    return render_template('page1')
@app.route('/page2')
def page2():
    return render_template('page2')

@app.route('/search',methods = ['POST'])
def search():
    global found
    global keywordFlask
    keywordFlask = request.form['keyword']
    print("keyword:",keywordFlask)
    ##searching
    main()
    if found == 1:
      redirect("/page1")
    if found == 2:
      redirect("/page2")
    redirect("/")
    return " "

def search_button():
    return 'search'

if __name__ == '__main__':
    app.run()

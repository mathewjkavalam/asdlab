#!/usr/bin/python

from flask import Flask,render_template,redirect,request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
@app.route('/')
def home_page():
    return render_template('homepage.html')
@app.route('/listAll.html')
def listAll_page():
    #query db get all rows of slno,movie names
    conn = sqlite3.connect("DB.sqllite3")
    conn.row_factory = sqlite3.Row
    cur = conn.execute('select slno,title from IMDB order by slno')
    allmovies = cur.fetchall()
    return render_template('listAll.html',movies=allmovies)
@app.route('/top50.html')
def top50_page():
    return render_template('top50.html')
@app.route('/details/<int(min=1,max=100):sl>')
def show_details_page(sl):
    #quer all details
    conn = sqlite3.connect("DB.sqllite3")
    conn.row_factory = sqlite3.Row
    #check!!
    cur = conn.execute('select Title,Director,Rating,Genre from IMDB where slno='+str(sl))
    details = cur.fetchall()
    print details
    (m,d,r,g) = details[0]
    return render_template('details.html',movieName=m,director=d,rating=r,genre=g)

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

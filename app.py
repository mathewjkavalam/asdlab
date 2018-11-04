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
    cur = conn.execute('select slno,title from IMDB order by title')
    allmovies = cur.fetchall()
    return render_template('listAll.html',movies=allmovies)
@app.route('/top50.html')
def top50_page():
    conn = sqlite3.connect("DB.sqllite3")
    conn.row_factory = sqlite3.Row
    cur = conn.execute('select slno,title from IMDB order by slno')
    allmovies = cur.fetchall()
    return render_template('top50.html',movies=allmovies)
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
    keywordFlask = request.form['keyword']
    print("keyword:",keywordFlask)
    found = -1
    conn = sqlite3.connect("DB.sqllite3")
    conn.row_factory = sqlite3.Row
    cur = conn.execute('select slno from IMDB where Title like ?', ['%' + keywordFlask + '%'])
    allmovies = cur.fetchall()
    print allmovies[0]
    found, = allmovies[0]
    if found>=1 and found <=100:
      return redirect("/details/"+str(found))
    else:
      return redirect('/')

if __name__ == '__main__':
    app.run()

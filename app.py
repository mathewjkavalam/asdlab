#!/usr/bin/python

from flask import Flask,render_template,redirect,request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
notlogged = True
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
    conn.close()
    return render_template('listAll.html',movies=allmovies)
@app.route('/top50.html')
def top50_page():
    conn = sqlite3.connect("DB.sqllite3")
    conn.row_factory = sqlite3.Row
    cur = conn.execute('select slno,title from IMDB order by slno')
    allmovies = cur.fetchall()
    conn.close()
    return render_template('top50.html',movies=allmovies)
@app.route('/details/<int(min=1,max=100):sl>')
def show_details_page(sl):
    #quer all details
    global notlogged
    conn = sqlite3.connect("DB.sqllite3")
    conn.row_factory = sqlite3.Row
    #check!!
    cur = conn.execute('select Title,Director,Rating,Genre,u_rating from IMDB where slno='+str(sl))
    details = cur.fetchall()
    conn.close()
    print details
    (m,d,r,g,u) = details[0]
    return render_template('details.html',slno= sl,movieName=m,director=d,rating=r,genre=g,urating=u,notlogged = notlogged)
@app.route('/login')
def login():
  return render_template('login.html')
@app.route('/checklogin',methods=['POST'])
def checklogin():
  global notlogged
  username = request.form['username'] 
  password = request.form['password']
  print "username,password",username,password
  conn = sqlite3.connect("DB.sqllite3")
  conn.row_factory = sqlite3.Row
  cur = conn.execute("select password from userlog where username = ?",(username,))
  real_pass , = cur.fetchall()[0]
  if len(real_pass) > 0:
	print "real_pass == password",real_pass == password 
  	conn.close()
  	if real_pass == password:
    	   notlogged = False
  	else:
           notlogged = True
        print notlogged
  conn.close()  
  return redirect('/')
@app.route('/register')
def goto_register():  
  return render_template('register.html')

@app.route('/registered',methods=['POST'])
def register():
  global notlogged
  username = request.form['username'] 
  password = request.form['password']
  print "username,password",username,password
  conn = sqlite3.connect("DB.sqllite3")
  conn.row_factory = sqlite3.Row
  try:
    conn.execute("insert into userlog(username,password) values(?,?)",(username,password,))
  except:
    pass  
  conn.commit()
  notlogged = False
  print notlogged
  conn.close()  
  return redirect('/')
      
@app.route('/search',methods = ['POST'])
def search():
    keywordFlask = request.form['keyword']
    print("keyword:",keywordFlask)
    found = -1
    conn = sqlite3.connect("DB.sqllite3")
    conn.row_factory = sqlite3.Row
    cur = conn.execute('select slno from IMDB where Title like ?', ['%' + keywordFlask + '%'])
    allmovies = cur.fetchall()
    conn.close()
    print allmovies[0]
    found, = allmovies[0]
    if found>=1 and found <=100:
      return redirect("/details/"+str(found))
    else:
      return redirect('/')
@app.route('/rated/<int(min=1,max=100):sln>')
def rated(sln):
  if notlogged == False:
	  conn = sqlite3.connect("DB.sqllite3")
	  conn.row_factory = sqlite3.Row
	  conn.execute('update IMDB set u_rating = u_rating + 1  where slno='+str(sln))
	  conn.commit()
	  conn.close()
  else:
    pass
  return redirect('/details/'+str(sln))
@app.route('/logout')
def logout():
  global notlogged
  notlogged = True
  return redirect('/')
if __name__ == '__main__':
    app.run()

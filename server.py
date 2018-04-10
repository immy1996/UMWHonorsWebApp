from flask import Flask, render_template, session, request, redirect, url_for
import psycopg2, psycopg2.extras, os
app = Flask(__name__)
import psycopg2, psycopg2.extras, os, random
import uuid
import pprint
import datetime
import os

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'

userIsAdmin = False
failedSresult = False
SignedInButton = False

def connectToDB():
  
  try:
    return psycopg2.connect(os.environ.get('DATABASE_URL'))
  except:
    print("Can't connect to database")


@app.route('/', methods=['GET', 'POST'])
def mainIndex():
    #connecting to database
    connection = connectToDB()
    #cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor = connection.cursor()
    try:
        print('User: ' + session['username'])
    except:
        session['username'] = ''

    global userIsAdmin
    global failedSresult
    global SignedInButton
    returnedUserInfo = ''
    announcementCount = 0
    announceList = []

    print("BEFORE POST")

     # if user typed in a post ...
    if request.method == 'POST':
          username = request.form['userName']
          print('incoming username ' + username)
          pw = request.form['pw']
          try: 
            
            cursor.execute("SELECT student_info.email, user_info.userid, user_info.isadmin FROM student_info FULL OUTER JOIN user_info ON (student_info.email = userid) WHERE (student_info.email = %s AND dupont_code = %s) OR (user_info.userid = %s AND user_info.password = %s);", (username, pw, username, pw))
            
            returnedUserInfo = cursor.fetchone()

            #If a user-pwd combo was found and it matches then log the person in
            if returnedUserInfo:
              print("user credentials found...")
              SignedInButton = False
              session['username'] = username
              session['loggedIn']=True 
              
              if returnedUserInfo[2] == 'y':
                userIsAdmin=True
              else:
                userIsAdmin=False
            else:
                session['loggedIn']=False
                session['username']=''
                SignedInButton = True
                userIsAdmin=False
                print("SignedInButton STATUS*********")
                print(SignedInButton)
                return redirect(url_for('mainIndex'))

          except:
            print("Error accesing from users table when logging in")
    print('Username: ' + session['username'])
    if session['username'] == '':
        session['loggedIn'] = False
        print("Nobody is currently logged in.") 
    else:
       session['loggedIn'] = True
       print('User: ' + session['username'] + ' is logged in, this is in MAIN FUNCTION')

    print("AFTER POST")

    #announcements
    try:
      mogAnnounce = cursor.mogrify("select * from announcements;")
      print(mogAnnounce)
      cursor.execute(mogAnnounce)
      resultsAnnounce = cursor.fetchall()
      print(resultsAnnounce)
      print(len(resultsAnnounce))
      announcementCount = len(resultsAnnounce)
      print("ANNOUNCEMENTCOUNT")
      print(announcementCount)
      print(type(announcementCount))
      
      
      print("BEFORE MOGRIFY")
      announceInfo = cursor.mogrify("select * from announcements where postid = %s;", (announcementCount, ))
      print(announceInfo)
      print("AFTER MOGRIFY")
      cursor.execute(announceInfo)
      A = cursor.fetchone()
      announceList.append(A)
      print(announceList)
      print(type(announceList))

    except:
      print(cursor.mogrify("select * from announcements where postid = %s;", (announcementCount, )))


    print("PRINT RETURNEDUSERINFO BEFORE COMMIT")

    connection.commit()

    print("PRINT RETURNEDUSERINFO")

    return render_template('home.html', loggedIn=session['loggedIn'], user=session['username'], adminView=userIsAdmin, announceList = announceList, failedSresult=failedSresult, failed = SignedInButton)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    #Username is nothing and loggedIn is false
    session['username'] = ''
    session['loggedIn'] = False
    return redirect(url_for('mainIndex'))
    
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html', loggedIn=session['loggedIn'],  user=session['username'], adminView = userIsAdmin)
    
@app.route('/announcement', methods=['GET','POST'])
def announcements():
    #Connect to DB
    connection = connectToDB()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        print('User: ' + session['username'] + ' in announcement function')
    except:
        session['username'] = ''
        

    post = False

    if request.method == 'POST':
        print("Inserting announcements")          
        
        try: 
          d = datetime.date.today()
          print( cursor.mogrify("INSERT into announcements (announcement_title, announcement_text, post_date) VALUES (%s, %s, now());", (request.form['title'], request.form['announcement']) ))
          query = cursor.mogrify("INSERT into announcements (announcement_title, announcement_text, post_date) VALUES (%s, %s, now());", (request.form['title'], request.form['announcement']) )
          #Execute on the db
          cursor.execute( query )
        
          post = True
          
          print("SUCCESSFULLLLLY INSERRTETDDDDDDDDDDDD")

          connection.commit()
          
        except:
            post = False
            print("Error inserting into announcements table!")
            print("Tried: INSERT into announcements (announcement_title, announcement_text, post_date) VALUES (%s, %s, now());", (request.form['title'], request.form['announcement']) )
            connection.rollback()
          
    session['loggedIn'] = True
    return render_template('announcements.html', loggedIn=session['loggedIn'], user=session['username'], adminView = userIsAdmin, posted = post)
    
@app.route('/previousannouncements', methods=['GET','POST'])
def allAnnouncements():
    #Connect to DB
    connection = connectToDB()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        print('User: ' + session['username'] + ' in announcement function')
    except:
        session['username'] = ''
        
    allAnnounceList = []    
    
    try:    
      mogallAnnounce = cursor.mogrify("select * from announcements;")
      print("BEFORE MOGALLANNOUNCE")
      print(mogallAnnounce)
      cursor.execute(mogallAnnounce)
      print("AFTER EXECUTE")
      resultsAnnounce = cursor.fetchall()
      print("AFTER FETCHALL")
      print(resultsAnnounce)
      #A = cursor.fetchone()
      #print(A)
      #allAnnounceList.append(A)
      #print(allAnnounceList)
      print("ATTEMPTING TO REVERSE THE LIST")
      print(resultsAnnounce[::-1])
      
    except:
      print("ERROR! Tried " + cursor.mogrify("select * from announcements;") )

    return render_template('allAnnouncements.html', loggedIn=session['loggedIn'],  user=session['username'], allAnnounceList = resultsAnnounce[::-1], adminView = userIsAdmin)

@app.route('/studentresult', methods=['GET','POST'])
def searchstudent():
    print("IN STUDENT RESULT")
  
    #Connect to DB
    connection = connectToDB()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        print('User: ' + session['username'] + ' in announcement function')
    except:
        session['username'] = ''
        
    global failedSresult    
    studentList = []  

    try:    
      mogstudentResult = cursor.mogrify("select * from student_info where lastname = %s and firstname = %s;", (request.form['lname'], request.form['fname']) )
      print("BEFORE MOGALLANNOUNCE")
      print(mogstudentResult)
      cursor.execute(mogstudentResult)
      print("AFTER EXECUTE")
      studentList = cursor.fetchall()
      print("AFTER FETCHALL")
      print("PRINTING STUDENTLIST NOW")
      print(studentList)
      failedSresult = False
      
      if studentList == []:
        failedSresult = True
        return redirect(url_for('mainIndex'))
        
      print("PRINTING FAILEDSRESULT STATUS")
      print(failedSresult)

    except:
      print("ERROR! Tried " + cursor.mogrify("select * from student_info where lastname = %s and firstname = %s;", (request.form['lname'], request.form['fname']) ) )    
  
  
    return render_template('listofstudent.html', loggedIn=session['loggedIn'],  user=session['username'], studentList=studentList, adminView = userIsAdmin, failedSresult=failedSresult)

@app.route('/mychecksheet', methods=['GET','POST'])
def searchownchecksheet():
    print("IN MY CHECKSHEET RESULT RESULT")
  
    #Connect to DB
    connection = connectToDB()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        print('User: ' + session['username'] + ' in announcement function')
        ourName = session['username']
        print('ourName: ' + ourName)
        
    except:
        session['username'] = ''
        
    print("Before Def failedSResult")
    global failedSresult    
    studentList = []  

    try:    
      print("Before SELECT statement")
      
      mogstudentResult = cursor.mogrify("select * from student_info where email = %s;", (ourName, ) )
      
      print("BEFORE MOGALLANNOUNCE")
      print(mogstudentResult)
      cursor.execute(mogstudentResult)
      print("AFTER EXECUTE")
      studentList = cursor.fetchall()
      print("AFTER FETCHALL")
      print("PRINTING STUDENTLIST NOW")
      print(studentList)
      failedSresult = False
      
      if studentList == []:
        failedSresult = True
        return redirect(url_for('mainIndex'))
        
      print("PRINTING FAILEDSRESULT STATUS")
      print(failedSresult)

    except:
      print("ERROR! Tried " + cursor.mogrify("select * from student_info where email = %s;", (request.form['lname'], request.form['fname']) ) )    
  
  
    return render_template('listofstudent.html', loggedIn=session['loggedIn'],  user=session['username'], studentList=studentList, adminView = userIsAdmin, failedSresult=failedSresult)


@app.route('/upload', methods=['POST'])
def upload():
   print("IN UPLOAD")

   uploadFailed = False

   #Connect to DB
   connection = connectToDB()
   cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
   try:
      print('User: ' + session['username'] + ' in upload function')
   except:
      session['username'] = ''
        
   try:
      uploadfile = request.files['csvfile']
      uploadfile.save(os.path.join(app.root_path, 'static/csvfiles/data.csv'))
      
      cursor.execute("delete from student_info;")
      copy_sql = """
                 COPY student_info FROM stdin WITH CSV HEADER
                 DELIMITER as ','
                 """
      with open(os.path.join(app.root_path, 'static/csvfiles/data.csv'), 'r') as f:
         print("file opened")
         cursor.copy_expert(sql=copy_sql, file=f)
         connection.commit()
      
      cursor.execute("update student_info set dupont_code = crypt('dupont_code', gen_salt('md5'));")
      connection.commit()
      cursor.close()
      print("done inserting?")
   except:
      print("ERROR! Tried ")
      uploadFailed = True 
  
  
   return render_template('uploaded.html', loggedIn=session['loggedIn'],  user=session['username'], adminView = userIsAdmin, uploadFailed = uploadFailed)

# start the server
if __name__ == '__main__':
     app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)
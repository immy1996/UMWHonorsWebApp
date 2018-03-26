from flask import Flask, render_template, session, request, redirect, url_for
import psycopg2, psycopg2.extras, os
app = Flask(__name__)
import psycopg2, psycopg2.extras, os, random
import uuid
import pprint
import datetime

userIsAdmin = False

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'

def connectToDB():
  connectionString = 'dbname=honors_program user=umwhonors password=umw host=localhost'
  try:
    return psycopg2.connect(connectionString)
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
    returnedUserInfo = ''

    print("BEFORE POST")
    #print(session['admin']) 

     # if user typed in a post ...
    if request.method == 'POST':
          username = request.form['userName']
          print('incoming username ' + username)
          pw = request.form['pw']
          session['SignedInButton'] = False
          SignedInButton = session['SignedInButton']
          try: 
            print(cursor.mogrify("select * from user_info WHERE userid = %s AND password = %s;", (username, pw)))
            cursor.execute("select * from user_info WHERE userid = %s AND password = %s;" , (username, pw))
            
            returnedUserInfo = cursor.fetchone()

            #If a user-pwd combo was found and it matches then log the person in
            if returnedUserInfo:
              print("username and password match found...")
              SignedInButton = False
              session['username'] = username
              session['loggedIn']=True 
                        
              print(returnedUserInfo)
              if returnedUserInfo[2] == 'y':
                print("We are an admin")
                userIsAdmin = True
              else:
                print("We are a student")
                userIsAdmin = False
            else:
              session['loggedIn']=False
              session['username']=''
              SignedInButton = True
              return render_template('login.html', failed = SignedInButton)

          except:
            print("Error accesing from users table when logging in")
            print(cursor.execute("select * from user_info WHERE userid = %s AND password = %s;" , (username, pw)))
    print('Username: ' + session['username'])
    if session['username'] == '':
        session['loggedIn'] = False
        print("Nobody is currently logged in.") 
    else:
       session['loggedIn'] = True
       print('User: ' + session['username'] + ' is logged in, this is in MAIN FUNCTION')

    print("AFTER POST")
    #print(session['admin'] )


    print("PRINT RETURNEDUSERINFO BEFORE COMMIT")

    connection.commit()

    print("PRINT RETURNEDUSERINFO")

    return render_template('home.html', loggedIn=session['loggedIn'], user=session['username'], adminView = userIsAdmin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #Connect to DB
    connection = connectToDB()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #Try to print the user, if not logged in this will throw an error and we set username to an empty string
    
    global userIsAdmin
    returnedUserInfo = ''
    session['loggedIn'] = False
    
    try:
        print('User: ' + session['username'])
    except:
        session['username'] = ''
        
    # if user tried to log in ...
    if request.method == 'POST':
          #Get username
          username = request.form['userName']
          print('incoming username ' + username)
          
          #Get password
          pw = request.form['pw']
          session['SignedInButton'] = False
          SignedInButton = session['SignedInButton']
          #Try and find the user and password combo in the table
          try: 
            #Print the query running
            print(cursor.mogrify("select * from user_info WHERE userid = %s AND password = %s;", (username, pw)))

            #Execute on the db
            cursor.execute("select * from user_info WHERE userid = %s AND password = %s;" , (username, pw))
            
            returnedUserInfo = cursor.fetchone()
            
            #If a user-pwd combo was found and it matches then log the person in
            if returnedUserInfo:
              print("username and password match found...")
              SignedInButton = False
              session['username'] = username
              session['loggedIn']=True 
              
              #print("Attempting cursor fetch")
              #returnedUserInfo = cursor.fetchone()
              
              if returnedUserInfo[2] == 'y':
                print("We are an admin")
                userIsAdmin = True
              else:
                print("We are a student")
                userIsAdmin = False
            else:
              session['loggedIn']=False
              session['username']=''
              SignedInButton = True
              return render_template('login.html', failed = SignedInButton)
          except:
              print("after return statement")
              print("Error accesing from users table when logging in whyyyy")
              #print(cursor.execute("select * from user_info WHERE userid = %s AND password = crypt(%s, password);" , (username, pw)))

    print('Username: ' + session['username'] + ' in login function')
    
    #Go to home page
    return render_template('home.html', loggedIn=session['loggedIn'], user=session['username'], adminView = userIsAdmin)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    #Username is nothing and loggedIn is false
    session['username'] = ''
    session['loggedIn'] = False
    return redirect(url_for('mainIndex'))
    
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    session['loggedIn'] = False
    return render_template('contact.html', loggedIn=session['loggedIn'])
    
@app.route('/announcement', methods=['GET','POST'])
def announcements():
    try:
        print('User: ' + session['username'] + ' in announcement function')
    except:
        session['username'] = ''
        

    #Connect to DB
    connection = connectToDB()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        print('User: ' + session['username'] + ' in announcement function')
    except:
        session['username'] = ''
        

    posted = False

    if request.method == 'POST':
        print("Inserting announcements")          
        
        try: 
          d = datetime.date.today()
          print( cursor.mogrify("INSERT into announcements (announcement_title, announcement_text, post_date) VALUES (%s, %s, now());", (request.form['title'], request.form['announcement']) ))
          query = cursor.mogrify("INSERT into announcements (announcement_title, announcement_text, post_date) VALUES (%s, %s, now());", (request.form['title'], request.form['announcement']) )
          #Execute on the db
          cursor.execute( query )
        
          posted = True
          
          print("SUCCESSFULLLLLY INSERRTETDDDDDDDDDDDD")

          connection.commit()

          return redirect(url_for('mainIndex'))
          
        except:
            posted = False
            print("Error inserting into announcements table!")
            print("Tried: INSERT INTO users (username, password) VALUES (%s, %s);" , 
                  (request.form['userName'], request.form['pw']) )
            connection.rollback()
          
    userIsAdmin = True
    session['loggedIn'] = True
    return render_template('announcements.html', loggedIn=session['loggedIn'], user=session['username'], adminView = userIsAdmin)
    
  
# start the server
if __name__ == '__main__':
     app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)
from flask import Flask, render_template, session, request, redirect, url_for
import psycopg2, psycopg2.extras, os
app = Flask(__name__)
import psycopg2, psycopg2.extras, os, random
import uuid
import pprint


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
        
    adminT = False
    studentT = False    
    userIsAdmin = False
        
     # if user typed in a post ...
    if request.method == 'POST':
          username = request.form['userName']
          print('incoming username ' + username)
          pw = request.form['pw']
          try: 
            print(cursor.mogrify("select * from user_info WHERE userid = %s AND password = %s;", (username, pw)))
            cursor.execute("select * from user_info WHERE userid = %s AND password = %s;" , (username, pw))
            
            returnedUserInfo = cursor.fetchone()
            
            pprint.pprint(returnedUserInfo)
            
            for row in returnedUserInfo:
                print row[0]
                print"    ", returnedUserInfo
                print("before isAdmin is equal to yes")
                print row[2]
                if row[2] == 'y':
                  print("After isAdmin is equal to yes")
                  adminT = True
                  studentT = False
                elif row[2] == 'n':
                  print("Student is equal to isAdmin")
                  adminT = False
                  studentT = True


            if cursor.fetchone():
              print("got here")
              session['username'] = username
              session['loggedIn']=True
              print adminT
              print studentT
            else:
              session['loggedIn']=False
              session['username']=''
          except:
            print("Error accesing from users table when logging in")
            print(cursor.execute("select * from user_info WHERE userid = %s AND password = %s;" , (username, pw)))
    print('Username: ' + session['username'])
    if session['username'] == '':
        session['loggedIn'] = False
        print("Nobody is currently logged in.") 
    else:
       session['loggedIn'] = True
       print('User: ' + session['username'] + ' is logged in')
    
    connection.commit()
    
    return render_template('home.html', loggedIn=session['loggedIn'], user=session['username'], adminView = userIsAdmin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #Connect to DB
    connection = connectToDB()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #Try to print the user, if not logged in this will throw an error and we set username to an empty string
    
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
              else:
                print("We are a student")
              
              return redirect(url_for('mainIndex'))
            #If not, then they aren't logged in, you want to put something here to let the person know that it did not work out
            else:
              print("Invalid username or password!")
              connection.rollback()
              SignedInButton = True
              session['loggedIn']=False
              session['username']=''
              print("before return statement")
              return render_template('login.html', failed = SignedInButton, loggedIn=session['loggedIn'], user=session['username'])
          except:
            print("after return statement")
            print("Error accesing from users table when logging in whyyyy")
            #print(cursor.execute("select * from user_info WHERE userid = %s AND password = crypt(%s, password);" , (username, pw)))

    print('Username: ' + session['username'])
    
    #Go to home page


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    #Username is nothing and loggedIn is false
    session['username'] = ''
    session['loggedIn'] = False
    return redirect(url_for('mainIndex'))
    
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')
  
# start the server
if __name__ == '__main__':
     app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)
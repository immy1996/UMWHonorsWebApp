import os
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def helloWorld():
    return render_template('home.html')
    
@app.route('/login')
def loginPage():
    return render_template('login.html')
    
# start the server
if __name__ == '__main__':
     app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)
from flask import Flask, render_template, url_for, redirect, request, session
from flask_bcrypt import Bcrypt
import sqlite3
import subprocess
debug_on = True

app = Flask(__name__)
bcrypt = Bcrypt(app) # an encryption lib
app.config.update(SECRET_KEY="themusicdictionary") # setting the secret key for the session


@app.route('/')
def hello():
  # if debug_on: # preventing access while a patch is being applied or dev is on..
  #   return "brb."
  
  # passing the session data to change the display for a signed in user
  return render_template("landingPage.html", data=session)

          
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)
     


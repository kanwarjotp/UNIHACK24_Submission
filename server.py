from flask import Flask, render_template, url_for, redirect, request, session
import databaseLogic

import sqlite3
import subprocess
debug_on = True

app = Flask(__name__)



@app.route('/')
def hello():
  # if debug_on: # preventing access while a patch is being applied or dev is on..
  #   return "brb."

  startData = databaseLogic.extractData(first=True)
  # this is the set containing first input
  
  # passing the session data to change the display for a signed in user
  return render_template("landingPage.html", data=startData)




@app.route('/userDislike')
def removeImg():
  pass

@app.route('/userLike')
def keepImg():
  pass
          
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug="True")
     


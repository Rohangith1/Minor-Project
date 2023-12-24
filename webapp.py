import pandas as pd
from datetime import datetime
from flask import Flask,request,render_template
import webbrowser
from subprocess import call

app = Flask(__name__)

nowdate = datetime.now()

current_date=nowdate.strftime("%d-%m-%Y")
def extract_attendance():
    df=pd.read_csv(f"{current_date}.csv")
    names = df['Name']
    rolls = df['Roll no']
    times = df['Time']
    l = len(df)
    return names,rolls,times,l
@app.route('/start', methods=['GET'])
def start():
    call(["python", "main.py"])
@app.route('/')
def home():
    names,rolls,times,l = extract_attendance() 
    return render_template('home2.html',names=names,rolls=rolls,times=times,l=l)

webbrowser.open('http://127.0.0.1:5000')
if __name__=="__main__":
    app.run()

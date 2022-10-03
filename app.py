from flask import Flask, flash, redirect, session, url_for, render_template, request
from datetime import date
import datetime, notifications 
 
app = Flask(__name__)
app.secret_key = "1234"
 
today = date.today()
today = today.strftime("%Y-%m-%d")
 
 
@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'GET':        
        return render_template('index.html')
    if request.method == 'POST':
        location = request.form['key_form']
        notifications.notify(location)
        return render_template('index.html', location=location)
 
 
if __name__ == "__main__":
    app.run(debug=True)

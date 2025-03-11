#Working on this page
from flask import Flask,render_template,request,session,jsonify,redirect
import numpy as np,pandas as pd,pickle
from datetime import date
import datetime

model = pickle.load(open('AdaBoost.pkl','rb'))
CountryCodes = pickle.load(open('Country_Codes.pkl','rb'))
dataSet = pickle.load(open('Customer_dataset.pkl','rb'))
DataScaler = pickle.load(open('scaler.pkl','rb'))

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

countries = [
    'United Kingdom', 'France', 'Australia', 'Netherlands', 'Germany',
    'Norway', 'EIRE', 'Switzerland', 'Spain', 'Poland', 'Portugal',
    'Italy', 'Belgium', 'Lithuania', 'Japan', 'Iceland',
    'Channel Islands', 'Denmark', 'Cyprus', 'Sweden', 'Austria',
    'Israel', 'Finland', 'Greece', 'Singapore', 'Lebanon',
    'United Arab Emirates', 'Saudi Arabia', 'Czech Republic', 'Canada',
    'Unspecified', 'Brazil', 'USA', 'European Community', 'Bahrain',
    'Malta', 'RSA'
]

@app.route('/')
def start():
    return render_template('landing_page.html')

@app.route('/input')
def get_input():
    return render_template('input_form.html',countries=countries)

@app.route('/login')
def login():
    return render_template('login.html')

USERS = {
    "admin": "password123",
    "user1": "securepass",
    "prashu": "rfmproject"
}

@app.route('/check_details', methods=['POST'])
def check_details():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in USERS and USERS[username] == password:
        session["user"] = username  # Store session
        return jsonify({"success": True, "message": "Login successful!"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password."})


@app.route('/user_in')
def logged_in():
    return render_template('user_logged_in.html')

@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/submit',methods=['POST'])
def submit():
    customerId = float(request.form.get('customer_id'))
    country = request.form.get('country')
    country_code = CountryCodes[country]
    monetary_str = request.form.get('transaction_amount', '0').strip()
    monetary = ''.join(filter(str.isdigit, monetary_str))
    monetary = float(monetary)
    last_visit = request.form.get('last_visit') 
    last_visit = datetime.datetime.strptime(last_visit, "%Y-%m-%d").date()
    frequency = float(request.form.get('total_visits'))
    recency = (date.today() - last_visit).days


    arr = np.array([recency,frequency,monetary,country_code])
    arr = arr.reshape(1,-1)
    arr = DataScaler.transform(arr)
    cluster_id = model.predict(arr)

    if(cluster_id == 0):
        return render_template('cluster0.html')
    if(cluster_id == 1):
        return render_template('cluster1.html')
    if(cluster_id == 2):
        return render_template('cluster2.html')
    if(cluster_id == 3):
        return render_template('cluster3.html')

if(__name__ == '__main__'):
    app.run(debug=True)

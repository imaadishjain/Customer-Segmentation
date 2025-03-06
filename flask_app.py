from flask import Flask,render_template,request,session,jsonify,redirect

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

if(__name__ == '__main__'):
    app.run(debug=True)
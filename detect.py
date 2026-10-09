from flask import Flask, request, jsonify, send_file
import subprocess
import os
import sys

app = Flask(__name__)

@app.route('/')
def home():
    # Serve the login page
    return send_file('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == 'mpm' and password == '12345':
        # Launch detect.py after successful login
        detect_script = os.path.join(os.path.dirname(__file__), 'detect.py')
        if os.path.exists(detect_script):
            subprocess.Popen([sys.executable, detect_script])
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/detect')
def detect_page():
    return "<h2>Kidney Stone Detection window will open separately.</h2>"

if __name__ == '__main__':
    app.run(debug=True)

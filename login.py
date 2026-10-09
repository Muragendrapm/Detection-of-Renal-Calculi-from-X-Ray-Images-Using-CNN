from flask import Flask, request, jsonify, render_template_string
import subprocess
import os
import sys

app = Flask(__name__)

LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Login Page</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #74ebd5, #9face6);
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .login-box {
      background: #fff;
      padding: 40px;
      border-radius: 15px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
      text-align: center;
      width: 300px;
    }
    h2 {
      margin-bottom: 20px;
      color: #333;
    }
    input {
      width: 100%;
      padding: 10px;
      margin: 10px 0;
      border: 1px solid #ccc;
      border-radius: 5px;
      font-size: 16px;
    }
    button {
      width: 100%;
      padding: 10px;
      background-color: #5a67d8;
      color: #fff;
      border: none;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
    }
    button:hover {
      background-color: #434190;
    }
    .error {
      color: red;
      margin-top: 10px;
    }
  </style>
</head>
<body>
  <div class="login-box">
    <h2>Kidney Stone Detection System</h2>
    <input type="text" id="username" placeholder="Username" />
    <input type="password" id="password" placeholder="Password" />
    <button onclick="login()">Login</button>
    <p class="error" id="errorMsg"></p>
    <p style="margin-top: 20px; font-size: 12px; color: #666;">
      Default credentials: username: mpm, password: 12345
    </p>
  </div>

  <script>
    async function login() {
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      const errorMsg = document.getElementById("errorMsg");

      const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const result = await response.json();
      if (result.success) {
        alert("Login successful! Opening detection window...");
        window.location.href = "/detect";
      } else {
        errorMsg.textContent = "Invalid username or password";
      }
    }
  </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(LOGIN_HTML)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == 'mpm' and password == '12345':
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/detect')
def detect_page():
    # Launch the Tkinter detection window
    try:
        subprocess.Popen([sys.executable, 'detect_left_backup.py'])
        return "<h2>Kidney Stone Detection window is opening...</h2><p>Please check for the detection window on your desktop.</p>"
    except Exception as e:
        return f"<h2>Error launching detection window: {str(e)}</h2>"

if __name__ == '__main__':
    print("Starting Kidney Stone Detection System...")
    print("Open your browser and go to: http://localhost:5000")
    print("Default login - Username: mpm, Password: 12345")
    app.run(debug=True, host='0.0.0.0', port=5000)

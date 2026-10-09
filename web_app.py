from flask import Flask, request, jsonify, render_template_string, send_file
import numpy as np
from PIL import Image, ImageTk, ImageDraw
from tensorflow.keras.models import load_model
import io
import base64
import os

app = Flask(__name__)

# Load the pre-trained model
try:
    model = load_model('model.h5')
    print("Model loaded successfully!")
except:
    try:
        model = load_model('../model.h5')
        print("Model loaded from parent directory!")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None

# Define target image size
image_height, image_width = 224, 224

def preprocess_image(image_file):
    """Preprocess uploaded image for prediction"""
    image = Image.open(image_file)
    image = image.resize((image_height, image_width))
    image = np.array(image)
    image = image.astype('float32') / 255.0
    return image

LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kidney Stone Detection System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #74ebd5, #9face6);
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }
        .header {
            background: #5a67d8;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .content {
            padding: 30px;
        }
        .login-box {
            max-width: 400px;
            margin: 0 auto;
            text-align: center;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #5a67d8;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            margin: 10px 0;
        }
        button:hover {
            background-color: #434190;
        }
        .error {
            color: red;
            margin-top: 10px;
        }
        .info {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #2196f3;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 Kidney Stone Detection System</h1>
            <p>AI-Powered Medical Image Analysis</p>
        </div>
        <div class="content">
            <div class="login-box">
                <h2>Login to Access Detection System</h2>
                <div class="info">
                    <strong>Default Credentials:</strong><br>
                    Username: <code>mpm</code><br>
                    Password: <code>12345</code>
                </div>
                <input type="text" id="username" placeholder="Enter username" value="mpm">
                <input type="password" id="password" placeholder="Enter password" value="12345">
                <button onclick="login()">🔐 Login</button>
                <p class="error" id="errorMsg"></p>
            </div>
        </div>
    </div>

    <script>
        async function login() {
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const errorMsg = document.getElementById("errorMsg");

            try {
                const response = await fetch("/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password }),
                });

                const result = await response.json();
                if (result.success) {
                    window.location.href = "/detect";
                } else {
                    errorMsg.textContent = "❌ Invalid username or password";
                }
            } catch (error) {
                errorMsg.textContent = "❌ Connection error. Please try again.";
            }
        }
        
        // Allow Enter key to submit
        document.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                login();
            }
        });
    </script>
</body>
</html>
'''

DETECT_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kidney Stone Detection</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #74ebd5, #9face6);
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }
        .header {
            background: #5a67d8;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .content {
            padding: 30px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        .upload-section {
            text-align: center;
        }
        .file-input {
            display: none;
        }
        .upload-btn {
            display: inline-block;
            padding: 15px 30px;
            background: #4CAF50;
            color: white;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 20px 0;
        }
        .upload-btn:hover {
            background: #45a049;
        }
        .image-preview {
            max-width: 100%;
            max-height: 400px;
            border: 2px dashed #ccc;
            border-radius: 10px;
            margin: 20px 0;
        }
        .result-section {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
        }
        .result {
            font-size: 18px;
            font-weight: bold;
            margin: 10px 0;
            padding: 15px;
            border-radius: 5px;
        }
        .positive {
            background: #ffebee;
            color: #c62828;
            border-left: 4px solid #f44336;
        }
        .negative {
            background: #e8f5e8;
            color: #2e7d32;
            border-left: 4px solid #4caf50;
        }
        .info-box {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #2196f3;
        }
        .prevention-tips {
            background: #fff3e0;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #ff9800;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        @media (max-width: 768px) {
            .content {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 Kidney Stone Detection</h1>
            <p>Upload an X-ray image for AI analysis</p>
        </div>
        <div class="content">
            <div class="upload-section">
                <h2>📤 Upload X-ray Image</h2>
                <div class="info-box">
                    <strong>Instructions:</strong><br>
                    • Upload a clear X-ray image<br>
                    • Supported formats: JPG, PNG, JPEG<br>
                    • Maximum file size: 10MB
                </div>
                
                <input type="file" id="imageInput" class="file-input" accept="image/*" onchange="previewImage()">
                <label for="imageInput" class="upload-btn">
                    📁 Choose X-ray Image
                </label>
                
                <div id="imagePreview">
                    <img id="previewImg" class="image-preview" style="display: none;">
                </div>
                
                <button onclick="analyzeImage()" id="analyzeBtn" style="display: none;" class="upload-btn">
                    🔍 Analyze Image
                </button>
                
                <div class="loading" id="loading">
                    <p>🔄 Analyzing image... Please wait.</p>
                </div>
            </div>
            
            <div class="result-section">
                <h2>📊 Analysis Results</h2>
                <div id="results">
                    <p>Upload an image to see analysis results.</p>
                </div>
                
                <div class="prevention-tips">
                    <h3>🛡️ Prevention Tips for Kidney Stones:</h3>
                    <ul>
                        <li><strong>Stay Hydrated:</strong> Drink plenty of water (8-10 glasses daily)</li>
                        <li><strong>Balanced Diet:</strong> Limit salt, animal protein, and oxalate-rich foods</li>
                        <li><strong>Healthy Weight:</strong> Maintain optimal body weight</li>
                        <li><strong>Limit Sugar:</strong> Reduce sugar and soda consumption</li>
                        <li><strong>Regular Exercise:</strong> Stay physically active</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <script>
        function previewImage() {
            const input = document.getElementById('imageInput');
            const preview = document.getElementById('previewImg');
            const analyzeBtn = document.getElementById('analyzeBtn');
            
            if (input.files && input.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                    analyzeBtn.style.display = 'inline-block';
                };
                reader.readAsDataURL(input.files[0]);
            }
        }
        
        async function analyzeImage() {
            const input = document.getElementById('imageInput');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const analyzeBtn = document.getElementById('analyzeBtn');
            
            if (!input.files || !input.files[0]) {
                alert('Please select an image first!');
                return;
            }
            
            const formData = new FormData();
            formData.append('image', input.files[0]);
            
            loading.style.display = 'block';
            analyzeBtn.style.display = 'none';
            results.innerHTML = '<p>Analyzing...</p>';
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    const isStone = result.prediction === 'Stone';
                    const confidence = (result.confidence * 100).toFixed(1);
                    
                    results.innerHTML = `
                        <div class="result ${isStone ? 'positive' : 'negative'}">
                            ${isStone ? '⚠️' : '✅'} ${result.prediction}
                        </div>
                        <p><strong>Confidence:</strong> ${confidence}%</p>
                        <div class="info-box">
                            <strong>Note:</strong> This is an AI analysis for reference only. 
                            Please consult with a medical professional for proper diagnosis and treatment.
                        </div>
                    `;
                } else {
                    results.innerHTML = `<p style="color: red;">❌ Error: ${result.error}</p>`;
                }
            } catch (error) {
                results.innerHTML = `<p style="color: red;">❌ Connection error: ${error.message}</p>`;
            } finally {
                loading.style.display = 'none';
                analyzeBtn.style.display = 'inline-block';
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
    return render_template_string(DETECT_HTML)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return jsonify({'success': False, 'error': 'Model not loaded'})
        
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image uploaded'})
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No image selected'})
        
        # Preprocess the image
        image = preprocess_image(file)
        image = np.expand_dims(image, axis=0)
        
        # Make prediction
        predictions = model.predict(image)[0]
        
        # Assuming the model has classes: [Normal, Stone, Cyst, Tumor]
        class_names = ['Normal', 'Stone', 'Cyst', 'Tumor']
        predicted_class_idx = np.argmax(predictions)
        predicted_class = class_names[predicted_class_idx]
        confidence = float(predictions[predicted_class_idx])
        
        return jsonify({
            'success': True,
            'prediction': predicted_class,
            'confidence': confidence,
            'all_predictions': {
                class_names[i]: float(predictions[i]) for i in range(len(class_names))
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("=" * 60)
    print("    KIDNEY STONE DETECTION WEB APPLICATION")
    print("=" * 60)
    print("🚀 Starting Flask web server...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("🔐 Default login credentials:")
    print("   Username: mpm")
    print("   Password: 12345")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
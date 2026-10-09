# Detection of Renal Calculi from X-Ray Images using CNN

This folder contains the project source code, the saved CNN model, sample images, and screenshots.

## Recommended way to run the web application (Windows)

1. Install **Python 3.10 or 3.11 (64-bit)**. During installation, select **Add Python to PATH**.
2. Extract this ZIP file completely to a normal folder. Keep `model.h5` in the same folder as `web_app.py`.
3. Open Command Prompt in the extracted folder.
4. Create and activate a virtual environment:

   ```bat
   py -3.10 -m venv .venv
   .venv\Scripts\activate
   ```

   If Python 3.10 is not installed but Python 3.11 is, use `py -3.11` instead.

5. Install dependencies:

   ```bat
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Start the web application:

   ```bat
   python web_app.py
   ```

   Or double-click `run_web.bat` after installing dependencies.

7. Open this address in your browser: **http://127.0.0.1:5000**

## Login

Use the credentials shown on the login screen. In the current source the default credentials are:

- Username: `mpm`
- Password: `12345`

## Included files

- `web_app.py` — primary Flask web application matching the browser-based interface.
- `login.py` — alternate login launcher for the desktop detection window.
- `detect_left_backup.py` — Tkinter desktop interface.
- `detect.py` — small Flask launcher/route example.
- `detection_model.py` — training script; requires a local `dataset` folder.
- `run_project.py` — menu-based launcher.
- `model.h5` — saved CNN model used for prediction.
- `sample_images/` — supplied sample images.
- `screenshots/` — screenshots of the application.

## Training the model (optional)

The supplied `detection_model.py` expects a `dataset` directory containing one subfolder per class with training images. The class folders and their order must match the model's expected output labels. The dataset itself is not included in this ZIP because it was not among the supplied project files. Do not run the training script unless you have prepared that folder.

## Important notes

- The included code files pass Python syntax compilation, but a successful prediction run depends on installing compatible libraries and having a compatible TensorFlow/Keras environment.
- Keep `model.h5` in the project root. It is large and must be included when sharing the application.
- The prediction is for academic demonstration only and is not a medical diagnosis. The confidence value is the model's output score and should not be interpreted as clinical certainty.
- Before sharing publicly, consider replacing the displayed default login credentials and reviewing the code for production security.

import os
import secrets
import logging
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_required, logout_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
import pickle
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize SQLAlchemy
db = SQLAlchemy()

# Create Flask app
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get("SESSION_SECRET", secrets.token_hex(16))
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure database options
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load the model once
import os as _os
MODEL_PATH = 'crop.pkl'
model = None
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    if _os.environ.get("WERKZEUG_RUN_MAIN") == "true" or _os.environ.get("WERKZEUG_RUN_MAIN") is None:
        logger.info("Model loaded successfully")
except FileNotFoundError:
    logger.error(f"Model file {MODEL_PATH} not found. Please ensure it exists.")
    model = None

# Configure login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return db.session.get(User, int(user_id))

import models

with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from crop_descriptions import CROP_DESCRIPTIONS

@app.route('/')
def home():
    return render_template('index.html')

from crop_descriptions import CROP_DESCRIPTIONS

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        flash("Model is not loaded. Prediction is unavailable.", "danger")
        return redirect(url_for('home'))
    try:
        features = ['nitrogen', 'phosphorous', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall']
        input_data = {}
        input_values = []
        for feature in features:
            value = request.form.get(feature)
            if not value:
                flash(f"Missing value for {feature}", "danger")
                return redirect(url_for('home'))
            # Allow negative temperature input explicitly
            if feature == 'temperature':
                try:
                    temp_val = float(value)
                    input_data[feature] = value
                    input_values.append(temp_val)
                    if temp_val < 0:
                        flash("Note: Negative temperature input detected. Crop recommendation will proceed.", "info")
                except ValueError:
                    flash(f"Invalid temperature value: {value}", "danger")
                    return redirect(url_for('home'))
            else:
                input_data[feature] = value
                input_values.append(float(value))
        input_array = np.array(input_values).reshape(1, -1)
        prediction = model.predict(input_array)[0]
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_array)[0]
            classes = model.classes_
            top_crops = sorted(zip(classes, proba), key=lambda x: x[1], reverse=True)
        else:
            top_crops = [(prediction, 1.0)]
        crop_info = CROP_DESCRIPTIONS.get(prediction.lower(), {
            "description": f"Description for {prediction} is not available.",
            "ideal_conditions": "Ideal growing conditions are not specified.",
            "growing_period": "Growing period information is not available."
        })
        crop_data = {
            'name': prediction,
            'image_url': None,
            'description': crop_info["description"],
            'ideal_conditions': crop_info["ideal_conditions"],
            'growing_period': crop_info["growing_period"]
        }
        return render_template('prediction.html', crop_data=crop_data, top_crops=top_crops, input_data=input_data)
    except Exception as e:
        flash(f"Error during prediction: {str(e)}", "danger")
        return redirect(url_for('home'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part in the request', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:
                df = pd.read_csv(filepath)
                required_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
                if not all(col in df.columns for col in required_columns):
                    flash('CSV file missing required columns', 'danger')
                    return redirect(request.url)
                features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
                X = df[features]
                predictions = model.predict(X)
                df['predicted_crop'] = predictions
                crop_counts = df['predicted_crop'].value_counts()
                crop_counts_dict = crop_counts.to_dict()
                result_filename = f"analysis_results_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
                result_filepath = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
                df.to_csv(result_filepath, index=False)
                summary = {
                    'total_samples': len(df),
                    'unique_crops': df['predicted_crop'].nunique(),
                    'result_filename': result_filename,
                    'crop_distribution': crop_counts_dict
                }
                return render_template('analysis.html', tables=[df.to_html(classes='table table-striped')], summary=summary, filename=filename)
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'danger')
                return redirect(request.url)
        else:
            flash('Invalid file type. Only CSV files are allowed.', 'danger')
            return redirect(request.url)
    return render_template('upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Placeholder login logic
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    from models import User
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            flash('Please fill out all fields.', 'danger')
            return render_template('register.html')
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please choose another.', 'danger')
            return render_template('register.html')
        password_hash = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you for contacting us! We will get back to you shortly.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

import traceback

@app.route('/chart')
def chart():
    try:
        labels = ["Nitrogen", "Phosphorous", "Potassium", "Temperature", "Humidity", "pH", "Rainfall"]
        data = [50, 40, 30, 20, 10, 60, 70]  # Sample data for the chart
        return render_template('chart.html', labels=labels, data=data)
    except Exception as e:
        logger.error(f"Error rendering chart page: {e}")
        logger.error(traceback.format_exc())
        from flask import abort
        abort(500, description="Internal Server Error while rendering chart page")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

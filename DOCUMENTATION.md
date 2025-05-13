# Crop Recommendation System Documentation

## 1. Project Overview
The Crop Recommendation System is a web application designed to recommend suitable crops based on soil and environmental parameters. It leverages machine learning to predict the best crop for given soil conditions. The system includes user authentication, data upload and analysis, and visualization features.

## 2. Backend

### app.py
- Initializes the Flask application with configuration and database setup.
- Loads a pre-trained Random Forest model (`crop.pkl`) for crop prediction.
- Defines routes for:
  - Home page (`/`)
  - Crop prediction (`/predict`)
  - Dataset upload and analysis (`/upload`)
  - User authentication: login (`/login`), logout (`/logout`), register (`/register`)
  - Contact page (`/contact`)
  - Download analysis results (`/download/<filename>`)
  - Chart visualization (`/chart`)
- Handles file uploads, CSV processing, and prediction on batch data.
- Manages user sessions and authentication using Flask-Login.

### crop_model.py
- Contains the function `train_crop_model()` to train a Random Forest classifier on the Crop Recommendation dataset.
- Saves the trained model as `crop.pkl`.
- This script can be run independently to retrain the model if needed.

### models.py
- Defines database models using SQLAlchemy:
  - `User`: Stores user information including username, email, password hash, and creation timestamp.
  - `SoilRecord`: Stores soil parameters, predicted crop, timestamp, and links to the user who submitted the data.

### config.py
- Contains configuration settings for the application.
- Defines the SQLAlchemy database URI for connecting to a PostgreSQL database.
- Disables SQLALCHEMY_TRACK_MODIFICATIONS for performance.

## 3. Frontend

### Templates
- `layout.html`: Main layout template with navigation bar, flash messages, content block, and footer.
- Other templates include pages for index, login, register, upload, prediction results, analysis, contact, chart, and more.
- Uses Bootstrap for styling and responsiveness.
- Includes Font Awesome icons and Chart.js for data visualization.

### Static Assets
- `styles.css`: Custom CSS styles complementing Bootstrap.
- `script.js`: JavaScript for UI interactions and tooltips.
- Images and icons stored in `static/images`.

## 4. Database Schema
- PostgreSQL database with two main tables:
  - `User`: User credentials and metadata.
  - `SoilRecord`: Soil data inputs and predicted crop results linked to users.

## 5. Machine Learning Model
- Random Forest Classifier trained on soil and environmental features.
- Features used: nitrogen, phosphorous, potassium, temperature, humidity, pH, rainfall.
- Model saved as `crop.pkl` and loaded by the Flask app for predictions.
- Supports single predictions via form input and batch predictions via CSV upload.

## 6. Folder Structure Explanation
- `app.py`: Main application file.
- `config.py`: Configuration settings.
- `crop_model.py`: Model training script.
- `models.py`: Database models.
- `dataset/`: Contains the Crop Recommendation CSV dataset.
- `static/`: CSS, JS, and image assets.
- `templates/`: HTML templates for the website.
- `uploads/`: Uploaded CSV files and analysis results.
- `crop.pkl`: Serialized machine learning model.

## 7. How to Run and Use the Project
1. Ensure PostgreSQL is installed and running.
2. Update database URI in `config.py` if needed.
3. Install dependencies from `requirements.txt`.
4. Run `crop_model.py` to train the model if `crop.pkl` is not present.
5. Start the Flask app using `python app.py` or `python main.py`.
6. Access the website at `http://localhost:5000`.
7. Use the web interface to input soil data, upload datasets, register/login, and view predictions.

## 8. Dependencies and Environment Setup
- Python 3.x
- Flask
- Flask-Login
- Flask-SQLAlchemy
- scikit-learn
- pandas
- numpy
- psycopg2 (PostgreSQL adapter)
- Werkzeug
- Bootstrap (via CDN)
- Font Awesome (via CDN)
- Chart.js (via CDN)

---

This documentation provides a comprehensive overview of the Crop Recommendation System project, its components, and usage instructions.

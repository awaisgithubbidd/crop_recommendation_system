import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

def train_crop_model():
    """
    Train a crop recommendation model and save it as a pickle file.
    Note: This function is provided to regenerate the model if needed.
    """
    # Check if model already exists
    if os.path.exists('crop.pkl'):
        print("Model already exists. Skipping training.")
        return
    
    try:
        # Load dataset (assumed to be in the project directory)
        # Replace with actual dataset path if different
        df = pd.read_csv('dataset/Crop_recommendation.csv')
        
        # Features and target
        X = df.drop('label', axis=1)
        y = df['label']
        
        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train Random Forest model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate model
        accuracy = model.score(X_test, y_test)
        print(f"Model accuracy: {accuracy:.4f}")
        
        # Save the model
        with open('crop.pkl', 'wb') as f:
            pickle.dump(model, f)
        
        print("Model saved successfully as 'crop.pkl'")
        
    except Exception as e:
        print(f"Error training model: {str(e)}")

if __name__ == "__main__":
    train_crop_model()
# config.py
import os

class Config:
     SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1122@localhost:5432/crop_recommendation_system'
os.environ['DATABASE_URL'] = 'postgresql://postgres:1122@localhost:5432/crop_recommendation_system'

SQLALCHEMY_TRACK_MODIFICATIONS = False
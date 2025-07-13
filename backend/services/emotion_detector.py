import librosa
import numpy as np
import joblib
import os

MODEL_PATH = "models/emotion_model.pkl"
_model = None

def load_model():
    global _model
    if _model is None and os.path.exists(MODEL_PATH):
        _model = joblib.load(MODEL_PATH)
    return _model

def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    return np.mean(mfccs.T, axis=0)

def detect_emotion(file_path):
    model = load_model()
    if model is None:
        return "unknown"
    features = extract_features(file_path).reshape(1, -1)
    prediction = model.predict(features)
    return prediction[0]

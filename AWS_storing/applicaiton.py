## Backend for the project....
from fastapi import FastAPI,UploadFile,File
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from config.data_paths import MODEL_SAVE_PATH
import librosa
import matplotlib.pyplot as plt
import sys

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Music genre classificaiton app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load the model
if os.path.exists(MODEL_SAVE_PATH):
    try:
        model = load_model(MODEL_SAVE_PATH)
        print(f"Model loaded successfully from {MODEL_SAVE_PATH}")
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)
else:
    print(f"Model file not found at {MODEL_SAVE_PATH}")
    sys.exit(1)

CLASS_NAMES = ['blues','classical','country','disco','hiphop','jazz','metal','pop','reggae','rock']

@app.get("/")
def home():
    return {"Status":"Music classification API is running successfully.."}

@app.get("/status")
def status():
    if model:
        return {"Status":"Model loaded successfully...."}
    else:
        return {"Status":"Model didnt loaded...!"}
    
@app.post("/predict")
async def predict_image(file:UploadFile=File(...)):
    try:

        '''Save upload file temperary'''
        temp_audio_path = "temp_audio.au"
        
        with open(temp_audio_path,'wb') as f:
            f.write(await file.read())
        
        # load and preprocess audio

        y,sr = librosa.load(temp_audio_path,sr=None)
        S = librosa.feature.melspectrogram(y=y,sr=sr,n_mels=128)
        S_db = librosa.power_to_db(S,ref=np.max)
        
        # Prepare input for the CNN
        #-resize/pad in to 128

        disired_size = (128,128)
        S_db = librosa.util.fix_length(S_db, size=disired_size[1], axis=1)
        S_db = S_db[:disired_size[0], :]

        # Normalize
        S_db = (S_db - S_db.min()) / (S_db.max() - S_db.min())
        # Reshape for CNN: (1, 128, 128, 1)
        input_data = np.expand_dims(S_db, axis=(0, -1))   # (1,128,128,1)
        input_data = np.repeat(input_data, 3, axis=-1)    # (1,128,128,3)

        # ---- Step 3: Predict ----
        preds = model.predict(input_data)
        class_idx = np.argmax(preds, axis=1)[0]
        confidence = float(np.max(preds))
        label = CLASS_NAMES[class_idx] if class_idx < len(CLASS_NAMES) else str(class_idx)

        os.remove(temp_audio_path)  # cleanup

        return {
                "predicted_class": label,
                "confidence": round(confidence, 4)
            }
    except Exception as e:
        os.remove(temp_audio_path)
        return {"error": str(e)}
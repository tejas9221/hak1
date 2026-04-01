from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = FastAPI()

# CORS (important)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = tf.keras.applications.MobileNetV2(weights="imagenet")

classes = ["Healthy", "Leaf Spot", "Rust", "Blight"]

@app.post("/predict")
async def predict(
    image: UploadFile = File(...),
    text: str = Form("")
):
    contents = await image.read()
    img = Image.open(io.BytesIO(contents)).resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    preds = model.predict(img)[0]

    result = {
        "disease": classes[np.argmax(preds) % 4],
        "confidence": float(np.max(preds)),
        "graph": preds[:4].tolist(),
        "tips": "Use organic fertilizer and proper irrigation"
    }

    return result

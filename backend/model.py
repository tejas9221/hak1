import tensorflow as tf
import numpy as np
from PIL import Image

# 🌿 Class labels (you can expand later)
CLASSES = [
    "Healthy",
    "Leaf Spot",
    "Rust",
    "Blight"
]

# 📦 Load trained model
def load_model():
    try:
        model = tf.keras.models.load_model("crop_model.h5")
        print("✅ Custom model loaded")
    except:
        print("⚠️ Using pretrained MobileNetV2")
        model = tf.keras.applications.MobileNetV2(weights="imagenet")
    return model

model = load_model()

# 🧠 Image preprocessing
def preprocess_image(image_bytes):
    img = Image.open(image_bytes).convert("RGB")
    img = img.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# 🔍 Prediction function
def predict_disease(image_bytes, symptoms_text=""):
    img = preprocess_image(image_bytes)

    preds = model.predict(img)[0]

    # Convert predictions to our classes
    graph = preds[:len(CLASSES)]
    class_index = int(np.argmax(graph))

    disease = CLASSES[class_index]
    confidence = float(np.max(graph))

    # 💡 Smart tips (basic logic)
    tips = generate_tips(disease, symptoms_text)

    return {
        "disease": disease,
        "confidence": confidence,
        "graph": graph.tolist(),
        "tips": tips
    }

# 🌱 Tips generator (hackathon feature)
def generate_tips(disease, text):
    text = text.lower()

    if "yellow" in text:
        return "Possible nutrient deficiency. Add nitrogen fertilizer."

    if disease == "Leaf Spot":
        return "Use fungicide and avoid overwatering."

    elif disease == "Rust":
        return "Remove infected leaves and apply sulfur spray."

    elif disease == "Blight":
        return "Ensure proper drainage and crop rotation."

    else:
        return "Crop looks healthy. Maintain irrigation and sunlight."

import random

diseases = ["Eczema", "Psoriasis", "Acne", "Fungal Infection"]

def predict_disease(image_path):
    disease = random.choice(diseases)
    confidence = round(random.uniform(60, 95), 2)
    return disease, confidence

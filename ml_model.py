"""
AI/ML Model Module

This module contains the AI prediction functionality for skin disease detection.
For the prototype, it uses random predictions to simulate an AI model.

In a production environment, this would be replaced with:
- A trained deep learning model (CNN, etc.)
- TensorFlow/PyTorch model
- Or an external API call to a medical AI service

This is a prototype demonstration only.
"""

import random

# Skin conditions that the AI can detect
# In a real implementation, this would come from a trained model
DISEASES = [
    "Eczema",
    "Psoriasis", 
    "Acne",
    "Fungal Infection",
    "Dermatitis",
    "Rosacea",
    "Vitiligo",
    "Skin Cancer (Benign)",
    "Hives",
    "Contact Dermatitis"
]

# Severity levels for each disease (for demonstration)
DISEASE_INFO = {
    "Eczema": {
        "severity": "Medium",
        "description": "Inflammatory skin condition causing itchy, red, swollen skin"
    },
    "Psoriasis": {
        "severity": "Medium-High",
        "description": "Autoimmune condition causing rapid skin cell growth"
    },
    "Acne": {
        "severity": "Low-Medium",
        "description": "Common skin condition when hair follicles get clogged with oil"
    },
    "Fungal Infection": {
        "severity": "Low",
        "description": "Infection caused by fungus affecting skin, nails, or hair"
    },
    "Dermatitis": {
        "severity": "Low-Medium",
        "description": "General term for skin inflammation"
    },
    "Rosacea": {
        "severity": "Low-Medium",
        "description": "Chronic skin condition causing facial redness"
    },
    "Vitiligo": {
        "severity": "Low",
        "description": "Loss of skin pigment in patches"
    },
    "Skin Cancer (Benign)": {
        "severity": "Medium-High",
        "description": "Abnormal growth of skin cells (non-malignant)"
    },
    "Hives": {
        "severity": "Low",
        "description": "Skin reaction causing itchy welts"
    },
    "Contact Dermatitis": {
        "severity": "Low-Medium",
        "description": "Skin reaction from contact with irritants or allergens"
    }
}

def predict_disease(image_path):
    """
    Analyze an image and predict potential skin condition.
    
    In this prototype:
    - Returns a random disease from the DISEASES list
    - Generates a random confidence score between 60-95%
    
    Args:
        image_path (str): Path to the uploaded image file
    
    Returns:
        tuple: (disease_name: str, confidence: float)
    
    Note:
        This is a simulation for demonstration purposes only.
        Real medical diagnosis should always be performed by qualified healthcare professionals.
    """
    
    # Randomly select a disease
    disease = random.choice(DISEASES)
    
    # Generate random confidence between 60% and 95%
    confidence = round(random.uniform(60, 95), 2)
    
    return disease, confidence

def get_disease_info(disease_name):
    """
    Get information about a specific disease.
    
    Args:
        disease_name (str): Name of the disease
    
    Returns:
        dict: Disease information including severity and description
    """
    return DISEASE_INFO.get(disease_name, {
        "severity": "Unknown",
        "description": "No information available"
    })

def get_all_diseases():
    """
    Get list of all supported diseases.
    
    Returns:
        list: List of disease names
    """
    return DISEASES

def get_confidence_level(confidence):
    """
    Get a human-readable confidence level.
    
    Args:
        confidence (float): Confidence percentage
    
    Returns:
        str: Confidence level (High, Medium, Low)
    """
    if confidence >= 85:
        return "High"
    elif confidence >= 70:
        return "Medium"
    else:
        return "Low"


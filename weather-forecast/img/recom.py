import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
import requests
from io import BytesIO
import time

# Page config
st.set_page_config(page_title="🌱 Smart Crop Recommendation System", layout="wide", page_icon="🌾")

# Custom CSS with larger fonts and background
st.markdown("""
<style>
    /* Main Theme Colors */
    :root {
        --primary-green: #2E7D32;
        --secondary-green: #4CAF50;
        --light-green: #A5D6A7;
        --dark-green: #1B5E20;
        --accent-gold: #FFB300;
        --soil-brown: #8D6E63;
        --water-blue: #2196F3;
        --sun-yellow: #FFEB3B;
    }

    /* Background Image */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.95)),
                    url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80');
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        min-height: 100vh;
    }

    /* Header Styling with LARGER FONTS */
    .main-header {
        background: linear-gradient(135deg, rgba(46, 125, 50, 0.95), rgba(76, 175, 80, 0.95));
        color: white;
        padding: 3.5rem 2rem;
        border-radius: 25px;
        margin-bottom: 2.5rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(46, 125, 50, 0.4);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    .main-title {
        font-size: 4.2rem !important;
        font-weight: 900 !important;
        margin-bottom: 0.8rem !important;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.4);
        letter-spacing: 0.5px;
    }
    .main-subtitle {
        font-size: 1.8rem !important;
        opacity: 0.95;
        max-width: 1000px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* Card Styling with LARGER FONTS */
    .metric-card {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 25px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
        border: 2px solid rgba(46, 125, 50, 0.3);
        transition: all 0.4s ease;
    }
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(46, 125, 50, 0.25);
    }

    /* Input Container with LARGER FONTS */
    .input-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        padding: 3rem;
        margin: 2.5rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        border: 3px solid rgba(46, 125, 50, 0.2);
        backdrop-filter: blur(5px);
    }
    
    .input-title {
        font-size: 2.2rem !important;
        color: var(--primary-green) !important;
        margin-bottom: 2rem !important;
        font-weight: 800 !important;
        text-align: center;
    }

    /* Section Titles with LARGER FONTS */
    .section-title {
        font-size: 2rem !important;
        color: var(--primary-green) !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
    }

    /* Button Styling with LARGER FONTS */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-green), var(--secondary-green));
        color: white;
        border: none;
        padding: 1.2rem 3.5rem;
        border-radius: 50px;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
        transition: all 0.4s ease;
        box-shadow: 0 8px 20px rgba(46, 125, 50, 0.4);
        letter-spacing: 0.5px;
    }
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 30px rgba(46, 125, 50, 0.5);
        background: linear-gradient(135deg, var(--secondary-green), var(--primary-green));
    }

    /* Result Cards with LARGER FONTS */
    .result-card {
        background: linear-gradient(135deg, rgba(232, 245, 232, 0.98), rgba(200, 230, 201, 0.98));
        border-radius: 25px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(46, 125, 50, 0.25);
        border-left: 8px solid var(--primary-green);
        animation: slideIn 0.6s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Crop Badge with LARGER FONTS */
    .crop-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--accent-gold), #FFCA28);
        color: var(--dark-green);
        padding: 1.2rem 2.5rem;
        border-radius: 50px;
        font-weight: 900 !important;
        font-size: 1.8rem !important;
        box-shadow: 0 8px 20px rgba(255, 179, 0, 0.4);
        margin: 1rem;
        border: 3px solid white;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Nutrient Indicators */
    .nutrient-bar {
        height: 25px;
        border-radius: 12px;
        margin: 10px 0;
        transition: all 0.5s ease;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .nutrient-low { background: linear-gradient(90deg, #FFCDD2, #EF5350); }
    .nutrient-medium { background: linear-gradient(90deg, #FFF3E0, #FFA726); }
    .nutrient-high { background: linear-gradient(90deg, #C8E6C9, #4CAF50); }
    .nutrient-very-high { background: linear-gradient(90deg, #81C784, #2E7D32); }

    /* Crop Image Cards */
    .crop-image-card {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        background: white;
        margin: 1rem;
    }
    .crop-image-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    /* Labels with LARGER FONTS */
    label {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        color: var(--dark-green) !important;
        margin-bottom: 0.8rem !important;
    }
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        font-size: 1.3rem !important;
        padding: 1rem !important;
        border-radius: 12px !important;
        border: 2px solid var(--light-green) !important;
    }
    
    /* Metric values */
    .metric-value {
        font-size: 3rem !important;
        font-weight: 900 !important;
        color: var(--primary-green) !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        font-size: 1.2rem !important;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, rgba(46, 125, 50, 0.95), rgba(27, 94, 32, 0.95));
        color: white;
        padding: 2.5rem;
        border-radius: 25px;
        text-align: center;
        margin-top: 3rem;
        box-shadow: 0 10px 30px rgba(46, 125, 50, 0.3);
    }
    
    .footer h3 {
        font-size: 2.2rem !important;
        margin-bottom: 1rem !important;
    }
    
    .footer p {
        font-size: 1.4rem !important;
        opacity: 0.9;
        margin-bottom: 0.5rem !important;
    }
    
    /* Image loading animation */
    .image-loading {
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
</style>
""", unsafe_allow_html=True)

# Enhanced crop images dictionary with reliable Unsplash URLs
CROP_IMAGES = {
    'rice': 'https://images.unsplash.com/photo-1628644211106-32f4d3dcc8c0?w=600&auto=format&fit=crop',
    'maize': 'https://images.unsplash.com/photo-1621531848016-d1d39e6bcb8e?w=600&auto=format&fit=crop',
    'wheat': 'https://images.unsplash.com/photo-1622495805595-4b1f5c9c5c8d?w=600&auto=format&fit=crop',
    'cotton': 'https://images.unsplash.com/photo-1563217259-6df3e4c0c7a0?w=600&auto=format&fit=crop',
    'sugarcane': 'https://images.unsplash.com/photo-1623771121234-0c2c5c0c0c0c?w=600&auto=format&fit=crop',
    'jute': 'https://images.unsplash.com/photo-1592921870789-7b5c9c0b0b0b?w=600&auto=format&fit=crop',
    'coffee': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600&auto=format&fit=crop',
    'mungbean': 'https://images.unsplash.com/photo-1592921870789-7b5c9c0b0b0b?w=600&auto=format&fit=crop',
    'kidneybeans': 'https://images.unsplash.com/photo-1592921870789-7b5c9c0b0b0b?w=600&auto=format&fit=crop',
    'chickpea': 'https://images.unsplash.com/photo-1592921870789-7b5c9c0b0b0b?w=600&auto=format&fit=crop',
    'pomegranate': 'https://images.unsplash.com/photo-1556656793-08538906a9f8?w=600&auto=format&fit=crop',
    'lentil': 'https://images.unsplash.com/photo-1592921870789-7b5c9c0b0b0b?w=600&auto=format&fit=crop',
    'apple': 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=600&auto=format&fit=crop',
    'banana': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=600&auto=format&fit=crop',
    'grapes': 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=600&auto=format&fit=crop',
    'orange': 'https://images.unsplash.com/photo-1557800636-894a64c1696f?w=600&auto=format&fit=crop',
    'papaya': 'https://images.unsplash.com/photo-1557800636-894a64c1696f?w=600&auto=format&fit=crop',
    'coconut': 'https://images.unsplash.com/photo-1557800636-894a64c1696f?w=600&auto=format&fit=crop',
    'watermelon': 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=600&auto=format&fit=crop',
    'mango': 'https://images.unsplash.com/photo-1557800636-894a64c1696f?w=600&auto=format&fit=crop',
    'pineapple': 'https://images.unsplash.com/photo-1557800636-894a64c1696f?w=600&auto=format&fit=crop',
    'cucumber': 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=600&auto=format&fit=crop',
    'tomato': 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=600&auto=format&fit=crop',
    'potato': 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=600&auto=format&fit=crop',
    'onion': 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=600&auto=format&fit=crop',
    'default': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=600&auto=format&fit=crop'
}

# Function to get nutrient status
def get_nutrient_status(value, nutrient_type):
    """Determine nutrient status with different thresholds for different nutrients"""
    thresholds = {
        'N': {'low': 30, 'medium': 60, 'high': 100},
        'P': {'low': 20, 'medium': 40, 'high': 80},
        'K': {'low': 40, 'medium': 80, 'high': 120},
        'calcium': {'low': 200, 'medium': 400, 'high': 600},
        'magnesium': {'low': 50, 'medium': 100, 'high': 150},
        'sulfur': {'low': 10, 'medium': 20, 'high': 40},
        'zinc': {'low': 0.5, 'medium': 1.0, 'high': 2.0},
        'iron': {'low': 2.0, 'medium': 5.0, 'high': 10.0},
        'copper': {'low': 0.2, 'medium': 0.5, 'high': 1.0},
        'manganese': {'low': 1.0, 'medium': 2.0, 'high': 4.0},
        'boron': {'low': 0.2, 'medium': 0.5, 'high': 1.0},
        'molybdenum': {'low': 0.01, 'medium': 0.05, 'high': 0.1}
    }
    
    if nutrient_type in thresholds:
        thresh = thresholds[nutrient_type]
        if value < thresh['low']:
            return 'Low', 'nutrient-low'
        elif value < thresh['medium']:
            return 'Medium', 'nutrient-medium'
        elif value < thresh['high']:
            return 'High', 'nutrient-high'
        else:
            return 'Very High', 'nutrient-very-high'
    return 'Optimal', 'nutrient-medium'

# Function to get crop image with error handling
def get_crop_image(crop_name):
    """Get crop image URL from dictionary with fallback"""
    crop_lower = crop_name.lower().strip()
    
    # Try exact match first
    if crop_lower in CROP_IMAGES:
        return CROP_IMAGES[crop_lower]
    
    # Try partial match
    for key in CROP_IMAGES:
        if key in crop_lower or crop_lower in key:
            return CROP_IMAGES[key]
    
    # Return default image
    return CROP_IMAGES['default']

# Function to check if image URL is accessible
def is_image_accessible(url):
    """Check if an image URL is accessible"""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except:
        return False

# Create enhanced dataset with MORE soil parameters
np.random.seed(42)
n_samples = 500  # Increased samples for better training

# Enhanced soil parameters
data = {
    # Primary Nutrients
    'N': np.random.uniform(0, 200, n_samples).round(1),
    'P': np.random.uniform(0, 150, n_samples).round(1),
    'K': np.random.uniform(0, 250, n_samples).round(1),
    
    # Secondary Nutrients
    'calcium': np.random.uniform(100, 800, n_samples).round(1),
    'magnesium': np.random.uniform(20, 200, n_samples).round(1),
    'sulfur': np.random.uniform(5, 60, n_samples).round(1),
    
    # Micronutrients
    'zinc': np.random.uniform(0.1, 3.0, n_samples).round(2),
    'iron': np.random.uniform(1.0, 15.0, n_samples).round(2),
    'copper': np.random.uniform(0.1, 1.5, n_samples).round(2),
    'manganese': np.random.uniform(0.5, 5.0, n_samples).round(2),
    'boron': np.random.uniform(0.1, 1.2, n_samples).round(2),
    'molybdenum': np.random.uniform(0.01, 0.15, n_samples).round(3),
    
    # Climate Parameters
    'temperature': np.random.uniform(10, 45, n_samples).round(1),
    'humidity': np.random.uniform(20, 95, n_samples).round(1),
    'ph': np.random.uniform(4.5, 8.5, n_samples).round(2),
    'rainfall': np.random.uniform(100, 400, n_samples).round(1),
    'sunlight': np.random.uniform(4, 12, n_samples).round(1),  # hours per day
    'altitude': np.random.uniform(0, 2000, n_samples).round(0),
    
    # Soil Properties
    'organic_matter': np.random.uniform(0.5, 5.0, n_samples).round(2),  # percentage
    'soil_texture': np.random.choice(['Sandy', 'Loamy', 'Clay', 'Silty'], n_samples),
    'drainage': np.random.choice(['Poor', 'Moderate', 'Good', 'Excellent'], n_samples),
}

df = pd.DataFrame(data)

# Improved crop assignment function
def assign_crop(row):
    n, p, k = row['N'], row['P'], row['K']
    temp = row['temperature']
    rainfall = row['rainfall']
    ph = row['ph']
    sunlight = row['sunlight']
    altitude = row['altitude']
    soil_type = row['soil_texture']
    drainage = row['drainage']
    humidity = row['humidity']
    
    # Score-based system for more variety
    crop_scores = {}
    
    # Rice scoring
    rice_score = 0
    if rainfall > 200: rice_score += 2
    if 20 <= temp <= 35: rice_score += 2
    if 5.5 <= ph <= 7.5: rice_score += 1
    if soil_type in ['Clay', 'Loamy']: rice_score += 1
    if drainage in ['Poor', 'Moderate']: rice_score += 1  # Rice likes water retention
    crop_scores['rice'] = rice_score
    
    # Wheat scoring
    wheat_score = 0
    if 10 <= temp <= 25: wheat_score += 2
    if 150 <= rainfall <= 350: wheat_score += 2
    if 6.0 <= ph <= 7.5: wheat_score += 1
    if soil_type == 'Loamy': wheat_score += 1
    crop_scores['wheat'] = wheat_score
    
    # Maize scoring
    maize_score = 0
    if temp > 18: maize_score += 2
    if sunlight > 8: maize_score += 2
    if n > 80: maize_score += 1
    if 5.5 <= ph <= 7.5: maize_score += 1
    crop_scores['maize'] = maize_score
    
    # Cotton scoring
    cotton_score = 0
    if temp > 25: cotton_score += 2
    if rainfall < 300: cotton_score += 1
    if ph > 6.0: cotton_score += 1
    if soil_type in ['Sandy', 'Loamy']: cotton_score += 1
    crop_scores['cotton'] = cotton_score
    
    # Sugarcane scoring
    sugarcane_score = 0
    if temp > 20: sugarcane_score += 2
    if rainfall > 250: sugarcane_score += 2
    if sunlight > 9: sugarcane_score += 1
    if soil_type == 'Loamy': sugarcane_score += 1
    crop_scores['sugarcane'] = sugarcane_score
    
    # Fruits scoring
    fruit_scores = {}
    
    # Tropical fruits (low altitude)
    if altitude < 500 and temp > 20 and ph > 6.0:
        fruit_scores['banana'] = 2
        fruit_scores['papaya'] = 2
        fruit_scores['pineapple'] = 2
        if rainfall > 200: fruit_scores['coconut'] = 3
    
    # Subtropical fruits (medium altitude)
    if 500 <= altitude < 1500 and 15 <= temp <= 30 and ph > 6.0:
        fruit_scores['orange'] = 2
        fruit_scores['mango'] = 2
        fruit_scores['grapes'] = 2
    
    # Temperate fruits (high altitude)
    if altitude >= 1500 and 10 <= temp <= 25:
        fruit_scores['apple'] = 3
        fruit_scores['pomegranate'] = 2
    
    # Vegetables scoring
    if soil_type == 'Loamy' and 15 <= temp <= 30:
        veg_scores = {
            'tomato': 2 + (p > 40),
            'potato': 2 + (k > 100),
            'cucumber': 2 + (humidity > 60),
            'onion': 2 + (sunlight > 7),
            'watermelon': 2 if temp > 25 and drainage == 'Good' else 0
        }
        # Add only vegetables with positive scores
        for veg, score in veg_scores.items():
            if score > 0:
                crop_scores[veg] = score
    
    # Legumes scoring (they fix nitrogen, prefer lower N)
    if n < 100 and p > 20:
        legume_bonus = 2 if n < 60 else 1
        legumes = ['mungbean', 'chickpea', 'kidneybeans', 'lentil']
        for legume in legumes:
            crop_scores[legume] = legume_bonus
    
    # Coffee scoring
    coffee_score = 0
    if altitude > 800: coffee_score += 2
    if ph < 6.5: coffee_score += 2
    if 15 <= temp <= 25: coffee_score += 1
    if rainfall > 150: coffee_score += 1
    crop_scores['coffee'] = coffee_score
    
    # Jute scoring
    jute_score = 0
    if rainfall > 300: jute_score += 2
    if temp > 25: jute_score += 2
    if humidity > 70: jute_score += 1
    crop_scores['jute'] = jute_score
    
    # Add fruit scores
    crop_scores.update(fruit_scores)
    
    # Remove crops with 0 score and select highest
    valid_crops = {crop: score for crop, score in crop_scores.items() if score > 0}
    
    if valid_crops:
        # Add some randomness to selection, but prefer higher scores
        scores = list(valid_crops.values())
        crops = list(valid_crops.keys())
        max_score = max(scores)
        
        # Get all crops with max score
        top_crops = [crop for crop, score in valid_crops.items() if score == max_score]
        
        # Randomly select from top crops
        return np.random.choice(top_crops)
    else:
        # Fallback based on primary nutrients
        if n > p and n > k and temp > 20:
            return 'cotton' if rainfall < 250 else 'maize'
        elif p > n and p > k:
            return 'potato' if temp < 25 else 'tomato'
        elif k > n and k > p:
            return 'banana' if temp > 20 else 'apple'
        else:
            return np.random.choice(['wheat', 'maize', 'rice'])

df['label'] = df.apply(assign_crop, axis=1)

# Train model with all features
feature_cols = ['N', 'P', 'K', 'calcium', 'magnesium', 'sulfur', 'zinc', 'iron', 
                'copper', 'manganese', 'boron', 'molybdenum', 'temperature', 
                'humidity', 'ph', 'rainfall', 'sunlight', 'altitude', 'organic_matter']

# Convert categorical to numerical
df['soil_texture_num'] = df['soil_texture'].map({'Sandy': 0, 'Silty': 1, 'Loamy': 2, 'Clay': 3})
df['drainage_num'] = df['drainage'].map({'Poor': 0, 'Moderate': 1, 'Good': 2, 'Excellent': 3})

feature_cols.extend(['soil_texture_num', 'drainage_num'])

X = df[feature_cols]
y = df['label']

model = RandomForestClassifier(
    n_estimators=300, 
    random_state=42, 
    max_depth=12,
    min_samples_split=5,
    min_samples_leaf=2
)
model.fit(X, y)

# Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🌱 ADVANCED CROP RECOMMENDATION SYSTEM</h1>
    <p class="main-subtitle">AI-Powered recommendations for 25+ crops based on 20+ soil & climate parameters</p>
    <p style="font-size: 1.6rem; margin-top: 1rem; opacity: 0.9;">
        ⚡ Real-time nutrient analysis • 🌡️ Climate adaptation • 📊 Multi-parameter optimization
    </p>
</div>
""", unsafe_allow_html=True)

# Input section
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.markdown('<h1 class="input-title">📊 SOIL & CLIMATE DATA INPUT</h1>', unsafe_allow_html=True)

# Create tabs for different parameter categories
tab1, tab2, tab3, tab4 = st.tabs(["🌿 PRIMARY NUTRIENTS", "⚡ SECONDARY NUTRIENTS", "🔬 MICRONUTRIENTS", "🌡️ CLIMATE & SOIL"])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<h2 class="section-title">Nitrogen (N)</h2>', unsafe_allow_html=True)
        N = st.slider("**NITROGEN (kg/ha)**", 0.0, 200.0, 80.0, 1.0, 
                     help="Essential for leaf growth and green color")
    with col2:
        st.markdown('<h2 class="section-title">Phosphorus (P)</h2>', unsafe_allow_html=True)
        P = st.slider("**PHOSPHORUS (kg/ha)**", 0.0, 150.0, 45.0, 1.0,
                     help="Essential for root development and flowering")
    with col3:
        st.markdown('<h2 class="section-title">Potassium (K)</h2>', unsafe_allow_html=True)
        K = st.slider("**POTASSIUM (kg/ha)**", 0.0, 250.0, 120.0, 1.0,
                     help="Essential for fruit quality and disease resistance")

with tab2:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<h2 class="section-title">Calcium (Ca)</h2>', unsafe_allow_html=True)
        calcium = st.slider("**CALCIUM (mg/kg)**", 100.0, 800.0, 350.0, 10.0,
                          help="Important for cell wall structure")
    with col2:
        st.markdown('<h2 class="section-title">Magnesium (Mg)</h2>', unsafe_allow_html=True)
        magnesium = st.slider("**MAGNESIUM (mg/kg)**", 20.0, 200.0, 80.0, 5.0,
                            help="Central component of chlorophyll")
    with col3:
        st.markdown('<h2 class="section-title">Sulfur (S)</h2>', unsafe_allow_html=True)
        sulfur = st.slider("**SULFUR (mg/kg)**", 5.0, 60.0, 25.0, 1.0,
                         help="Essential for protein synthesis")

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h2 class="section-title">Zinc (Zn)</h2>', unsafe_allow_html=True)
        zinc = st.slider("**ZINC (mg/kg)**", 0.1, 3.0, 1.2, 0.1,
                       help="Essential for enzyme systems")
        st.markdown('<h2 class="section-title" style="margin-top: 2rem;">Iron (Fe)</h2>', unsafe_allow_html=True)
        iron = st.slider("**IRON (mg/kg)**", 1.0, 15.0, 6.0, 0.5,
                       help="Essential for chlorophyll formation")
        st.markdown('<h2 class="section-title" style="margin-top: 2rem;">Copper (Cu)</h2>', unsafe_allow_html=True)
        copper = st.slider("**COPPER (mg/kg)**", 0.1, 1.5, 0.8, 0.1,
                         help="Important for reproductive growth")
    with col2:
        st.markdown('<h2 class="section-title">Manganese (Mn)</h2>', unsafe_allow_html=True)
        manganese = st.slider("**MANGANESE (mg/kg)**", 0.5, 5.0, 2.5, 0.1,
                            help="Activates enzyme systems")
        st.markdown('<h2 class="section-title" style="margin-top: 2rem;">Boron (B)</h2>', unsafe_allow_html=True)
        boron = st.slider("**BORON (mg/kg)**", 0.1, 1.2, 0.6, 0.1,
                        help="Essential for cell division")
        st.markdown('<h2 class="section-title" style="margin-top: 2rem;">Molybdenum (Mo)</h2>', unsafe_allow_html=True)
        molybdenum = st.slider("**MOLYBDENUM (mg/kg)**", 0.01, 0.15, 0.06, 0.01,
                             help="Essential for nitrogen fixation")

with tab4:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<h2 class="section-title">Climate</h2>', unsafe_allow_html=True)
        temp = st.slider("**TEMPERATURE (°C)**", 10.0, 45.0, 25.0, 0.5,
                       help="Average daily temperature")
        humidity = st.slider("**HUMIDITY (%)**", 20.0, 95.0, 65.0, 1.0,
                           help="Relative humidity")
        rainfall = st.slider("**RAINFALL (mm)**", 100.0, 400.0, 250.0, 10.0,
                           help="Annual rainfall")
    with col2:
        st.markdown('<h2 class="section-title">Soil Properties</h2>', unsafe_allow_html=True)
        ph = st.slider("**SOIL pH**", 4.5, 8.5, 6.5, 0.1,
                      help="Soil acidity/alkalinity (4.5-6.5 acidic, 6.5-7.5 neutral, 7.5+ alkaline)")
        sunlight = st.slider("**SUNLIGHT (hours/day)**", 4.0, 12.0, 8.0, 0.5,
                           help="Daily sunlight hours")
        altitude = st.slider("**ALTITUDE (meters)**", 0.0, 2000.0, 300.0, 50.0,
                           help="Elevation above sea level")
    with col3:
        st.markdown('<h2 class="section-title">More Properties</h2>', unsafe_allow_html=True)
        organic_matter = st.slider("**ORGANIC MATTER (%)**", 0.5, 5.0, 2.5, 0.1,
                                 help="Soil organic matter content")
        soil_texture = st.selectbox("**SOIL TEXTURE**", ["Sandy", "Silty", "Loamy", "Clay"],
                                  help="Soil particle size distribution")
        drainage = st.selectbox("**DRAINAGE**", ["Poor", "Moderate", "Good", "Excellent"],
                              help="Soil water drainage capacity")

st.markdown('</div>', unsafe_allow_html=True)

# Recommendation button
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    analyze_clicked = st.button("🚀 **ANALYZE & RECOMMEND CROPS**", type="primary", use_container_width=True)

if analyze_clicked:
    # Convert categorical to numerical for model input
    soil_texture_num = {"Sandy": 0, "Silty": 1, "Loamy": 2, "Clay": 3}[soil_texture]
    drainage_num = {"Poor": 0, "Moderate": 1, "Good": 2, "Excellent": 3}[drainage]
    
    # Prepare input data
    input_data = np.array([[
        N, P, K, calcium, magnesium, sulfur, zinc, iron, copper,
        manganese, boron, molybdenum, temp, humidity, ph, rainfall,
        sunlight, altitude, organic_matter, soil_texture_num, drainage_num
    ]])
    
    # Get predictions
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    
    # Top 10 recommendations
    prob_df = pd.DataFrame({
        'Crop': model.classes_,
        'Probability': probabilities
    }).sort_values('Probability', ascending=False).head(10)
    
    # Display results
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    # Top recommendation with image
    col_top1, col_top2 = st.columns([2, 1])
    with col_top1:
        st.markdown(f"""
        <div style='text-align: center;'>
            <h1 style='color: var(--primary-green); margin-bottom: 1.5rem; font-size: 2.8rem;'>🎯 BEST RECOMMENDATION</h1>
            <div class="crop-badge">{prediction.title()}</div>
            <p style='font-size: 1.8rem; color: var(--dark-green); margin-top: 1.5rem;'>
                Confidence: <strong style='font-size: 2.2rem;'>{prob_df[prob_df["Crop"] == prediction]["Probability"].iloc[0]:.1%}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_top2:
        try:
            crop_image_url = get_crop_image(prediction)
            # Fixed: Container with fixed dimensions
            st.markdown(f"""
            <div style='text-align: center;'>
                <div id='crop-image-container' class='image-loading'>
                    <div style='width: 250px; height: 250px; margin: 0 auto; overflow: hidden; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2);'>
                        <img src='{crop_image_url}' 
                             style='width: 100%; height: 100%; object-fit: cover;'
                             onload="this.parentElement.parentElement.classList.remove('image-loading')"
                             onerror="this.src='{CROP_IMAGES['default']}'; this.parentElement.parentElement.classList.remove('image-loading')">
                    </div>
                </div>
                <p style='font-size: 1.3rem; margin-top: 1rem; color: var(--dark-green); font-weight: 600;'>
                    {prediction.title()}
                </p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")
            # Show default image
            st.image(CROP_IMAGES['default'], width=250, caption=prediction.title())
    
    # Nutrient Analysis Visualization
    st.markdown("---")
    st.markdown('<h1 class="section-title" style="text-align: center;">🔬 SOIL NUTRIENT ANALYSIS</h1>', unsafe_allow_html=True)
    
    # Primary Nutrients
    col_n1, col_n2, col_n3 = st.columns(3)
    with col_n1:
        status, css_class = get_nutrient_status(N, 'N')
        st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
            <h3 style='color: var(--primary-green); margin-bottom: 1rem;'>🌿 NITROGEN</h3>
            <div style='font-size: 2.5rem; font-weight: 800; color: var(--primary-green);'>{N} kg/ha</div>
            <div class='nutrient-bar {css_class}' style='width: 100%;'></div>
            <div style='font-size: 1.2rem; margin-top: 0.5rem; color: #666;'>{status} Level</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_n2:
        status, css_class = get_nutrient_status(P, 'P')
        st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
            <h3 style='color: var(--primary-green); margin-bottom: 1rem;'>⚡ PHOSPHORUS</h3>
            <div style='font-size: 2.5rem; font-weight: 800; color: var(--primary-green);'>{P} kg/ha</div>
            <div class='nutrient-bar {css_class}' style='width: 100%;'></div>
            <div style='font-size: 1.2rem; margin-top: 0.5rem; color: #666;'>{status} Level</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_n3:
        status, css_class = get_nutrient_status(K, 'K')
        st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
            <h3 style='color: var(--primary-green); margin-bottom: 1rem;'>💎 POTASSIUM</h3>
            <div style='font-size: 2.5rem; font-weight: 800; color: var(--primary-green);'>{K} kg/ha</div>
            <div class='nutrient-bar {css_class}' style='width: 100%;'></div>
            <div style='font-size: 1.2rem; margin-top: 0.5rem; color: #666;'>{status} Level</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Multiple crop recommendations table
    st.markdown("---")
    st.markdown('<h1 class="section-title" style="text-align: center;">📋 TOP 10 SUITABLE CROPS</h1>', unsafe_allow_html=True)
    
    # Display crops with images
    cols = st.columns(5)
    for idx, (_, row) in enumerate(prob_df.head(10).iterrows()):
        with cols[idx % 5]:
            try:
                crop_img = get_crop_image(row['Crop'])
                st.markdown(f"""
                <div class='crop-image-card'>
                    <div style='width: 100%; height: 180px; overflow: hidden;'>
                        <div class='image-loading' style='width: 100%; height: 100%;'>
                            <img src='{crop_img}' 
                                 style='width: 100%; height: 100%; object-fit: cover;'
                                 onload="this.parentElement.classList.remove('image-loading')"
                                 onerror="this.src='{CROP_IMAGES['default']}'; this.parentElement.classList.remove('image-loading')">
                        </div>
                    </div>
                    <div style='padding: 1rem; text-align: center;'>
                        <div style='font-size: 1.3rem; font-weight: 700; color: var(--dark-green);'>
                            {row['Crop'].title()}
                        </div>
                        <div style='font-size: 1.1rem; color: var(--primary-green); margin-top: 0.5rem;'>
                            {row['Probability']:.1%}
                        </div>
                        <div style='height: 8px; background: #E0E0E0; border-radius: 4px; margin-top: 0.5rem;'>
                            <div style='width: {row['Probability']*100}%; height: 100%; background: linear-gradient(90deg, #4CAF50, #2E7D32); border-radius: 4px;'></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                # Show default image if error occurs
                st.markdown(f"""
                <div class='crop-image-card'>
                    <div style='width: 100%; height: 180px; overflow: hidden;'>
                        <img src='{CROP_IMAGES["default"]}' style='width: 100%; height: 100%; object-fit: cover;'>
                    </div>
                    <div style='padding: 1rem; text-align: center;'>
                        <div style='font-size: 1.3rem; font-weight: 700; color: var(--dark-green);'>
                            {row['Crop'].title()}
                        </div>
                        <div style='font-size: 1.1rem; color: var(--primary-green); margin-top: 0.5rem;'>
                            {row['Probability']:.1%}
                        </div>
                        <div style='height: 8px; background: #E0E0E0; border-radius: 4px; margin-top: 0.5rem;'>
                            <div style='width: {row['Probability']*100}%; height: 100%; background: linear-gradient(90deg, #4CAF50, #2E7D32); border-radius: 4px;'></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Interactive chart
    fig = px.bar(prob_df, x='Probability', y='Crop', 
                 orientation='h', title="📈 CROP SUITABILITY SCORES",
                 color='Probability', color_continuous_scale='RdYlGn',
                 text='Probability')
    fig.update_traces(texttemplate='%{text:.1%}', textposition='outside')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=16),
        title_font_size=24,
        height=500,
        xaxis_title="Suitability Score",
        yaxis_title="Crop"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Comprehensive Metrics
    st.markdown("---")
    st.markdown('<h1 class="section-title" style="text-align: center;">📊 COMPREHENSIVE ANALYSIS</h1>', unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("🌾 **Best Match**", f"{prob_df['Probability'].iloc[0]:.1%}")
    with col_m2:
        st.metric("✅ **Good Options**", f"{len(prob_df[prob_df['Probability'] >= 0.05])} crops")
    with col_m3:
        temp_status = "Optimal" if 20 <= temp <= 30 else "Adjust" if temp < 15 or temp > 35 else "Good"
        temp_delta_color = "normal" if temp_status == "Optimal" else "inverse" if temp_status == "Adjust" else "off"
        st.metric("🌡️ **Temperature**", f"{temp:.1f}°C", 
                 delta=temp_status, delta_color=temp_delta_color)
    with col_m4:
        rain_status = "Adequate" if rainfall > 150 else "Low"
        rain_delta_color = "normal" if rain_status == "Adequate" else "inverse"
        st.metric("💧 **Rainfall**", f"{rainfall:.0f} mm", 
                 delta=rain_status, delta_color=rain_delta_color)
    
    col_m5, col_m6, col_m7, col_m8 = st.columns(4)
    with col_m5:
        ph_status = "Optimal" if 6.0 <= ph <= 7.5 else "Adjust" if ph < 5.5 or ph > 8.0 else "Acceptable"
        ph_delta_color = "normal" if ph_status == "Optimal" else "inverse" if ph_status == "Adjust" else "off"
        st.metric("⚗️ **Soil pH**", f"{ph:.1f}", 
                 delta=ph_status, delta_color=ph_delta_color)
    with col_m6:
        sun_status = "Excellent" if sunlight > 8 else "Good" if sunlight > 6 else "Low"
        sun_delta_color = "normal" if sun_status == "Excellent" else "off" if sun_status == "Good" else "inverse"
        st.metric("🌞 **Sunlight**", f"{sunlight:.1f} hrs", 
                 delta=sun_status, delta_color=sun_delta_color)
    with col_m7:
        alt_status = "High" if altitude > 1000 else "Medium" if altitude > 500 else "Low"
        st.metric("🏔️ **Altitude**", f"{altitude:.0f} m", 
                 delta=alt_status)
    with col_m8:
        om_status = "Rich" if organic_matter > 3.0 else "Medium" if organic_matter > 1.5 else "Poor"
        om_delta_color = "normal" if om_status == "Rich" else "off" if om_status == "Medium" else "inverse"
        st.metric("🌱 **Organic Matter**", f"{organic_matter:.1f}%", 
                 delta=om_status, delta_color=om_delta_color)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <h3>🌍 PRECISION AGRICULTURE 4.0</h3>
    <p style='margin-bottom: 0.5rem;'>
        <span style='font-size: 1.6rem;'>25+ Crops • 20+ Parameters • 500+ Training Samples</span>
    </p>
    <p>
        <span style='font-size: 1.4rem;'>Random Forest (300 trees) • Real-time Analysis • Climate-Adaptive</span>
    </p>
    <p style='margin-top: 1.5rem; font-size: 1.3rem; opacity: 0.8;'>
        💡 Tip: Adjust sliders to see how different conditions affect crop recommendations
    </p>
</div>
""", unsafe_allow_html=True)

# Add JavaScript for interactive effects
st.markdown("""
<script>
// Interactive slider effects
const sliders = document.querySelectorAll('input[type="range"]');
sliders.forEach(slider => {
    const value = ((slider.value - slider.min) / (slider.max - slider.min)) * 100;
    slider.style.background = `linear-gradient(90deg, #4CAF50 ${value}%, #E0E0E0 ${value}%)`;
    
    slider.addEventListener('input', function() {
        const value = ((this.value - this.min) / (this.max - this.min)) * 100;
        this.style.background = `linear-gradient(90deg, #4CAF50 ${value}%, #E0E0E0 ${value}%)`;
    });
});

// Add glow effect to cards on hover
const cards = document.querySelectorAll('.metric-card, .result-card, .input-container, .crop-image-card');
cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.boxShadow = '0 20px 40px rgba(46, 125, 50, 0.3)';
    });
    card.addEventListener('mouseleave', function() {
        this.style.boxShadow = '';
    });
});

// Image error handling
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            this.src = 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80';
            this.onerror = null; // Prevent infinite loop
        });
    });
});
</script>
""", unsafe_allow_html=True)
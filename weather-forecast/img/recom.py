import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import random
import warnings
import plotly.express as px
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Smart Crop Advisor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with modern design
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
    }
    
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    /* Input Section */
    .input-section {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
    
    /* Prediction Cards */
    .prediction-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        border-left: 6px solid #4CAF50;
        margin: 1.5rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        transition: transform 0.3s ease;
    }
    
    .prediction-card:hover {
        transform: translateY(-5px);
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: #4CAF50;
        box-shadow: 0 5px 15px rgba(76, 175, 80, 0.1);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #4CAF50 0%, #2E8B57 100%);
        color: white;
        font-weight: bold;
        border: none;
        width: 100%;
        padding: 12px 24px;
        border-radius: 12px;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
    }
    
    /* Input boxes */
    .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 10px;
        transition: all 0.3s ease;
    }
    
    .stNumberInput>div>div>input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
    }
    
    /* Metrics */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 3px 15px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.12);
    }
    
    /* Crop Cards */
    .crop-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 10px;
        box-shadow: 0 3px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .crop-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        border-color: #4CAF50;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Generate synthetic dataset
@st.cache_data
def generate_crop_data(n_samples=1000):
    """Generate synthetic crop recommendation dataset"""
    # Set random seeds for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Define crop characteristics based on real agricultural knowledge
    crop_profiles = {
        'Rice': {
            'temp_range': (20, 35), 'humidity_range': (70, 95), 'rainfall_range': (150, 300),
            'ph_range': (5.0, 7.5), 'N_range': (60, 120), 'P_range': (30, 60), 'K_range': (40, 80),
            'emoji': '🍚', 'color': '#4CAF50'
        },
        'Wheat': {
            'temp_range': (10, 25), 'humidity_range': (50, 80), 'rainfall_range': (50, 100),
            'ph_range': (6.0, 7.5), 'N_range': (50, 100), 'P_range': (40, 70), 'K_range': (30, 60),
            'emoji': '🌾', 'color': '#FFC107'
        },
        'Maize': {
            'temp_range': (18, 32), 'humidity_range': (60, 85), 'rainfall_range': (60, 120),
            'ph_range': (5.8, 7.4), 'N_range': (80, 140), 'P_range': (40, 80), 'K_range': (50, 90),
            'emoji': '🌽', 'color': '#FF9800'
        },
        'Cotton': {
            'temp_range': (20, 35), 'humidity_range': (60, 85), 'rainfall_range': (50, 120),
            'ph_range': (5.5, 8.5), 'N_range': (40, 80), 'P_range': (30, 60), 'K_range': (40, 80),
            'emoji': '🧵', 'color': '#2196F3'
        },
        'Sugarcane': {
            'temp_range': (20, 35), 'humidity_range': (65, 90), 'rainfall_range': (100, 200),
            'ph_range': (6.0, 8.0), 'N_range': (100, 180), 'P_range': (50, 90), 'K_range': (80, 150),
            'emoji': '🎋', 'color': '#9C27B0'
        },
        'Coffee': {
            'temp_range': (15, 25), 'humidity_range': (70, 90), 'rainfall_range': (150, 250),
            'ph_range': (6.0, 6.5), 'N_range': (60, 100), 'P_range': (30, 50), 'K_range': (40, 70),
            'emoji': '☕', 'color': '#795548'
        },
        'Tea': {
            'temp_range': (15, 30), 'humidity_range': (75, 95), 'rainfall_range': (150, 300),
            'ph_range': (4.5, 5.5), 'N_range': (50, 90), 'P_range': (20, 40), 'K_range': (30, 60),
            'emoji': '🍵', 'color': '#009688'
        },
        'Potato': {
            'temp_range': (15, 20), 'humidity_range': (60, 80), 'rainfall_range': (50, 100),
            'ph_range': (5.0, 6.5), 'N_range': (60, 120), 'P_range': (50, 100), 'K_range': (80, 150),
            'emoji': '🥔', 'color': '#FF5722'
        },
        'Tomato': {
            'temp_range': (18, 28), 'humidity_range': (60, 85), 'rainfall_range': (60, 120),
            'ph_range': (6.0, 6.8), 'N_range': (80, 140), 'P_range': (40, 80), 'K_range': (60, 120),
            'emoji': '🍅', 'color': '#F44336'
        },
        'Soybean': {
            'temp_range': (20, 30), 'humidity_range': (60, 80), 'rainfall_range': (60, 110),
            'ph_range': (6.0, 7.0), 'N_range': (40, 80), 'P_range': (30, 60), 'K_range': (40, 80),
            'emoji': '🫘', 'color': '#8BC34A'
        }
    }
    
    data = []
    crops = list(crop_profiles.keys())
    
    for _ in range(n_samples):
        crop = random.choice(crops)
        profile = crop_profiles[crop]
        
        # Generate data with some noise
        row = {
            'N': np.random.randint(profile['N_range'][0], profile['N_range'][1]),
            'P': np.random.randint(profile['P_range'][0], profile['P_range'][1]),
            'K': np.random.randint(profile['K_range'][0], profile['K_range'][1]),
            'temperature': np.random.uniform(profile['temp_range'][0], profile['temp_range'][1]),
            'humidity': np.random.uniform(profile['humidity_range'][0], profile['humidity_range'][1]),
            'ph': np.random.uniform(profile['ph_range'][0], profile['ph_range'][1]),
            'rainfall': np.random.uniform(profile['rainfall_range'][0], profile['rainfall_range'][1]),
            'label': crop
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    return df, crop_profiles

# Train model on generated data
@st.cache_resource
def train_model(df):
    """Train Random Forest model on generated data"""
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        min_samples_split=4,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    
    return model, accuracy, X.columns

# Get crop descriptions
def get_crop_description(crop_name):
    """Return description for each crop"""
    descriptions = {
        'Rice': 'Staple food crop requiring warm temperatures and plenty of water. Best suited for areas with high rainfall.',
        'Wheat': 'Cool season cereal crop. Requires moderate rainfall and fertile soil with good drainage.',
        'Maize': 'Warm season crop that grows quickly. Needs well-drained soil and adequate nitrogen.',
        'Cotton': 'Fiber crop requiring long warm season. Drought tolerant but needs careful pest management.',
        'Sugarcane': 'Tropical perennial grass. Requires abundant water and sunshine for high sugar content.',
        'Coffee': 'Shade-loving tropical crop. Requires specific altitude, rainfall, and temperature conditions.',
        'Tea': 'Evergreen shrub preferring acidic soil, high rainfall, and humid conditions.',
        'Potato': 'Cool season tuber crop. Needs loose, well-drained soil and consistent moisture.',
        'Tomato': 'Warm season vegetable. Requires full sun, consistent watering, and support for growth.',
        'Soybean': 'Legume crop that fixes nitrogen. Adaptable to various soils but sensitive to day length.'
    }
    return descriptions.get(crop_name, 'No description available.')

# Get suitability level
def get_suitability_level(probability):
    """Get suitability level based on probability"""
    if probability >= 0.8:
        return "Excellent", "#4CAF50"
    elif probability >= 0.6:
        return "Good", "#8BC34A"
    elif probability >= 0.4:
        return "Moderate", "#FFC107"
    else:
        return "Fair", "#FF9800"

# Main application
def main():
    # Header
    st.markdown("""
    <div class='main-header fade-in'>
        <h1 style='font-size: 2.8rem; margin-bottom: 1rem;'>🌱 Smart Crop Recommendation System</h1>
        <p style='font-size: 1.2rem; opacity: 0.9;'>AI-powered crop suggestion based on soil and climate parameters</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate data and train model
    with st.spinner("Generating agricultural dataset and training model... 🌱"):
        df, crop_profiles = generate_crop_data(1500)
        model, accuracy, features = train_model(df)
    
    # Display system info
    st.markdown("### 📊 System Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>📈 Model Accuracy</h3>
            <h1 style='color: #4CAF50;'>{accuracy:.1%}</h1>
            <p>Trained on {len(df)} samples</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>🌽 Available Crops</h3>
            <h1 style='color: #2196F3;'>{len(df['label'].unique())}</h1>
            <p>10 different crop types</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>📋 Features Analyzed</h3>
            <h1 style='color: #FF9800;'>{len(features)}</h1>
            <p>Soil + Climate parameters</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Input Section with boxes
    st.markdown("## 🌱 Enter Soil & Climate Details")
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Soil Nutrients (ppm)")
        nitrogen = st.number_input(
            "**Nitrogen (N)**",
            min_value=0,
            max_value=200,
            value=80,
            step=1,
            help="Essential for leaf growth and green color (0-200 ppm)"
        )
        
        phosphorus = st.number_input(
            "**Phosphorus (P)**",
            min_value=0,
            max_value=150,
            value=50,
            step=1,
            help="Important for root development and flowering (0-150 ppm)"
        )
        
        potassium = st.number_input(
            "**Potassium (K)**",
            min_value=0,
            max_value=200,
            value=70,
            step=1,
            help="Essential for overall plant health and disease resistance (0-200 ppm)"
        )
    
    with col2:
        st.markdown("### Climate Conditions")
        temperature = st.number_input(
            "**Temperature (°C)**",
            min_value=0.0,
            max_value=40.0,
            value=25.0,
            step=0.5,
            help="Average daytime temperature (0-40°C)",
            format="%.1f"
        )
        
        humidity = st.number_input(
            "**Humidity (%)**",
            min_value=0,
            max_value=100,
            value=70,
            step=1,
            help="Average relative humidity (0-100%)"
        )
        
        ph = st.number_input(
            "**pH Level**",
            min_value=4.0,
            max_value=9.0,
            value=6.5,
            step=0.1,
            help="Soil acidity/alkalinity (4.0-9.0, 7 is neutral)",
            format="%.1f"
        )
        
        rainfall = st.number_input(
            "**Rainfall (mm/year)**",
            min_value=0,
            max_value=500,
            value=120,
            step=10,
            help="Annual rainfall or irrigation available (0-500 mm)"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Predict button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button("🚜 **Get Crop Recommendations**", use_container_width=True)
    
    if predict_button:
        # Validate inputs
        if any([pd.isna(x) for x in [nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]]):
            st.error("❌ Please fill in all input fields with valid values.")
        else:
            with st.spinner("Analyzing soil and climate conditions... 🔍"):
                # Prepare input
                input_data = np.array([[nitrogen, phosphorus, potassium, 
                                      temperature, humidity, ph, rainfall]])
                
                # Get predictions
                try:
                    prediction = model.predict(input_data)[0]
                    probabilities = model.predict_proba(input_data)[0]
                    
                    # Get top 5 crops
                    top_5_idx = np.argsort(probabilities)[-5:][::-1]
                    top_5_crops = model.classes_[top_5_idx]
                    top_5_probs = probabilities[top_5_idx]
                    
                    # Display top recommendation
                    st.markdown("---")
                    
                    emoji = crop_profiles[prediction].get('emoji', '🌱')
                    color = crop_profiles[prediction].get('color', '#4CAF50')
                    
                    st.markdown(f"""
                    <div class='prediction-card fade-in'>
                        <div style='display: flex; align-items: center; gap: 25px;'>
                            <div style='font-size: 4.5rem;'>{emoji}</div>
                            <div>
                                <h2 style='color: {color}; margin-bottom: 10px;'>🎯 Recommended Crop: {prediction}</h2>
                                <p style='font-size: 1.2rem; margin-bottom: 15px;'>
                                    <strong>Confidence:</strong> <span style='color: {color}; font-weight: bold;'>{top_5_probs[0]:.1%}</span>
                                </p>
                                <p style='font-size: 1.1rem; color: #666; line-height: 1.6;'>
                                    {get_crop_description(prediction)}
                                </p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display top 5 recommendations
                    st.markdown("### 📊 Top 5 Suitable Crops")
                    
                    cols = st.columns(5)
                    for idx, (crop, prob) in enumerate(zip(top_5_crops, top_5_probs)):
                        with cols[idx]:
                            suitability, suit_color = get_suitability_level(prob)
                            crop_emoji = crop_profiles[crop].get('emoji', '🌱')
                            crop_color = crop_profiles[crop].get('color', '#4CAF50')
                            
                            st.markdown(f"""
                            <div class='crop-card' style='border-color: {crop_color};'>
                                <div style='font-size: 2.8rem; margin-bottom: 12px;'>{crop_emoji}</div>
                                <h4 style='color: {crop_color};'>{crop}</h4>
                                <div style='font-size: 1.6rem; font-weight: bold; color: {suit_color}; margin: 12px 0;'>
                                    {prob:.1%}
                                </div>
                                <div style='font-size: 0.9rem; color: #666; padding: 5px 10px; 
                                          background-color: {suit_color}15; border-radius: 20px;'>
                                    {suitability}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Feature importance
                    st.markdown("### 🔬 Feature Importance Analysis")
                    
                    feature_importance = pd.DataFrame({
                        'Feature': features,
                        'Importance': model.feature_importances_
                    }).sort_values('Importance', ascending=True)
                    
                    fig, ax = plt.subplots(figsize=(12, 6))
                    
                    # Create gradient colors
                    importances = feature_importance['Importance'].values
                    colors = plt.cm.viridis((importances - importances.min()) / (importances.max() - importances.min()))
                    
                    bars = ax.barh(feature_importance['Feature'], importances, color=colors)
                    
                    # Add value labels
                    for i, (value, feature) in enumerate(zip(importances, feature_importance['Feature'])):
                        ax.text(value + 0.002, i, f'{value:.3f}', va='center', fontsize=11, fontweight='bold')
                    
                    ax.set_xlabel('Importance Score', fontsize=12, fontweight='bold')
                    ax.set_title('How Each Factor Influences Crop Selection', fontsize=16, fontweight='bold', pad=20)
                    ax.grid(axis='x', alpha=0.2, linestyle='--')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Detailed analysis
                    st.markdown("### 📈 Detailed Analysis")
                    
                    tab1, tab2 = st.tabs(["🎯 Input Summary", "💡 Recommendations"])
                    
                    with tab1:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### Your Input Values")
                            input_summary = pd.DataFrame({
                                'Parameter': ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 
                                            'Humidity', 'pH', 'Rainfall'],
                                'Your Value': [nitrogen, phosphorus, potassium, f"{temperature}°C", 
                                             f"{humidity}%", f"{ph:.1f}", f"{rainfall} mm"],
                                'Unit': ['ppm', 'ppm', 'ppm', '°C', '%', 'pH', 'mm/yr']
                            })
                            
                            # Display as styled table
                            st.dataframe(
                                input_summary,
                                column_config={
                                    "Parameter": st.column_config.TextColumn("Parameter", width="medium"),
                                    "Your Value": st.column_config.TextColumn("Your Value", width="medium"),
                                    "Unit": st.column_config.TextColumn("Unit", width="small")
                                },
                                hide_index=True,
                                use_container_width=True
                            )
                        
                        with col2:
                            st.markdown("#### Optimal Ranges for Top Crop")
                            profile = crop_profiles[prediction]
                            
                            # Create comparison table
                            comparison_data = {
                                'Parameter': ['Temperature', 'Rainfall', 'pH', 'Nitrogen', 'Phosphorus', 'Potassium'],
                                'Your Value': [f"{temperature}°C", f"{rainfall} mm", f"{ph:.1f}", 
                                             f"{nitrogen} ppm", f"{phosphorus} ppm", f"{potassium} ppm"],
                                'Optimal Range': [
                                    f"{profile['temp_range'][0]} - {profile['temp_range'][1]}°C",
                                    f"{profile['rainfall_range'][0]} - {profile['rainfall_range'][1]} mm",
                                    f"{profile['ph_range'][0]} - {profile['ph_range'][1]}",
                                    f"{profile['N_range'][0]} - {profile['N_range'][1]} ppm",
                                    f"{profile['P_range'][0]} - {profile['P_range'][1]} ppm",
                                    f"{profile['K_range'][0]} - {profile['K_range'][1]} ppm"
                                ]
                            }
                            
                            comparison_df = pd.DataFrame(comparison_data)
                            st.dataframe(comparison_df, hide_index=True, use_container_width=True)
                    
                    with tab2:
                        st.markdown("#### 💡 Agricultural Recommendations")
                        
                        recommendations = []
                        
                        # pH recommendations
                        if ph < 5.5:
                            recommendations.append("**Soil is acidic.** Consider adding agricultural lime to raise pH to optimal levels.")
                        elif ph > 7.5:
                            recommendations.append("**Soil is alkaline.** Add sulfur or organic matter (compost, peat moss) to lower pH.")
                        
                        # Temperature recommendations
                        if temperature < 15:
                            recommendations.append("**Low temperature conditions.** Consider cold-tolerant crops or using greenhouses/protected cultivation.")
                        elif temperature > 30:
                            recommendations.append("**High temperature conditions.** Ensure adequate irrigation and consider heat-tolerant crop varieties.")
                        
                        # Rainfall recommendations
                        if rainfall < 50:
                            recommendations.append("**Low rainfall area.** Consider drought-resistant crops or implement irrigation systems.")
                        elif rainfall > 200:
                            recommendations.append("**High rainfall area.** Ensure good drainage systems to prevent waterlogging.")
                        
                        # Nutrient recommendations
                        if nitrogen < 30:
                            recommendations.append("**Low nitrogen levels.** Add nitrogen-rich fertilizers or plant legumes (which fix nitrogen).")
                        if phosphorus < 20:
                            recommendations.append("**Low phosphorus levels.** Apply phosphorus fertilizers to support root development.")
                        if potassium < 30:
                            recommendations.append("**Low potassium levels.** Add potassium fertilizers for better disease resistance.")
                        
                        if not recommendations:
                            recommendations.append("**Good news!** Your soil and climate conditions are generally favorable for agriculture.")
                        
                        # Display recommendations
                        for i, rec in enumerate(recommendations):
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); 
                                      padding: 18px; border-radius: 12px; margin: 12px 0; 
                                      border-left: 5px solid #4CAF50;'>
                                <div style='display: flex; align-items: flex-start; gap: 12px;'>
                                    <div style='font-size: 1.5rem;'>✅</div>
                                    <div>
                                        <p style='margin: 0; font-size: 1.05rem; line-height: 1.5;'>
                                            {rec}
                                        </p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Sustainable farming tips
                        st.markdown("#### 🌍 Sustainable Farming Tips")
                        tips = [
                            "**Crop rotation:** Alternate crops to maintain soil fertility and reduce pest buildup",
                            "**Organic matter:** Add compost regularly to improve soil structure and water retention",
                            "**Water conservation:** Use drip irrigation or mulching to reduce water usage",
                            "**Integrated pest management:** Combine biological, cultural, and chemical methods",
                            "**Soil testing:** Test soil every 2-3 years to adjust nutrient applications"
                        ]
                        
                        for tip in tips:
                            st.markdown(f"• {tip}")
                
                except Exception as e:
                    st.error(f"❌ Error making prediction: {str(e)}")
    
    else:
        # Welcome screen when no prediction is made
        st.markdown("""
        <div style='background: white; padding: 2.5rem; border-radius: 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); 
                  margin-top: 2rem;'>
            <h2 style='color: #2E8B57; margin-bottom: 1.5rem;'>👋 Welcome to Smart Crop Advisor!</h2>
            
            <p style='font-size: 1.15rem; line-height: 1.7; color: #555; margin-bottom: 2rem;'>
            This AI-powered system helps farmers and agricultural experts determine the most suitable crops 
            for specific soil and climate conditions. Using machine learning algorithms trained on realistic 
            agricultural data, we provide intelligent crop recommendations with confidence scores.
            </p>
            
            <h3 style='color: #4CAF50; margin-top: 2rem; margin-bottom: 1rem;'>🎯 How to Use:</h3>
            <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 2rem;'>
                <div class='feature-card'>
                    <h4>1. Enter Parameters</h4>
                    <p>Fill in the soil nutrient levels and climate conditions using the input boxes above.</p>
                </div>
                <div class='feature-card'>
                    <h4>2. Get Recommendations</h4>
                    <p>Click the "Get Crop Recommendations" button to analyze your inputs.</p>
                </div>
                <div class='feature-card'>
                    <h4>3. Review Results</h4>
                    <p>View detailed crop suggestions with confidence scores and expert advice.</p>
                </div>
            </div>
            
            <h3 style='color: #4CAF50; margin-top: 1rem; margin-bottom: 1rem;'>🌽 Available Crops in Our System:</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Display all available crops
        crops = list(df['label'].unique())
        cols = st.columns(5)
        
        for idx, crop in enumerate(crops):
            with cols[idx % 5]:
                emoji = crop_profiles[crop].get('emoji', '🌱')
                color = crop_profiles[crop].get('color', '#4CAF50')
                
                st.markdown(f"""
                <div style='text-align: center; padding: 1.5rem; background: white; 
                          border-radius: 15px; margin: 10px; box-shadow: 0 3px 15px rgba(0,0,0,0.08);
                          border: 2px solid {color}30; transition: all 0.3s ease; cursor: pointer;'
                          onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 5px 20px rgba(0,0,0,0.12)';"
                          onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 3px 15px rgba(0,0,0,0.08)';">
                    <div style='font-size: 2.8rem; margin-bottom: 12px;'>{emoji}</div>
                    <strong style='font-size: 1.1rem; color: {color};'>{crop}</strong>
                    <p style='font-size: 0.85rem; color: #777; margin-top: 8px;'>
                        {get_crop_description(crop)[:60]}...
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Show sample data
        with st.expander("📊 View Sample Data from Our Database", expanded=False):
            st.dataframe(df.head(10), use_container_width=True)
            
            # Crop distribution visualization
            st.markdown("##### 📈 Crop Distribution in Training Data")
            crop_counts = df['label'].value_counts()
            
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Get colors for each crop
            colors = [crop_profiles[crop].get('color', '#4CAF50') for crop in crop_counts.index]
            
            bars = ax.bar(crop_counts.index, crop_counts.values, color=colors, edgecolor='white', linewidth=1.5)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                       f'{int(height)}', ha='center', va='bottom', fontweight='bold')
            
            ax.set_ylabel('Number of Samples', fontweight='bold')
            ax.set_title('Distribution of Crops in Training Dataset', fontsize=14, fontweight='bold', pad=20)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            plt.tight_layout()
            st.pyplot(fig)
    
    # Footer
    st.markdown("""
    <div style='background: linear-gradient(135deg, #2E8B57 0%, #1B5E20 100%); 
              color: white; padding: 3rem 2rem; margin-top: 4rem; border-radius: 20px; 
              text-align: center;'>
        <h3 style='color: white; margin-bottom: 1rem;'>🌾 Smart Crop Advisor</h3>
        <p style='opacity: 0.9; font-size: 1.1rem; margin-bottom: 1.5rem;'>AI-Powered Agricultural Recommendation System</p>
        
        <div style='background: rgba(255,255,255,0.1); padding: 1.2rem; border-radius: 10px; margin: 1rem 0;'>
            <p style='margin: 0; font-size: 0.95rem; opacity: 0.8;'>
                <strong>Note:</strong> This system uses synthetic data generated based on agricultural research 
                for demonstration purposes. For real farming decisions, always consult local agricultural 
                extension services and conduct proper soil tests.
            </p>
        </div>
        
        <div style='margin-top: 1.5rem; font-size: 0.9rem; opacity: 0.7;'>
            <p>📧 Contact: info@smartcropadvisor.com | 🌐 Website: www.smartcropadvisor.com</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
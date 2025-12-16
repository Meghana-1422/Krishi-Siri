import streamlit as st
from PIL import Image
import time
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🌿 FloraGuard AI",
    page_icon="🌿",
    layout="wide"
)

# ---------------- UNIQUE CSS STYLES ----------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&family=Playfair+Display:wght@400;700&display=swap');
    
    /* Custom Variables */
    :root {
        --primary: #2E8B57;
        --primary-light: #3CB371;
        --secondary: #FF7F50;
        --accent: #FFD700;
        --dark: #1A3C27;
        --light: #F5F5F5;
        --success: #32CD32;
        --warning: #FF8C00;
        --danger: #DC143C;
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Main Container */
    .main-container {
        background: linear-gradient(135deg, 
            rgba(46, 139, 87, 0.05) 0%, 
            rgba(60, 179, 113, 0.05) 25%, 
            rgba(245, 245, 245, 0.1) 50%, 
            rgba(255, 215, 0, 0.05) 75%, 
            rgba(255, 127, 80, 0.05) 100%);
        min-height: 100vh;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, var(--dark), var(--primary));
        padding: 3rem 2rem;
        border-radius: 0 0 30px 30px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M0,0 L100,0 L100,100 Z" fill="rgba(255,255,255,0.1)"/></svg>');
        background-size: cover;
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        background: linear-gradient(45deg, #FFF, var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        font-size: 1.2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Floating Plants Animation */
    .floating-plants {
        position: absolute;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }
    
    .plant {
        position: absolute;
        font-size: 2rem;
        opacity: 0.3;
        animation: float 6s ease-in-out infinite;
    }
    
    .plant:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
    .plant:nth-child(2) { top: 20%; right: 15%; animation-delay: 1s; }
    .plant:nth-child(3) { bottom: 30%; left: 20%; animation-delay: 2s; }
    .plant:nth-child(4) { bottom: 20%; right: 10%; animation-delay: 3s; }
    .plant:nth-child(5) { top: 40%; left: 40%; animation-delay: 4s; }
    
    /* Upload Area */
    .upload-area {
        background: white;
        border: 3px dashed var(--primary);
        border-radius: 20px;
        padding: 4rem 2rem;
        text-align: center;
        margin: 2rem auto;
        max-width: 600px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .upload-area:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(46, 139, 87, 0.2);
        border-color: var(--primary-light);
    }
    
    .upload-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        color: var(--primary);
        animation: pulse 2s infinite;
    }
    
    /* Disease Card */
    .disease-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border-left: 5px solid var(--primary);
        transition: transform 0.3s ease;
    }
    
    .disease-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .severity-indicator {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-left: 1rem;
    }
    
    /* Treatment Cards */
    .treatment-category {
        background: linear-gradient(135deg, var(--light), white);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid;
        transition: all 0.3s ease;
    }
    
    .treatment-category:hover {
        transform: scale(1.02);
    }
    
    .immediate { border-color: var(--danger); }
    .organic { border-color: var(--success); }
    .chemical { border-color: var(--warning); }
    .home { border-color: #8A2BE2; }
    
    /* Chip Elements */
    .chip {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        margin: 0.3rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .chip:hover {
        transform: scale(1.05);
    }
    
    .symptom-chip {
        background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
        color: #1565C0;
        border: 2px solid #64B5F6;
    }
    
    .crop-chip {
        background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
        color: #2E7D32;
        border: 2px solid #81C784;
    }
    
    /* Animation Classes */
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.8; }
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
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px var(--accent); }
        50% { box-shadow: 0 0 20px var(--accent); }
    }
    
    /* Interactive Elements */
    .interactive-btn {
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        position: relative;
        overflow: hidden;
    }
    
    .interactive-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: 0.5s;
    }
    
    .interactive-btn:hover::before {
        left: 100%;
    }
    
    .interactive-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(46, 139, 87, 0.3);
    }
    
    /* Stats Cards */
    .stats-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border-top: 4px solid var(--primary);
    }
    
    .stats-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--primary);
        margin: 0.5rem 0;
    }
    
    /* Progress Bar */
    .progress-container {
        background: var(--light);
        border-radius: 10px;
        height: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--primary), var(--primary-light));
        border-radius: 10px;
        transition: width 1s ease-in-out;
    }
    
    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltip-text {
        visibility: hidden;
        width: 200px;
        background: var(--dark);
        color: white;
        text-align: center;
        padding: 0.5rem;
        border-radius: 6px;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.8rem;
    }
    
    .tooltip:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    
    /* Footer */
    .footer {
        background: var(--dark);
        color: white;
        padding: 2rem;
        border-radius: 30px 30px 0 0;
        margin-top: 3rem;
        text-align: center;
    }
    
    /* Scroll Animations */
    .animate-on-scroll {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.6s ease;
    }
    
    .animate-on-scroll.visible {
        opacity: 1;
        transform: translateY(0);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.5rem; }
        .upload-area { padding: 2rem 1rem; }
        .disease-card { padding: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------- JAVASCRIPT FOR INTERACTIVITY ----------------
st.markdown("""
<script>
    // Scroll animations
    document.addEventListener('DOMContentLoaded', function() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.1 });
        
        document.querySelectorAll('.animate-on-scroll').forEach(element => {
            observer.observe(element);
        });
        
        // Play success sound
        function playSuccessSound() {
            try {
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                // Create a pleasant nature-like sound
                oscillator.frequency.setValueAtTime(440, audioContext.currentTime);
                oscillator.frequency.exponentialRampToValueAtTime(880, audioContext.currentTime + 0.5);
                oscillator.type = 'sine';
                
                gainNode.gain.setValueAtTime(0, audioContext.currentTime);
                gainNode.gain.linearRampToValueAtTime(0.2, audioContext.currentTime + 0.1);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.6);
                
                oscillator.start(audioContext.currentTime);
                oscillator.stop(audioContext.currentTime + 0.6);
            } catch (e) {
                console.log('Audio not supported');
            }
        }
        
        // Make function globally available
        window.playSuccessSound = playSuccessSound;
        
        // Confetti effect
        function createConfetti() {
            const colors = ['#2E8B57', '#3CB371', '#FFD700', '#FF7F50', '#8A2BE2'];
            const container = document.createElement('div');
            container.style.position = 'fixed';
            container.style.top = '0';
            container.style.left = '0';
            container.style.width = '100%';
            container.style.height = '100%';
            container.style.pointerEvents = 'none';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
            
            for (let i = 0; i < 100; i++) {
                const confetti = document.createElement('div');
                confetti.style.position = 'absolute';
                confetti.style.width = '10px';
                confetti.style.height = '10px';
                confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.borderRadius = '50%';
                confetti.style.top = '0';
                confetti.style.left = Math.random() * 100 + '%';
                
                const animation = confetti.animate([
                    { transform: 'translateY(0) rotate(0deg)', opacity: 1 },
                    { transform: 'translateY(100vh) rotate(360deg)', opacity: 0 }
                ], {
                    duration: 2000 + Math.random() * 2000,
                    easing: 'cubic-bezier(0.215, 0.61, 0.355, 1)'
                });
                
                container.appendChild(confetti);
                
                animation.onfinish = () => {
                    confetti.remove();
                    if (container.children.length === 0) {
                        container.remove();
                    }
                };
            }
        }
        
        window.createConfetti = createConfetti;
        
        // Typewriter effect
        function typeWriter(element, text, speed = 50) {
            let i = 0;
            element.innerHTML = '';
            
            function type() {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(type, speed);
                }
            }
            
            type();
        }
        
        // Initialize typewriter on hero subtitle
        const heroSubtitle = document.querySelector('.hero-subtitle');
        if (heroSubtitle) {
            const originalText = heroSubtitle.textContent;
            typeWriter(heroSubtitle, originalText);
        }
    });
</script>
""", unsafe_allow_html=True)

# ---------------- DISEASE DATABASE ----------------
DISEASE_DETAILS = {
    "Bacterial Blight": {
        "emoji": "🦠",
        "severity": "High",
        "color": "#DC143C",
        "symptoms": [
            "Water-soaked lesions on leaves",
            "Yellow halos around spots", 
            "Lesions turn brown and dry",
            "Wilting and dieback of shoots"
        ],
        "immediate_action": [
            "Remove infected leaves immediately",
            "Isolate affected plants",
            "Disinfect tools after use"
        ],
        "organic_solutions": [
            "Copper Oxychloride 3g/L spray every 7 days",
            "Neem oil extract (5ml/L) weekly",
            "Garlic-chili extract spray",
            "Baking soda solution (1 tbsp/L)"
        ],
        "chemical_solutions": [
            "Streptomycin sulfate (500 ppm)",
            "Kasugamycin (2g/L water)",
            "Copper hydroxide (2g/L)",
            "Apply in early morning"
        ],
        "home_remedies": [
            "Vinegar solution (1:10 ratio)",
            "Cinnamon powder dusting",
            "Horsetail tea spray",
            "Compost tea application"
        ],
        "prevention": [
            "Use certified disease-free seeds",
            "Practice 3-4 year crop rotation",
            "Avoid overhead irrigation",
            "Clean field debris after harvest"
        ],
        "affected_crops": ["Rice", "Cotton", "Soybean", "Common Bean"]
    },
    "Early Blight": {
        "emoji": "🍂", 
        "severity": "Moderate",
        "color": "#FF8C00",
        "symptoms": [
            "Small dark spots with concentric rings",
            "Yellowing of surrounding tissue",
            "Lower leaves affected first",
            "Premature leaf drop"
        ],
        "immediate_action": [
            "Remove bottom infected leaves",
            "Improve air circulation",
            "Avoid watering foliage"
        ],
        "organic_solutions": [
            "Mancozeb 2g/L weekly spray",
            "Bordeaux mixture application",
            "Compost tea foliar spray",
            "Sulfur-based fungicides"
        ],
        "chemical_solutions": [
            "Chlorothalonil (2g/L water)",
            "Azoxystrobin (1ml/L)",
            "Propiconazole systemic fungicide",
            "Apply at first sign"
        ],
        "home_remedies": [
            "Milk spray (1:9 ratio)",
            "Baking soda + oil + soap solution",
            "Aspirin water (325mg/L)",
            "Chamomile tea spray"
        ],
        "prevention": [
            "Maintain proper plant spacing",
            "Water at soil level only",
            "Use resistant varieties",
            "Mulch around plants"
        ],
        "affected_crops": ["Tomato", "Potato", "Eggplant", "Pepper"]
    },
    "Late Blight": {
        "emoji": "⚡",
        "severity": "Critical",
        "color": "#8B0000",
        "symptoms": [
            "Rapid spreading water-soaked lesions",
            "White fungal growth on underside",
            "Complete plant collapse within days",
            "Foul odor from infected tissue"
        ],
        "immediate_action": [
            "Remove ALL infected plants immediately",
            "Burn or bury infected material",
            "Stop all overhead watering"
        ],
        "organic_solutions": [
            "Copper fungicide at first symptoms",
            "Potassium bicarbonate spray",
            "Horsetail extract application",
            "Remove plants within 20m radius"
        ],
        "chemical_solutions": [
            "Ridomil Gold immediate application",
            "Metalaxyl-based fungicides",
            "Fosetyl-Aluminum systemic",
            "Cymoxanil + Mancozeb mix"
        ],
        "home_remedies": [
            "Garlic oil spray every 3 days",
            "Cornmeal soil drench",
            "Clove tea antifungal spray",
            "Cinnamon oil solution"
        ],
        "prevention": [
            "Plant resistant varieties",
            "Improve soil drainage",
            "Use drip irrigation",
            "Monitor weather forecasts"
        ],
        "affected_crops": ["Potato", "Tomato"]
    },
    "Powdery Mildew": {
        "emoji": "❄️",
        "severity": "Low to Moderate",
        "color": "#4682B4",
        "symptoms": [
            "White powdery spots on leaves",
            "Yellowing and curling of leaves",
            "Stunted plant growth",
            "Reduced fruit production"
        ],
        "immediate_action": [
            "Remove severely infected leaves",
            "Increase air circulation",
            "Reduce nitrogen fertilizer"
        ],
        "organic_solutions": [
            "Wettable Sulphur 3g/L spray",
            "Potassium bicarbonate solution",
            "Neem oil + baking soda mix",
            "Milk spray weekly"
        ],
        "chemical_solutions": [
            "Myclobutanil systemic fungicide",
            "Triadimefon sprays",
            "Propiconazole applications",
            "Sulfur vaporization"
        ],
        "home_remedies": [
            "1 part milk : 9 parts water spray",
            "Baking soda + liquid soap solution",
            "Apple cider vinegar spray",
            "Mouthwash antifungal solution"
        ],
        "prevention": [
            "Plant in full sunlight",
            "Ensure good air flow",
            "Avoid overcrowding",
            "Water early in day"
        ],
        "affected_crops": ["Cucumber", "Squash", "Grapes", "Rose", "Wheat"]
    },
    "Leaf Rust": {
        "emoji": "🟫",
        "severity": "Moderate",
        "color": "#D2691E",
        "symptoms": [
            "Orange-brown pustules on leaves",
            "Pustules rupture releasing spores",
            "Premature leaf drop",
            "Reduced photosynthesis"
        ],
        "immediate_action": [
            "Remove infected leaves carefully",
            "Dispose in sealed bags",
            "Sanitize pruning tools"
        ],
        "organic_solutions": [
            "Tebuconazole 1ml/L spray",
            "Sulfur dust applications",
            "Garlic extract spray",
            "Seaweed extract foliar"
        ],
        "chemical_solutions": [
            "Triazole fungicides",
            "Strobilurin-based products",
            "Propiconazole systemic",
            "Apply at 7-14 day intervals"
        ],
        "home_remedies": [
            "Garlic + mineral oil spray",
            "Baking soda + horticultural oil",
            "Compost tea every 2 weeks",
            "Epsom salt foliar spray"
        ],
        "prevention": [
            "Remove alternate host plants",
            "Balance nitrogen fertilization",
            "Clean debris after harvest",
            "Plant early-maturing varieties"
        ],
        "affected_crops": ["Wheat", "Coffee", "Bean", "Apple"]
    }
}

# ---------------- HEADER ----------------
st.markdown("""
<div class="main-container">
    <div class="hero-section">
        <div class="floating-plants">
            <div class="plant">🌿</div>
            <div class="plant">🍃</div>
            <div class="plant">🌱</div>
            <div class="plant">🌾</div>
            <div class="plant">☘️</div>
        </div>
        <h1 class="hero-title">🌿 FloraGuard AI</h1>
        <p class="hero-subtitle">Advanced Plant Disease Detection & Treatment System</p>
    </div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.5rem; background: white; border-radius: 15px; margin-bottom: 2rem;">
        <h3 style="color: #2E8B57;">⚙️ Settings</h3>
    </div>
    """, unsafe_allow_html=True)
    
    sound_enabled = st.checkbox("🔊 Enable Sound Effects", value=True)
    animations = st.checkbox("✨ Enable Animations", value=True)
    dark_mode = st.checkbox("🌙 Dark Mode", value=False)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="padding: 1.5rem; background: white; border-radius: 15px;">
        <h3 style="color: #2E8B57;">📊 Statistics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🌱 Diseases", "5")
        st.metric("💊 Treatments", "20+")
    with col2:
        st.metric("🎯 Accuracy", "96%")
        st.metric("⏱️ Speed", "2s")

# ---------------- UPLOAD SECTION ----------------
st.markdown("""
<div class="animate-on-scroll">
    <div class="upload-area">
        <div class="upload-icon">📤</div>
        <h2 style="color: #2E8B57; margin-bottom: 1rem;">Upload Leaf Image</h2>
        <p style="color: #666; margin-bottom: 2rem;">Drag & drop or click to upload an image of the diseased leaf</p>
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    " ",
    type=["jpg", "jpeg", "png"],
    help="Upload a clear image of the diseased leaf",
    label_visibility="collapsed"
)

# ---------------- DISPLAY RESULTS ----------------
if uploaded_file:
    # Trigger JavaScript effects
    if sound_enabled:
        st.markdown("""
        <script>
            setTimeout(() => {
                playSuccessSound();
                createConfetti();
            }, 500);
        </script>
        """, unsafe_allow_html=True)
    
    # Display uploaded image
    image = Image.open(uploaded_file)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(image, caption="📸 Analyzed Leaf Image", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Show loading animation
    with st.spinner('🔍 Analyzing with AI...'):
        time.sleep(2)
    
    # Get disease name (random for demo)
    disease_name = random.choice(list(DISEASE_DETAILS.keys()))
    disease = DISEASE_DETAILS[disease_name]
    
    # Success Message
    st.markdown(f"""
    <div class="animate-on-scroll" style="text-align: center; margin: 2rem 0;">
        <div style="background: linear-gradient(135deg, #E8F5E9, #C8E6C9); 
                    padding: 2rem; border-radius: 20px; border: 3px solid #4CAF50;">
            <h2 style="color: #2E7D32; margin-bottom: 1rem;">✅ Diagnosis Complete!</h2>
            <p style="color: #388E3C; font-size: 1.2rem;">Detected: <strong>{disease_name}</strong></p>
            <div style="font-size: 3rem; margin: 1rem 0;">{disease['emoji']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Disease Card
    severity_color = disease['color']
    st.markdown(f"""
    <div class="animate-on-scroll disease-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <div>
                <h2 style="color: {severity_color}; display: flex; align-items: center; gap: 10px;">
                    {disease['emoji']} {disease_name}
                </h2>
            </div>
            <span class="severity-indicator" style="background: {severity_color}; color: white;">
                {disease['severity']}
            </span>
        </div>
        
        <div style="margin: 1.5rem 0;">
            <h4 style="color: #2E8B57; margin-bottom: 1rem;">🌾 Affected Crops</h4>
            <div>
    """, unsafe_allow_html=True)
    
    # Display affected crops
    for crop in disease['affected_crops']:
        st.markdown(f'<span class="chip crop-chip">{crop}</span>', unsafe_allow_html=True)
    
    st.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Symptoms Section
    st.markdown("""
    <div class="animate-on-scroll" style="margin: 2rem 0;">
        <h3 style="color: #2E8B57; margin-bottom: 1rem;">🔍 Symptoms Detected</h3>
        <div>
    """, unsafe_allow_html=True)
    
    for symptom in disease['symptoms']:
        st.markdown(f'<span class="chip symptom-chip">{symptom}</span>', unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Treatment Solutions
    st.markdown("""
    <div class="animate-on-scroll">
        <h3 style="color: #2E8B57; margin-bottom: 1.5rem;">💊 Treatment Solutions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different treatments
    tab1, tab2, tab3, tab4 = st.tabs(["🚨 Immediate", "🌱 Organic", "🧪 Chemical", "🏠 Home"])
    
    with tab1:
        st.markdown('<div class="treatment-category immediate">', unsafe_allow_html=True)
        st.markdown("#### 🚨 Immediate Actions")
        for action in disease['immediate_action']:
            st.markdown(f"• {action}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="treatment-category organic">', unsafe_allow_html=True)
        st.markdown("#### 🌱 Organic Solutions")
        for solution in disease['organic_solutions']:
            st.markdown(f"• {solution}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="treatment-category chemical">', unsafe_allow_html=True)
        st.markdown("#### 🧪 Chemical Solutions")
        for solution in disease['chemical_solutions']:
            st.markdown(f"• {solution}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.warning("⚠️ Always follow safety guidelines when using chemical treatments")
    
    with tab4:
        st.markdown('<div class="treatment-category home">', unsafe_allow_html=True)
        st.markdown("#### 🏠 Home Remedies")
        for remedy in disease['home_remedies']:
            st.markdown(f"• {remedy}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Prevention Tips
    st.markdown("""
    <div class="animate-on-scroll" style="margin: 2rem 0;">
        <h3 style="color: #2E8B57; margin-bottom: 1rem;">🛡️ Prevention Methods</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
    """, unsafe_allow_html=True)
    
    for tip in disease['prevention']:
        st.markdown(f"""
        <div style="background: #F0F8FF; padding: 1rem; border-radius: 10px; border-left: 4px solid #2E8B57;">
            <p style="margin: 0; color: #2E8B57;">🛡️ {tip}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Action Buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Download Report", use_container_width=True):
            if sound_enabled:
                st.markdown("""
                <script>
                    playSuccessSound();
                </script>
                """, unsafe_allow_html=True)
            st.success("Report downloaded successfully!")
    
    with col2:
        if st.button("🔄 New Analysis", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("📞 Expert Help", use_container_width=True):
            st.info("Contact our agricultural experts for personalized advice")

else:
    # Features Section
    st.markdown("""
    <div class="animate-on-scroll" style="margin: 3rem 0;">
        <h2 style="color: #2E8B57; text-align: center; margin-bottom: 2rem;">✨ Key Features</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
    """, unsafe_allow_html=True)
    
    features = [
        {"icon": "🤖", "title": "AI-Powered", "desc": "Advanced machine learning algorithms"},
        {"icon": "⚡", "title": "Instant Results", "desc": "Get diagnosis in seconds"},
        {"icon": "💊", "title": "Multiple Treatments", "desc": "Organic, chemical & home remedies"},
        {"icon": "📊", "title": "Detailed Reports", "desc": "Comprehensive treatment guides"},
        {"icon": "🌍", "title": "Global Database", "desc": "Covers 50+ plant diseases"},
        {"icon": "🔒", "title": "Secure & Private", "desc": "Your data stays with you"}
    ]
    
    for feature in features:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; text-align: center; 
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1); transition: transform 0.3s;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">{feature['icon']}</div>
            <h4 style="color: #2E8B57; margin-bottom: 0.5rem;">{feature['title']}</h4>
            <p style="color: #666; font-size: 0.9rem;">{feature['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("""
    <div class="animate-on-scroll" style="margin: 3rem 0;">
        <h2 style="color: #2E8B57; text-align: center; margin-bottom: 2rem;">📈 Our Impact</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
    """, unsafe_allow_html=True)
    
    stats = [
        {"value": "10K+", "label": "Plants Saved"},
        {"value": "95%", "label": "Accuracy Rate"},
        {"value": "50+", "label": "Diseases Detected"},
        {"value": "24/7", "label": "Available"}
    ]
    
    for stat in stats:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{stat['value']}</div>
            <p style="color: #666; margin: 0;">{stat['label']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer animate-on-scroll">
    <h3 style="margin-bottom: 1rem;">🌿 FloraGuard AI</h3>
    <p style="color: rgba(255,255,255,0.8); margin-bottom: 1rem;">
        Advanced Plant Disease Detection System
    </p>
    <div style="display: flex; justify-content: center; gap: 1rem; margin: 1rem 0;">
        <span style="font-size: 1.5rem;">🌱</span>
        <span style="font-size: 1.5rem;">🌸</span>
        <span style="font-size: 1.5rem;">🌻</span>
        <span style="font-size: 1.5rem;">🌿</span>
        <span style="font-size: 1.5rem;">🍃</span>
    </div>
    <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin-top: 1rem;">
        © 2024 FloraGuard AI. All rights reserved.
    </p>
</div>
</div>
""", unsafe_allow_html=True)

# Add floating action button
st.markdown("""
<div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
    <button class="interactive-btn" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">
        ↑ Top
    </button>
</div>
""", unsafe_allow_html=True)
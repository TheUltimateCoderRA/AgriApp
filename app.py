import streamlit as st
import supabase
import requests
from datetime import datetime, timedelta, timezone
import time
import cv2
import numpy as np
from PIL import Image
import io
import hashlib


css = """
<style>
/* ===== SOFT ORGANIC THEME VARIABLES ===== */
:root {
    /* Soft Organic Color Palette */
    --cream-soft: #fefef8;
    --cream-warm: #fcfaf2;
    --cream-natural: #faf8f0;
    --paper-white: #fffef9;
    
    /* Earthy Organic Gradients */
    --sage-light: #f0f4f0;
    --sage-soft: #e8efe8;
    --moss-light: #e6ede3;
    --moss-soft: #dce5d9;
    --clay-light: #f4f0eb;
    --clay-soft: #ede8e1;
    --stone-light: #f5f3f0;
    --stone-soft: #ebe8e3;
    
    /* Subtle Green Tints */
    --organic-green: #e8f1e6;
    --leaf-tint: #f2f7f0;
    --forest-mist: #ecf2e8;
    
    /* Earthy Accents */
    --earth-brown: #a1887f;
    --clay-orange: #d7ccc8;
    --stone-gray: #bcaaa4;
    --accent-terracotta: #bf8a7e;
    --accent-sand: #d7ccc8;
    
    /* Text Colors */
    --text-charcoal: #37474f;
    --text-slate: #546e7a;
    --text-stone: #78909c;
    --text-soft: #90a4ae;
    
    /* Soft Shadows */
    --shadow-organic: 0 2px 12px rgba(58, 71, 59, 0.06);
    --shadow-soft: 0 4px 20px rgba(58, 71, 59, 0.08);
    --shadow-gentle: 0 6px 24px rgba(58, 71, 59, 0.1);
}

/* ===== BASE STYLING ===== */
.stApp {
    background: linear-gradient(135deg, var(--cream-soft) 0%, var(--cream-warm) 50%, var(--sage-light) 100%);
    color: var(--text-charcoal);
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
    line-height: 1.6;
}

/* ===== HEADERS & TITLES ===== */
h1 {
    background: linear-gradient(135deg, var(--text-charcoal) 0%, var(--text-slate) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 600;
    font-size: 2.5rem !important;
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--sage-soft);
}

h2 {
    color: var(--text-charcoal);
    font-weight: 500;
    font-size: 1.8rem !important;
    margin: 2rem 0 1rem 0;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--sage-soft);
}

h3 {
    color: var(--text-slate);
    font-weight: 500;
    font-size: 1.4rem !important;
    margin: 1.5rem 0 0.75rem 0;
}

/* ===== INPUT FIELDS ===== */
.stTextInput>div>div>input, 
.stTextInput>div>div>textarea,
.stNumberInput>div>div>input,
.stSelectbox>div>div>select {
    background: linear-gradient(135deg, var(--paper-white) 0%, var(--cream-natural) 100%) !important;
    border: 1.5px solid var(--sage-soft) !important;
    border-radius: 16px !important;
    padding: 16px 20px !important;
    font-size: 15px !important;
    color: var(--text-charcoal) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: var(--shadow-organic) !important;
    min-height: 52px !important;
}

.stTextInput>div>div>input:focus, 
.stTextInput>div>div>textarea:focus,
.stNumberInput>div>div>input:focus,
.stSelectbox>div>div>select:focus {
    border-color: var(--earth-brown) !important;
    box-shadow: 0 0 0 3px rgba(161, 136, 127, 0.1), var(--shadow-soft) !important;
    outline: none !important;
    background: linear-gradient(135deg, var(--paper-white) 0%, var(--cream-warm) 100%) !important;
    transform: translateY(-1px);
}

/* ===== BUTTONS ===== */
.stButton>button {
    background: linear-gradient(135deg, var(--moss-light) 0%, var(--sage-soft) 50%, var(--organic-green) 100%) !important;
    color: var(--text-charcoal) !important;
    border: 1.5px solid var(--sage-soft) !important;
    border-radius: 20px !important;
    padding: 16px 32px !important;
    font-weight: 500 !important;
    font-size: 15px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: var(--shadow-organic) !important;
    min-height: 54px !important;
    min-width: 120px !important;
}

.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-gentle) !important;
    background: linear-gradient(135deg, var(--sage-soft) 0%, var(--moss-soft) 50%, var(--forest-mist) 100%) !important;
    border-color: var(--earth-brown) !important;
    color: var(--text-charcoal) !important;
}

.stButton>button:active {
    transform: translateY(0) !important;
    box-shadow: var(--shadow-organic) !important;
}

/* Primary Action Buttons */
.stButton>button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent-terracotta) 0%, var(--earth-brown) 100%) !important;
    color: white !important;
    border: none !important;
}

/* ===== SIDEBAR ===== */
.css-1d391kg, .css-1lcbmhc {
    background: linear-gradient(180deg, var(--cream-soft) 0%, var(--sage-light) 50%, var(--cream-warm) 100%) !important;
    border-right: 1px solid var(--sage-soft) !important;
}

.sidebar .sidebar-content {
    background: transparent !important;
    padding: 2rem 1rem !important;
}

/* Sidebar Radio Buttons - Much Larger */
.stRadio>div {
    background: linear-gradient(135deg, var(--paper-white) 0%, var(--cream-natural) 100%) !important;
    border-radius: 20px !important;
    padding: 12px !important;
    border: 1.5px solid var(--sage-soft) !important;
    margin: 8px 0 !important;
}

.stRadio>div[data-baseweb="radio"]>div {
    background: transparent !important;
    padding: 12px 16px !important;
}

.stRadio label {
    font-size: 15px !important;
    font-weight: 500 !important;
    color: var(--text-charcoal) !important;
    padding: 8px 12px !important;
    margin: 4px 0 !important;
    border-radius: 14px !important;
    transition: all 0.3s ease !important;
    min-height: 44px !important;
    display: flex !important;
    align-items: center !important;
}

.stRadio label:hover {
    background: var(--sage-light) !important;
}

.stRadio [data-baseweb="radio"] div:first-child {
    margin-right: 12px !important;
}

/* ===== EXPANDERS ===== */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, var(--paper-white) 0%, var(--cream-natural) 100%) !important;
    border: 1.5px solid var(--sage-soft) !important;
    border-radius: 16px !important;
    color: var(--text-charcoal) !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    margin-bottom: 12px !important;
    padding: 20px 24px !important;
    transition: all 0.3s ease !important;
}

.streamlit-expanderHeader:hover {
    background: linear-gradient(135deg, var(--cream-natural) 0%, var(--sage-light) 100%) !important;
    border-color: var(--earth-brown) !important;
    transform: translateY(-1px);
}

.streamlit-expanderContent {
    background: linear-gradient(135deg, var(--paper-white) 0%, var(--cream-warm) 100%) !important;
    border: 1.5px solid var(--sage-soft) !important;
    border-top: none !important;
    border-radius: 0 0 16px 16px !important;
    padding: 28px !important;
    margin-top: -12px !important;
}

/* ===== METRICS & CARDS ===== */
.stMetric {
    background: linear-gradient(135deg, var(--paper-white) 0%, var(--cream-natural) 100%) !important;
    border: 1.5px solid var(--sage-soft) !important;
    border-radius: 20px !important;
    padding: 24px !important;
    box-shadow: var(--shadow-organic) !important;
    margin: 8px !important;
}

[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 600 !important;
    color: var(--text-charcoal) !important;
}

[data-testid="stMetricLabel"] {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: var(--text-slate) !important;
}

/* ===== PROGRESS BARS ===== */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--moss-light) 0%, var(--sage-soft) 50%, var(--earth-brown) 100%) !important;
    border-radius: 12px !important;
    height: 8px !important;
}

.stProgress > div > div {
    background: var(--sage-light) !important;
    border-radius: 12px !important;
    border: 1px solid var(--sage-soft) !important;
    height: 10px !important;
}

/* ===== TABS - Much Larger & Softer ===== */
.stTabs [data-baseweb="tab-list"] {
    background: linear-gradient(135deg, var(--cream-soft) 0%, var(--sage-light) 100%) !important;
    border-radius: 20px !important;
    padding: 12px !important;
    gap: 8px !important;
    border: 1.5px solid var(--sage-soft) !important;
    margin: 1rem 0 !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 16px !important;
    color: var(--text-slate) !important;
    font-weight: 500 !important;
    font-size: 15px !important;
    padding: 16px 24px !important;
    margin: 4px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    min-height: 54px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background: var(--sage-light) !important;
    color: var(--text-charcoal) !important;
    transform: translateY(-1px);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--moss-light) 0%, var(--sage-soft) 100%) !important;
    color: var(--text-charcoal) !important;
    font-weight: 600 !important;
    box-shadow: var(--shadow-organic) !important;
    border: 1.5px solid var(--earth-brown) !important;
}

/* ===== FILE UPLOADER ===== */
.stFileUploader>div>div {
    background: linear-gradient(135deg, var(--paper-white) 0%, var(--cream-natural) 100%) !important;
    border: 2px dashed var(--sage-soft) !important;
    border-radius: 20px !important;
    padding: 40px !important;
    transition: all 0.3s ease !important;
}

.stFileUploader>div>div:hover {
    border-color: var(--earth-brown) !important;
    background: linear-gradient(135deg, var(--cream-natural) 0%, var(--sage-light) 100%) !important;
    transform: translateY(-2px);
}

/* ===== ALERT MESSAGES ===== */
div[data-testid="stSuccess"] > div {
    background: linear-gradient(135deg, var(--leaf-tint) 0%, var(--organic-green) 100%) !important;
    border: 1.5px solid var(--sage-soft) !important;
    border-radius: 16px !important;
    color: var(--text-charcoal) !important;
    padding: 20px 24px !important;
}

div[data-testid="stError"] > div {
    background: linear-gradient(135deg, #fdf2f2 0%, #fde8e8 100%) !important;
    border: 1.5px solid #fecaca !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
}

div[data-testid="stInfo"] > div {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%) !important;
    border: 1.5px solid #bae6fd !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
}

/* ===== DATA FRAMES & TABLES ===== */
.dataframe {
    border: 1.5px solid var(--sage-soft) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-organic) !important;
}

.dataframe thead th {
    background: linear-gradient(135deg, var(--moss-light) 0%, var(--sage-soft) 100%) !important;
    color: var(--text-charcoal) !important;
    font-weight: 600 !important;
    padding: 16px 12px !important;
    font-size: 14px !important;
}

.dataframe tbody tr:nth-child(even) {
    background: var(--sage-light) !important;
}

.dataframe tbody tr:nth-child(odd) {
    background: var(--paper-white) !important;
}

.dataframe td {
    padding: 14px 12px !important;
    font-size: 14px !important;
    color: var(--text-slate) !important;
}

/* ===== CUSTOM SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: var(--sage-light);
    border-radius: 8px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, var(--sage-soft) 0%, var(--moss-soft) 100%);
    border-radius: 8px;
    border: 2px solid var(--sage-light);
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, var(--moss-soft) 0%, var(--earth-brown) 100%);
}

/* ===== IMAGE CONTAINERS ===== */
.stImage {
    border: 2px solid var(--sage-soft) !important;
    border-radius: 20px !important;
    padding: 12px !important;
    background: var(--paper-white) !important;
    box-shadow: var(--shadow-organic) !important;
}

/* ===== LOGOUT BUTTON ===== */
.stButton>button:contains("Logout") {
    background: linear-gradient(135deg, var(--clay-light) 0%, var(--clay-soft) 100%) !important;
    border-color: var(--stone-gray) !important;
    margin-top: 2rem !important;
}

/* ===== TOKEN DISPLAY ===== */
[data-testid="stMetricValue"]:contains("🪙") {
    color: var(--earth-brown) !important;
}

/* ===== RESPONSIVE DESIGN ===== */
@media (max-width: 768px) {
    .stButton>button {
        padding: 14px 24px !important;
        font-size: 14px !important;
        min-height: 48px !important;
    }
    
    .stTextInput>div>div>input {
        padding: 14px 18px !important;
        min-height: 48px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 16px !important;
        font-size: 14px !important;
        min-height: 48px !important;
    }
}

/* ===== GENTLE ANIMATIONS ===== */
@keyframes gentleFloat {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-2px); }
    100% { transform: translateY(0px); }
}

.stButton>button:hover {
    animation: gentleFloat 1.5s ease-in-out infinite;
}

/* ===== FOCUS STATES ===== */
*:focus {
    outline: 2px solid var(--earth-brown) !important;
    outline-offset: 3px !important;
    border-radius: 8px !important;
}

/* ===== SELECTION ===== */
::selection {
    background: var(--sage-soft);
    color: var(--text-charcoal);
}

::-moz-selection {
    background: var(--sage-soft);
    color: var(--text-charcoal);
}

/* ===== SIDEBAR SPACING IMPROVEMENTS ===== */
.sidebar .stRadio {
    margin: 1rem 0 !important;
}

.sidebar .stButton {
    margin: 0.5rem 0 !important;
}

/* ===== TEXT CONTENT ===== */
.stMarkdown {
    color: var(--text-slate) !important;
    line-height: 1.7 !important;
}

.stMarkdown p {
    margin-bottom: 1rem !important;
    font-size: 15px !important;
}
</style>"""

st.markdown(css, unsafe_allow_html=True)


# ===== FEATURE TOGGLES =====
FEATURES = {
    'DUPLICATE_IMAGE_CHECK': True,  # Prevent same image submissions
    'TOKEN_SYSTEM': True,  # Enable token rewards
    'AI_ANALYSIS': True,  # Enable AI plant analysis
    'HEALTH_BASED_REWARDS': True,  # Tokens based on plant health
}


# Initialize Supabase client
@st.cache_resource
def init_supabase():
    client = supabase.create_client(
        supabase_url="https://ebyigfejpqlrwdmmscrs.supabase.co",
        supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVieWlnZmVqcHFscndkbW1zY3JzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0ODgyMzUsImV4cCI6MjA3NjA2NDIzNX0.IYEggIHdwjaBzWpsqgt4K-RP6gGr9x99IOOnCq_fb-g"
    )
    return client


supabase_client = init_supabase()


# Initialize database tables
def init_database():
    try:
        # Check if seeds exist, if not create them
        seeds = supabase_client.table('seeds').select('*').execute()
        if not seeds.data:
            seed_data = [
                {'name': 'Sunflower', 'type': 'flower', 'growth_increments': 8, 'growth_per_increment_cm': 15,
                 'image_url': '🌻', 'days_per_increment': 7},
                {'name': 'Tomato', 'type': 'vegetable', 'growth_increments': 10, 'growth_per_increment_cm': 12,
                 'image_url': '🍅', 'days_per_increment': 5},
                {'name': 'Basil', 'type': 'herb', 'growth_increments': 6, 'growth_per_increment_cm': 20,
                 'image_url': '🌿', 'days_per_increment': 4},
                {'name': 'Lavender', 'type': 'flower', 'growth_increments': 7, 'growth_per_increment_cm': 17,
                 'image_url': '💜', 'days_per_increment': 6},
                {'name': 'Carrot', 'type': 'vegetable', 'growth_increments': 12, 'growth_per_increment_cm': 10,
                 'image_url': '🥕', 'days_per_increment': 8}
            ]
            for seed in seed_data:
                supabase_client.table('seeds').insert(seed).execute()
    except Exception as e:
        print(f"Init error: {e}")


init_database()


# Auth functions
def sign_up(email, password, username):
    try:
        result = supabase_client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"username": username}}
        })
        return result
    except Exception as e:
        st.error(f"Signup error: {str(e)}")
        return None


def sign_in(email, password):
    try:
        result = supabase_client.auth.sign_in_with_password({"email": email, "password": password})
        return result
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return None


def get_current_user():
    try:
        return supabase_client.auth.get_user()
    except:
        return None


# Database functions
def get_user_seeds(user_id):
    try:
        result = supabase_client.table('user_seeds').select('*').eq('user_id', user_id).execute()
        return result.data
    except:
        return []


def get_user_plants(user_id):
    try:
        result = supabase_client.table('user_plants').select('*').eq('user_id', user_id).execute()
        return result.data
    except:
        return []


def get_user_tokens(user_id):
    if not FEATURES['TOKEN_SYSTEM']:
        return 0

    try:
        result = supabase_client.table('user_tokens').select('*').eq('user_id', user_id).execute()
        if result.data:
            return result.data[0]['tokens']
        else:
            # Initialize with 0 tokens
            supabase_client.table('user_tokens').insert({'user_id': user_id, 'tokens': 0}).execute()
            return 0
    except Exception as e:
        print(f"Token get error: {e}")
        return 0


def award_tokens(user_id, amount, reason):
    if not FEATURES['TOKEN_SYSTEM']:
        return True

    try:
        # Get current tokens
        current_result = supabase_client.table('user_tokens').select('*').eq('user_id', user_id).execute()

        if current_result.data:
            current_tokens = current_result.data[0]['tokens']
            new_total = current_tokens + amount
            # Update existing record
            result = supabase_client.table('user_tokens').update({'tokens': new_total}).eq('user_id', user_id).execute()
        else:
            # Create new record
            new_total = amount
            result = supabase_client.table('user_tokens').insert({'user_id': user_id, 'tokens': new_total}).execute()

        # Log transaction
        supabase_client.table('token_transactions').insert({
            'user_id': user_id,
            'amount': amount,
            'reason': reason,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }).execute()

        print(f"Awarded {amount} tokens to user {user_id}. New total: {new_total}")
        return True
    except Exception as e:
        print(f"Token award error: {e}")
        return False


def get_available_seeds():
    try:
        result = supabase_client.table('seeds').select('*').execute()
        return result.data
    except:
        return []


# Get AI analysis history for a user
def get_analysis_history(user_id):
    try:
        # Get all submissions with plant info and analysis data
        result = supabase_client.table('plant_submissions') \
            .select('*, user_plants!inner(seed_name, user_id)') \
            .eq('user_plants.user_id', user_id) \
            .order('submitted_at', desc=True) \
            .execute()
        return result.data
    except Exception as e:
        print(f"Analysis history error: {e}")
        return []


# Duplicate image check
def is_duplicate_image(plant_id, image_bytes):
    if not FEATURES['DUPLICATE_IMAGE_CHECK']:
        return False

    try:
        # Create image hash
        image_hash = hashlib.md5(image_bytes).hexdigest()

        # Check if this hash exists for this plant
        result = supabase_client.table('plant_submissions').select('*').eq('plant_id', plant_id).eq('image_hash',
                                                                                                    image_hash).execute()

        return len(result.data) > 0
    except:
        return False


def record_submission(plant_id, analysis_result, image_hash=None):
    try:
        submission_data = {
            'plant_id': plant_id,
            'submitted_at': datetime.now(timezone.utc).isoformat(),
            'image_hash': image_hash,
            'health_score': analysis_result.get('health_score'),
            'plant_detected': analysis_result.get('plant_detected', False),
            'analysis_details': analysis_result.get('analysis_details', ''),
            'health_data': analysis_result.get('health_analysis', {})
        }
        result = supabase_client.table('plant_submissions').insert(submission_data).execute()
        return result
    except Exception as e:
        print(f"Submission record error: {e}")
        return None


# Enhanced AI Plant Analysis
def analyze_plant_health(image_bytes):
    """Comprehensive plant health analysis"""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = image.resize((400, 300))
        img_array = np.array(image)

        if len(img_array.shape) == 3:
            img_rgb = img_array
            img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

            # 1. Green health analysis
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([85, 255, 255])
            green_mask = cv2.inRange(img_hsv, lower_green, upper_green)
            green_pixels = np.sum(green_mask > 0)
            total_pixels = img_rgb.shape[0] * img_rgb.shape[1]
            green_ratio = green_pixels / total_pixels

            # 2. Yellow detection (unhealthy leaves)
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])
            yellow_mask = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
            yellow_ratio = np.sum(yellow_mask > 0) / total_pixels

            # 3. Brown detection (dead/dying areas)
            lower_brown = np.array([10, 50, 20])
            upper_brown = np.array([20, 150, 100])
            brown_mask = cv2.inRange(img_hsv, lower_brown, upper_brown)
            brown_ratio = np.sum(brown_mask > 0) / total_pixels

            # 4. Texture analysis
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / total_pixels

            # 5. Color variance (healthy plants have color diversity)
            color_variance = np.var(img_rgb, axis=(0, 1))
            avg_color_variance = np.mean(color_variance)

            # 6. Brightness analysis (proper lighting)
            brightness = np.mean(gray)

        else:
            # Grayscale fallback
            green_ratio = yellow_ratio = brown_ratio = 0.05
            edge_density = 0.01
            avg_color_variance = 0
            brightness = 128

        # Health scoring with multiple factors
        green_score = min(green_ratio * 1.5, 0.4)  # Max 40%
        texture_score = min(edge_density * 8, 0.2)  # Max 20%
        color_score = min(avg_color_variance / 800, 0.15)  # Max 15%
        brightness_score = min(abs(brightness - 128) / 128, 0.1)  # Max 10% (optimal brightness)

        # Penalties for unhealthy indicators
        yellow_penalty = yellow_ratio * 0.3  # Up to 30% penalty
        brown_penalty = brown_ratio * 0.5  # Up to 50% penalty

        health_score = (
                                   green_score + texture_score + color_score + brightness_score - yellow_penalty - brown_penalty) * 100
        health_score = max(0, min(health_score, 85))  # Cap between 0-85%

        plant_detected = green_ratio > 0.08 or edge_density > 0.02
        is_healthy = health_score > 30

        health_analysis = {
            'plant_detected': plant_detected,
            'is_healthy': is_healthy,
            'health_score': float(health_score),
            'green_ratio': float(green_ratio),
            'yellow_ratio': float(yellow_ratio),
            'brown_ratio': float(brown_ratio),
            'edge_density': float(edge_density),
            'color_variance': float(avg_color_variance),
            'brightness': float(brightness),
            'health_breakdown': {
                'green_score': float(green_score * 100),
                'texture_score': float(texture_score * 100),
                'color_score': float(color_score * 100),
                'brightness_score': float(brightness_score * 100),
                'yellow_penalty': float(yellow_penalty * 100),
                'brown_penalty': float(brown_penalty * 100)
            }
        }

        return health_analysis

    except Exception as e:
        return {'error': str(e)}


def analyze_plant(image_bytes):
    """Main analysis function"""
    if not FEATURES['AI_ANALYSIS']:
        return {
            'verification_passed': True,
            'health_score': 70,
            'analysis_details': "AI Analysis Disabled - Auto Pass"
        }

    try:
        # Run health analysis
        health_analysis = analyze_plant_health(image_bytes)
        if health_analysis.get('error'):
            return {'error': health_analysis['error'], 'verification_passed': False}

        verification_passed = health_analysis.get('is_healthy', False)

        # Create detailed analysis report
        analysis_details = f"Health: {health_analysis['health_score']:.1f}%"

        result = {
            'verification_passed': verification_passed,
            'health_score': health_analysis['health_score'],
            'health_analysis': health_analysis,
            'analysis_details': analysis_details,
            'plant_detected': health_analysis.get('plant_detected', False)
        }

        return result

    except Exception as e:
        return {'error': str(e), 'verification_passed': False}


# Token calculation with detailed breakdown
def calculate_tokens(health_score, current_increment):
    if not FEATURES['TOKEN_SYSTEM']:
        return 0, {}

    if not FEATURES['HEALTH_BASED_REWARDS']:
        # Fixed tokens if health-based rewards disabled
        tokens = 50 + (current_increment * 10)
        breakdown = {
            'base_tokens': 50,
            'health_bonus': 0,
            'stage_bonus': current_increment * 10,
            'total': tokens
        }
        return tokens, breakdown

    # Base tokens per stage
    base_tokens = 50

    # Health bonus (scaled realistically)
    health_bonus = int((health_score / 85) * 50)

    # Stage bonus (increases with each stage)
    stage_bonus = current_increment * 10

    total_tokens = base_tokens + health_bonus + stage_bonus

    breakdown = {
        'base_tokens': base_tokens,
        'health_bonus': health_bonus,
        'stage_bonus': stage_bonus,
        'total': total_tokens
    }

    return total_tokens, breakdown


# App UI
st.set_page_config(page_title="AgriApp", page_icon="🌱", layout="wide")
st.title("🌱 AgriApp- Grow Plants, Earn Tokens!")


def main():
    user_info = get_current_user()

    if not user_info or not user_info.user:
        show_auth_interface()
    else:
        show_main_app(user_info.user)


def show_auth_interface():
    st.header("Welcome to PlantReward!")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.subheader("Login to Your Account")
        email = st.text_input("Email", key="login_email_input")
        password = st.text_input("Password", type="password", key="login_password_input")
        if st.button("Login", key="login_button"):
            if email and password:
                result = sign_in(email, password)
                if result and result.user:
                    st.success("✅ Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Login failed")

    with tab2:
        st.subheader("Create New Account")
        username = st.text_input("Username", key="signup_username_input")
        email = st.text_input("Email", key="signup_email_input")
        password = st.text_input("Password", type="password", key="signup_password_input")
        if st.button("Sign Up", key="signup_button"):
            if username and email and password:
                result = sign_up(email, password, username)
                if result and result.user:
                    st.success("✅ Account created! You can now login.")
                else:
                    st.error("❌ Sign up failed")


def show_main_app(user):
    st.sidebar.title(f"Welcome, {user.user_metadata.get('username', 'Gardener')}!")

    # Get and display tokens
    user_tokens = get_user_tokens(user.id)
    if FEATURES['TOKEN_SYSTEM']:
        st.sidebar.metric("Your Tokens", f"{user_tokens} 🪙")

    # Navigation
    page = st.sidebar.radio("Go to:", ["Dashboard", "Get Seeds", "Plant & Track", "My Plants", "AI Analysis History", "Shop"],
                            key="nav_radio")

    if page == "Dashboard":
        show_dashboard(user)
    elif page == "Get Seeds":
        show_seed_selection(user)
    elif page == "Plant & Track":
        show_plant_tracking(user)
    elif page == "My Plants":
        show_my_plants(user)
    elif page == "AI Analysis History":
        show_analysis_history(user)
    elif page == "Shop":
        show_shop(user)

    if st.sidebar.button("Logout", key="logout_button"):
        supabase_client.auth.sign_out()
        st.rerun()


def show_dashboard(user):
    st.header("📊 Your Dashboard")

    user_plants = get_user_plants(user.id)
    user_tokens = get_user_tokens(user.id)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Plants", len(user_plants))
    with col2:
        active_plants = [p for p in user_plants if p.get('is_active', True)]
        st.metric("Active Plants", len(active_plants))
    with col3:
        if FEATURES['TOKEN_SYSTEM']:
            st.metric("Total Tokens", user_tokens)
        else:
            completed = [p for p in user_plants if not p.get('is_active', True)]
            st.metric("Completed", len(completed))

    # Feature status
    st.subheader("🔧 System Status")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**AI Analysis:**", "✅ On" if FEATURES['AI_ANALYSIS'] else "❌ Off")
    with col2:
        st.write("**Token System:**", "✅ On" if FEATURES['TOKEN_SYSTEM'] else "❌ Off")
    with col3:
        st.write("**Duplicate Check:**", "✅ On" if FEATURES['DUPLICATE_IMAGE_CHECK'] else "❌ Off")

    # Quick actions
    # Recent plants
    st.subheader("Your Plant Progress")
    if user_plants:
        for i, plant in enumerate(user_plants[-3:]):
            progress = min(100, (plant.get('current_height', 0) / 122) * 100)
            status = "✅ Complete" if not plant.get('is_active', True) else "🌱 Growing"
            st.progress(progress / 100, text=f"{plant['seed_name']} - {status} - {progress:.1f}%")
    else:
        st.info("No plants yet! Get some seeds and start planting!")


def show_seed_selection(user):
    st.header("🌱 Get Your Free Seeds!")
    st.success("Choose up to 50 seeds total from 5 different types!")

    available_seeds = get_available_seeds()
    user_seeds = get_user_seeds(user.id)

    total_selected = sum(seed.get('quantity', 0) for seed in user_seeds)
    remaining_seeds = 50 - total_selected

    st.write(f"**Seeds selected:** {total_selected}/50")
    st.write(f"**Remaining:** {remaining_seeds} seeds")

    selected_seeds = {}

    for seed in available_seeds:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.write(f"**{seed['image_url']}**")
        with col2:
            st.write(f"**{seed['name']}**")
            st.write(f"Type: {seed['type']} | Growth: {seed['growth_increments']} stages")
        with col3:
            max_qty = min(20, remaining_seeds)
            quantity = st.number_input(f"Quantity", 0, max_qty, 0, key=f"seed_qty_{seed['name']}")
            if quantity > 0:
                selected_seeds[seed['name']] = quantity

    if st.button("Add Selected Seeds to Collection", key="add_seeds_button"):
        total_new_seeds = sum(selected_seeds.values())
        if total_new_seeds == 0:
            st.warning("Please select at least one seed")
        elif total_new_seeds <= remaining_seeds:
            for seed_name, quantity in selected_seeds.items():
                if quantity > 0:
                    # Add or update user seeds
                    supabase_client.table('user_seeds').upsert({
                        'user_id': user.id,
                        'seed_name': seed_name,
                        'quantity': quantity
                    }).execute()
            st.success(f"🎉 Added {total_new_seeds} seeds to your collection!")
            time.sleep(1)
            st.rerun()
        else:
            st.error(f"You can only select {remaining_seeds} more seeds!")


def show_plant_tracking(user):
    st.header("🌿 Plant & Track Growth")

    # Section 1: Plant new seeds
    st.subheader("1. Plant New Seeds")
    user_seeds = get_user_seeds(user.id)
    available_seeds = [seed for seed in user_seeds if seed.get('quantity', 0) > 0]

    if available_seeds:
        seed_options = {f"{seed['seed_name']} ({seed['quantity']} left)": seed for seed in available_seeds}
        selected_seed = st.selectbox("Choose seed to plant:", list(seed_options.keys()), key="plant_seed_select")

        if st.button("Plant This Seed", key="plant_seed_button"):
            chosen_seed = seed_options[selected_seed]
            # Create new plant
            plant_data = {
                'user_id': user.id,
                'seed_name': chosen_seed['seed_name'],
                'planted_date': datetime.now(timezone.utc).isoformat(),
                'current_height': 0,
                'current_increment': 0,
                'is_active': True,
                'last_update': datetime.now(timezone.utc).isoformat()
            }
            supabase_client.table('user_plants').insert(plant_data).execute()

            # Reduce seed count
            new_quantity = chosen_seed['quantity'] - 1
            supabase_client.table('user_seeds').update({'quantity': new_quantity}).eq('user_id', user.id).eq(
                'seed_name', chosen_seed['seed_name']).execute()

            st.success(f"🌱 Planted {chosen_seed['seed_name']}! Now track its growth below.")
            time.sleep(1)
            st.rerun()
    else:
        st.warning("No seeds available! Get some seeds first.")

    # Section 2: Track existing plants
    st.subheader("2. Track Growth")

    # Show feature status
    status_cols = st.columns(3)
    with status_cols[0]:
        st.write("**AI:**", "✅" if FEATURES['AI_ANALYSIS'] else "❌")
    with status_cols[1]:
        st.write("**Tokens:**", "✅" if FEATURES['TOKEN_SYSTEM'] else "❌")
    with status_cols[2]:
        st.write("**Dup Check:**", "✅" if FEATURES['DUPLICATE_IMAGE_CHECK'] else "❌")

    user_plants = get_user_plants(user.id)
    active_plants = [p for p in user_plants if p.get('is_active', True)]

    if not active_plants:
        st.info("No active plants to track. Plant a seed first!")
        return

    for i, plant in enumerate(active_plants):
        with st.expander(
                f"{plant['seed_name']} - Height: {plant.get('current_height', 0)}cm - Stage: {plant.get('current_increment', 0)}"):

            uploaded_file = st.file_uploader(f"Upload progress photo", type=['jpg', 'png', 'jpeg'],
                                             key=f"upload_{plant['id']}_{i}")

            if uploaded_file is not None:
                # SMALLER image display
                st.image(uploaded_file, caption="Your plant photo", width=200)

                if st.button(f"Submit Progress", key=f"analyze_{plant['id']}_{i}"):
                    image_bytes = uploaded_file.getvalue()

                    # Duplicate image check
                    if FEATURES['DUPLICATE_IMAGE_CHECK'] and is_duplicate_image(plant['id'], image_bytes):
                        st.error("❌ This image has already been submitted before!")
                        return

                    with st.spinner("🤖 Analyzing plant health..."):
                        analysis = analyze_plant(image_bytes)
                        time.sleep(2)

                    # Show detailed results
                    if analysis.get('error'):
                        st.error(f"❌ Analysis Error: {analysis['error']}")
                    else:
                        # Health Analysis Display
                        st.subheader("🔍 Health Analysis")
                        health = analysis.get('health_analysis', {})

                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            health_score = analysis.get('health_score', 0)
                            if health_score > 60:
                                st.success(f"**{health_score:.1f}%**")
                                st.write("Excellent")
                            elif health_score > 40:
                                st.warning(f"**{health_score:.1f}%**")
                                st.write("Good")
                            else:
                                st.error(f"**{health_score:.1f}%**")
                                st.write("Needs Care")

                        with col2:
                            st.metric("Green", f"{health.get('green_ratio', 0) * 100:.1f}%")
                        with col3:
                            yellow = health.get('yellow_ratio', 0) * 100
                            st.metric("Yellow", f"{yellow:.1f}%", delta=f"{-yellow:.1f}%" if yellow > 0 else None)
                        with col4:
                            brown = health.get('brown_ratio', 0) * 100
                            st.metric("Brown", f"{brown:.1f}%", delta=f"{-brown:.1f}%" if brown > 0 else None)

                        # Final Verification Result
                        if analysis.get('verification_passed'):
                            st.success("✅ **VERIFICATION PASSED!**")

                            # Calculate tokens with detailed breakdown
                            current_increment = plant.get('current_increment', 0)
                            tokens_earned, token_breakdown = calculate_tokens(analysis.get('health_score', 70),
                                                                              current_increment)

                            # Update plant growth
                            seed_info = next((s for s in get_available_seeds() if s['name'] == plant['seed_name']),
                                             None)
                            if seed_info:
                                new_increment = current_increment + 1
                                new_height = new_increment * seed_info['growth_per_increment_cm']

                                # Update plant in database
                                supabase_client.table('user_plants').update({
                                    'current_increment': new_increment,
                                    'current_height': new_height,
                                    'last_update': datetime.now(timezone.utc).isoformat()
                                }).eq('id', plant['id']).execute()

                                # Record submission and image hash WITH ANALYSIS DATA
                                image_hash = hashlib.md5(image_bytes).hexdigest() if FEATURES[
                                    'DUPLICATE_IMAGE_CHECK'] else None
                                record_submission(plant['id'], analysis, image_hash)

                                # Award tokens
                                if FEATURES['TOKEN_SYSTEM'] and tokens_earned > 0:
                                    award_success = award_tokens(user.id, tokens_earned,
                                                                 f"Growth stage {new_increment} for {plant['seed_name']}")

                                    if award_success:
                                        # SHOW DETAILED TOKEN BREAKDOWN
                                        st.success(f"🎉 **+{tokens_earned} TOKENS AWARDED!**")

                                        # Token breakdown display
                                        st.subheader("💰 Token Breakdown")
                                        breakdown_cols = st.columns(4)

                                        with breakdown_cols[0]:
                                            st.metric("Base", f"{token_breakdown['base_tokens']}")
                                        with breakdown_cols[1]:
                                            st.metric("Health Bonus", f"+{token_breakdown['health_bonus']}")
                                        with breakdown_cols[2]:
                                            st.metric("Stage Bonus", f"+{token_breakdown['stage_bonus']}")
                                        with breakdown_cols[3]:
                                            st.metric("Total", f"{token_breakdown['total']}",
                                                      delta=f"+{token_breakdown['total']}")

                                st.success(f"📏 Plant grew to {new_height}cm!")

                                # Check for full growth bonus
                                if new_height >= 122:
                                    if FEATURES['TOKEN_SYSTEM']:
                                        award_tokens(user.id, 200, f"FULL GROWTH BONUS: {plant['seed_name']}")
                                        st.success("💰 **+200 BONUS TOKENS FOR FULL GROWTH!**")
                                    supabase_client.table('user_plants').update({'is_active': False}).eq('id', plant[
                                        'id']).execute()
                                    st.balloons()
                                    st.success("🏆 **PLANT REACHED FULL GROWTH!**")

                                st.rerun()

                        else:
                            st.error("❌ **VERIFICATION FAILED**")
                            st.write("Plant health is too low for verification.")


def show_my_plants(user):
    st.header("🌿 My Plants")

    user_plants = get_user_plants(user.id)
    user_seeds = get_user_seeds(user.id)
    user_tokens = get_user_tokens(user.id)

    if FEATURES['TOKEN_SYSTEM']:
        st.subheader(f"💰 Your Tokens: {user_tokens} 🪙")

    if not user_plants and not user_seeds:
        st.info("No plants or seeds yet! Get some seeds to start.")
        return

    if user_seeds:
        st.subheader("Seed Inventory")
        for seed in user_seeds:
            if seed.get('quantity', 0) > 0:
                st.write(f"{seed['seed_name']}: {seed['quantity']} seeds")

    if user_plants:
        st.subheader("Your Plants")
        for plant in user_plants:
            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                seed_emoji = next((s['image_url'] for s in get_available_seeds() if s['name'] == plant['seed_name']),
                                  '🌱')
                st.write(f"### {seed_emoji}")

            with col2:
                status = "✅ Complete" if not plant.get('is_active', True) else "🌱 Growing"
                progress = min(100, (plant.get('current_height', 0) / 122) * 100)
                st.write(f"**{plant['seed_name']}** - {status}")
                st.progress(progress / 100)
                st.write(f"Height: {plant.get('current_height', 0)}cm / 122cm")
                st.write(f"Stage: {plant.get('current_increment', 0)}")

            with col3:
                if FEATURES['TOKEN_SYSTEM']:
                    st.write("**Tokens Earned**")
                    stages = plant.get('current_increment', 0)
                    bonus = 200 if not plant.get('is_active', True) else 0
                    estimated = stages * 75 + bonus
                    st.write(f"**~{estimated}** 🪙")


def show_analysis_history(user):
    st.header("📊 AI Analysis History")
    st.info("View detailed AI analysis results for all your plant submissions")

    # Get analysis history
    analysis_history = get_analysis_history(user.id)

    if not analysis_history:
        st.warning("No AI analysis history found. Submit some plant photos first!")
        return

    st.subheader(f"📈 Total Submissions: {len(analysis_history)}")

    # Show summary statistics with safe data access
    if analysis_history:
        # Safe calculation of statistics
        health_scores = []
        plant_detected_count = 0
        successful_verifications = 0

        for sub in analysis_history:
            # Safely access health_score with fallback
            health_score = sub.get('health_score')
            if health_score is not None:
                health_scores.append(health_score)
                if health_score > 30:
                    successful_verifications += 1

            # Safely access plant_detected with fallback
            if sub.get('plant_detected'):
                plant_detected_count += 1

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Analyses", len(analysis_history))
        with col2:
            if health_scores:
                avg_health = sum(health_scores) / len(health_scores)
                st.metric("Avg Health Score", f"{avg_health:.1f}%")
            else:
                st.metric("Avg Health Score", "N/A")
        with col3:
            st.metric("Plants Detected", f"{plant_detected_count}/{len(analysis_history)}")
        with col4:
            st.metric("Passed Verification", successful_verifications)

    # Show detailed analysis for each submission with safe data access
    st.subheader("Detailed Analysis History")

    for i, submission in enumerate(analysis_history):
        # Safe data access with fallbacks
        plant_name = submission.get('user_plants', {}).get('seed_name', 'Unknown Plant')
        submission_date = submission.get('submitted_at', 'Unknown Date')
        health_score = submission.get('health_score')
        plant_detected = submission.get('plant_detected', False)
        analysis_details = submission.get('analysis_details', 'No analysis details available')
        health_data = submission.get('health_data', {})

        # Format date safely
        try:
            if 'Z' in submission_date:
                date_obj = datetime.fromisoformat(submission_date.replace('Z', '+00:00'))
            else:
                date_obj = datetime.fromisoformat(submission_date)
            formatted_date = date_obj.strftime("%B %d, %Y at %H:%M")
        except:
            formatted_date = submission_date

        # Create expander title with safe health score display
        health_display = f"{health_score}%" if health_score is not None else "N/A"
        with st.expander(f"{plant_name} - {formatted_date} - Health: {health_display}", expanded=i < 2):

            # Main health score with color coding
            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                if health_score is not None:
                    if health_score > 60:
                        st.success(f"**Overall Health**\n# {health_score:.1f}%")
                    elif health_score > 40:
                        st.warning(f"**Overall Health**\n# {health_score:.1f}%")
                    else:
                        st.error(f"**Overall Health**\n# {health_score:.1f}%")
                else:
                    st.info("**Overall Health**\n# N/A")

            with col2:
                status = "✅ Detected" if plant_detected else "❌ Not Detected"
                st.write(f"**Plant Detection**\n{status}")

                verification = "✅ PASSED" if health_score and health_score > 30 else "❌ FAILED"
                st.write(f"**Verification**\n{verification}")

            with col3:
                st.write(f"**Analysis Summary:** {analysis_details}")

            # Detailed health metrics if available
            if health_data:
                st.subheader("🔍 Detailed Health Metrics")

                # Green/Yellow/Brown ratios with safe access
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    green_ratio = health_data.get('green_ratio', 0) * 100
                    st.metric("🌿 Green Area", f"{green_ratio:.1f}%")
                with col2:
                    yellow_ratio = health_data.get('yellow_ratio', 0) * 100
                    st.metric("🟡 Yellow Area", f"{yellow_ratio:.1f}%",
                              delta=f"{-yellow_ratio:.1f}%" if yellow_ratio > 0 else None)
                with col3:
                    brown_ratio = health_data.get('brown_ratio', 0) * 100
                    st.metric("🟤 Brown Area", f"{brown_ratio:.1f}%",
                              delta=f"{-brown_ratio:.1f}%" if brown_ratio > 0 else None)
                with col4:
                    edge_density = health_data.get('edge_density', 0) * 100
                    st.metric("📊 Texture", f"{edge_density:.1f}%")

                # Health breakdown if available
                health_breakdown = health_data.get('health_breakdown', {})
                if health_breakdown:
                    st.write("**Health Score Breakdown:**")
                    breakdown_cols = st.columns(6)
                    metrics = [
                        ("Green", health_breakdown.get('green_score', 0), "🌿"),
                        ("Texture", health_breakdown.get('texture_score', 0), "📊"),
                        ("Color", health_breakdown.get('color_score', 0), "🎨"),
                        ("Brightness", health_breakdown.get('brightness_score', 0), "💡"),
                        ("Yellow Penalty", health_breakdown.get('yellow_penalty', 0), "🟡"),
                        ("Brown Penalty", health_breakdown.get('brown_penalty', 0), "🟤")
                    ]

                    for idx, (name, value, emoji) in enumerate(metrics):
                        with breakdown_cols[idx]:
                            if "Penalty" in name:
                                st.metric(f"{emoji} {name}", f"{value:.1f}", delta=f"-{value:.1f}")
                            else:
                                st.metric(f"{emoji} {name}", f"{value:.1f}")
            else:
                st.info("No detailed health metrics available for this submission.")

            # Submission metadata with safe access
            submission_id = submission.get('id', 'N/A')
            plant_id = submission.get('plant_id', 'N/A')
            st.caption(f"Submission ID: #{submission_id} • Plant ID: {plant_id}")

def show_shop(user):
    st.header("🛍️ Token Shop")
    st.info("Spend your tokens on affordable items under 200 rupees!")

    user_tokens = get_user_tokens(user.id)
    st.success(f"### Your Balance: {user_tokens:,} 🪙")

    shop_items = [
        # VERY SMALL ITEMS (2000-4000 tokens)
        {'id': 1, 'name': 'Pencil', 'description': 'Single wooden pencil', 'price': 2000, 'category': 'stationery', 'image': '✏️'},
        {'id': 2, 'name': 'Ball Pen', 'description': 'Basic ballpoint pen', 'price': 2500, 'category': 'stationery', 'image': '🖊️'},
        {'id': 3, 'name': 'Paper Clip', 'description': 'Box of 100 paper clips', 'price': 2000, 'category': 'stationery', 'image': '🧷'},
        {'id': 4, 'name': 'Push Pin', 'description': 'Set of 20 push pins', 'price': 2500, 'category': 'stationery', 'image': '📌'},
        {'id': 5, 'name': 'Bookmark', 'description': 'Decorative bookmark', 'price': 2000, 'category': 'stationery', 'image': '🔖'},
        {'id': 6, 'name': 'Sticky Notes', 'description': 'Small sticky note pad', 'price': 3000, 'category': 'stationery', 'image': '📜'},
        {'id': 7, 'name': 'Small Scissors', 'description': 'Mini safety scissors', 'price': 3500, 'category': 'stationery', 'image': '✂️'},
        {'id': 8, 'name': 'Rubber Band', 'description': 'Pack of 50 rubber bands', 'price': 2000, 'category': 'stationery', 'image': '🧮'},
        {'id': 9, 'name': '15cm Ruler', 'description': 'Small plastic ruler', 'price': 2500, 'category': 'stationery', 'image': '📏'},
        {'id': 10, 'name': 'Crayon', 'description': 'Single wax crayon', 'price': 2000, 'category': 'stationery', 'image': '🖍️'},

        # BASIC STATIONERY (3000-5000 tokens)
        {'id': 11, 'name': 'Small Notebook', 'description': 'Pocket sized notebook', 'price': 4000, 'category': 'stationery', 'image': '📒'},
        {'id': 12, 'name': 'Gel Pen', 'description': 'Smooth gel ink pen', 'price': 3500, 'category': 'stationery', 'image': '🖋️'},
        {'id': 13, 'name': 'Eraser', 'description': 'Quality pencil eraser', 'price': 3000, 'category': 'stationery', 'image': '🧽'},
        {'id': 14, 'name': 'Geometry Set', 'description': 'Basic geometry tools', 'price': 4500, 'category': 'stationery', 'image': '📐'},
        {'id': 15, 'name': 'Printer Paper', 'description': '10 sheets A4 paper', 'price': 3500, 'category': 'stationery', 'image': '🖨️'},
        {'id': 16, 'name': 'Envelopes', 'description': 'Pack of 5 envelopes', 'price': 3000, 'category': 'stationery', 'image': '📮'},
        {'id': 17, 'name': 'Pen Refill', 'description': 'Ink refill for pens', 'price': 2500, 'category': 'stationery', 'image': '🖊️'},
        {'id': 18, 'name': 'Writing Pad', 'description': 'Small writing pad', 'price': 4000, 'category': 'stationery', 'image': '📝'},
        {'id': 19, 'name': 'Magnifying Glass', 'description': 'Small magnifier', 'price': 4500, 'category': 'stationery', 'image': '🔍'},
        {'id': 20, 'name': 'Book Cover', 'description': 'Plastic book cover', 'price': 3000, 'category': 'stationery', 'image': '📚'},

        # DIGITAL & MOBILE (5000-10000 tokens)
        {'id': 21, 'name': 'Mobile Recharge', 'description': '₹50 mobile top-up', 'price': 5000, 'category': 'digital', 'image': '📱'},
        {'id': 22, 'name': 'Music Subscription', 'description': '1 month music app', 'price': 6000, 'category': 'digital', 'image': '🎵'},
        {'id': 23, 'name': 'Game Voucher', 'description': '₹100 gaming credit', 'price': 8000, 'category': 'digital', 'image': '🎮'},
        {'id': 24, 'name': 'Streaming Pass', 'description': '2 week streaming', 'price': 7000, 'category': 'digital', 'image': '📺'},
        {'id': 25, 'name': 'App Store Credit', 'description': '₹150 app store', 'price': 9000, 'category': 'digital', 'image': '💻'},
        {'id': 26, 'name': 'Arcade Tokens', 'description': 'Digital game tokens', 'price': 5000, 'category': 'digital', 'image': '🕹️'},
        {'id': 27, 'name': 'Email Storage', 'description': 'Extra cloud storage', 'price': 6000, 'category': 'digital', 'image': '📧'},
        {'id': 28, 'name': 'Ringtone Pack', 'description': 'Custom ringtones', 'price': 4000, 'category': 'digital', 'image': '🎧'},
        {'id': 29, 'name': 'Wallpaper Pack', 'description': 'HD phone wallpapers', 'price': 3000, 'category': 'digital', 'image': '📱'},
        {'id': 30, 'name': 'Photo Filter Pack', 'description': 'Premium photo filters', 'price': 5000, 'category': 'digital', 'image': '🖼️'},

        # PERSONAL CARE (4000-8000 tokens)
        {'id': 31, 'name': 'Hand Sanitizer', 'description': '50ml hand sanitizer', 'price': 4000, 'category': 'personal', 'image': '🧴'},
        {'id': 32, 'name': 'Soap Bar', 'description': 'Natural soap bar', 'price': 3500, 'category': 'personal', 'image': '🧼'},
        {'id': 33, 'name': 'Toothbrush', 'description': 'Soft bristle toothbrush', 'price': 3000, 'category': 'personal', 'image': '🪥'},
        {'id': 34, 'name': 'Toothpaste', 'description': '100g toothpaste', 'price': 4500, 'category': 'personal', 'image': '🦷'},
        {'id': 35, 'name': 'Lip Balm', 'description': 'Moisturizing lip balm', 'price': 3500, 'category': 'personal', 'image': '🧴'},
        {'id': 36, 'name': 'Hand Cream', 'description': 'Travel size hand cream', 'price': 4000, 'category': 'personal', 'image': '🧴'},
        {'id': 37, 'name': 'Face Wash', 'description': 'Gentle face cleanser', 'price': 5000, 'category': 'personal', 'image': '🧴'},
        {'id': 38, 'name': 'Deodorant', 'description': 'Roll-on deodorant', 'price': 4500, 'category': 'personal', 'image': '🧴'},
        {'id': 39, 'name': 'Shampoo Sachet', 'description': 'Single use shampoo', 'price': 2000, 'category': 'personal', 'image': '🧴'},
        {'id': 40, 'name': 'Conditioner Sachet', 'description': 'Single use conditioner', 'price': 2000, 'category': 'personal', 'image': '🧴'},

        # FOOD & SNACKS (3000-8000 tokens)
        {'id': 41, 'name': 'Chocolate Bar', 'description': 'Milk chocolate 50g', 'price': 4000, 'category': 'food', 'image': '🍫'},
        {'id': 42, 'name': 'Candy Pack', 'description': 'Assorted candies', 'price': 3000, 'category': 'food', 'image': '🍬'},
        {'id': 43, 'name': 'Cookie Pack', 'description': '4 cookies pack', 'price': 3500, 'category': 'food', 'image': '🍪'},
        {'id': 44, 'name': 'Popcorn', 'description': 'Microwave popcorn', 'price': 4500, 'category': 'food', 'image': '🍿'},
        {'id': 45, 'name': 'Juice Box', 'description': '250ml fruit juice', 'price': 4000, 'category': 'food', 'image': '🥤'},
        {'id': 46, 'name': 'Instant Coffee', 'description': '10 sachets coffee', 'price': 5000, 'category': 'food', 'image': '☕'},
        {'id': 47, 'name': 'Tea Bags', 'description': '10 tea bags', 'price': 3500, 'category': 'food', 'image': '🍵'},
        {'id': 48, 'name': 'Instant Noodles', 'description': 'Single noodle pack', 'price': 3000, 'category': 'food', 'image': '🍜'},
        {'id': 49, 'name': 'Energy Bar', 'description': 'Granola energy bar', 'price': 4000, 'category': 'food', 'image': '🍫'},
        {'id': 50, 'name': 'Chewing Gum', 'description': 'Pack of chewing gum', 'price': 2500, 'category': 'food', 'image': '🍬'},

        # JOKE ITEMS (Impossibly expensive)
        {'id': 131, 'name': 'PlayStation 5', 'description': 'Next-gen gaming console', 'price': 100000000000, 'category': 'electronics', 'image': '🎮'},
        {'id': 132, 'name': 'Gaming Laptop', 'description': 'High-end gaming laptop', 'price': 50000000000, 'category': 'electronics', 'image': '💻'},
        {'id': 133, 'name': 'iPhone Pro', 'description': 'Latest smartphone', 'price': 30000000000, 'category': 'electronics', 'image': '📱'},
        {'id': 134, 'name': 'Apple Watch', 'description': 'Premium smartwatch', 'price': 20000000000, 'category': 'electronics', 'image': '⌚'},
        {'id': 135, 'name': 'Smart Home', 'description': 'Complete smart home system', 'price': 150000000000, 'category': 'electronics', 'image': '🏠'},
    ]

    # Rest of the shop code remains the same...
    tab1, tab2, tab3, tab4 = st.tabs(["🎵 Digital", "🖊️ Stationery", "🔑 Accessories", "🎮 Dream Items"])

    with tab1:
        digital_items = [item for item in shop_items if item['category'] == 'digital']
        for item in digital_items:
            col1, col2, col3 = st.columns([1, 3, 2])
            with col1:
                st.write(f"### {item['image']}")
            with col2:
                st.write(f"**{item['name']}**")
                st.write(item['description'])
            with col3:
                st.write(f"**{item['price']:,} 🪙**")
                if st.button(f"Buy Now", key=f"buy_{item['id']}", disabled=user_tokens < item['price']):
                    st.session_state.selected_item = item
                    st.rerun()

    with tab2:
        stationery_items = [item for item in shop_items if item['category'] == 'stationery']
        for item in stationery_items:
            col1, col2, col3 = st.columns([1, 3, 2])
            with col1:
                st.write(f"### {item['image']}")
            with col2:
                st.write(f"**{item['name']}**")
                st.write(item['description'])
            with col3:
                st.write(f"**{item['price']:,} 🪙**")
                if st.button(f"Buy Now", key=f"buy_{item['id']}", disabled=user_tokens < item['price']):
                    st.session_state.selected_item = item
                    st.rerun()

    with tab3:
        accessory_items = [item for item in shop_items if item['category'] in ['personal', 'food']]
        for item in accessory_items:
            col1, col2, col3 = st.columns([1, 3, 2])
            with col1:
                st.write(f"### {item['image']}")
            with col2:
                st.write(f"**{item['name']}**")
                st.write(item['description'])
            with col3:
                st.write(f"**{item['price']:,} 🪙**")
                if st.button(f"Buy Now", key=f"buy_{item['id']}", disabled=user_tokens < item['price']):
                    st.session_state.selected_item = item
                    st.rerun()

    with tab4:
        joke_items = [item for item in shop_items if item['price'] > 1000000]
        for item in joke_items:
            col1, col2, col3 = st.columns([1, 3, 2])
            with col1:
                st.write(f"### {item['image']}")
            with col2:
                st.write(f"**{item['name']}**")
                st.write(item['description'])
            with col3:
                st.write(f"**{item['price']:,} 🪙**")
                st.button(f"Dream Buy", key=f"buy_{item['id']}", disabled=True)

    # Rest of the checkout code remains the same...
    if 'selected_item' in st.session_state:
        item = st.session_state.selected_item
        st.subheader(f"🎁 Checkout: {item['name']}")
        st.write(f"**Price:** {item['price']:,} 🪙")
        st.write(f"**Your balance:** {user_tokens:,} 🪙")

        if user_tokens >= item['price']:
            with st.form("billing_form"):
                full_name = st.text_input("Full Name")
                email = st.text_input("Email", value=user.email)
                phone = st.text_input("Phone Number")
                address = st.text_area("Shipping Address")
                city = st.text_input("City")
                zip_code = st.text_input("ZIP Code")
                country = st.text_input("Country")

                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("🚀 Confirm Purchase"):
                        if all([full_name, email, phone, address, city, zip_code, country]):
                            try:
                                # Deduct tokens
                                new_balance = user_tokens - item['price']
                                supabase_client.table('user_tokens').update({'tokens': new_balance}).eq('user_id',
                                                                                                        user.id).execute()

                                # Save billing info
                                billing_data = {
                                    'user_id': user.id,
                                    'full_name': full_name,
                                    'email': email,
                                    'address': address,
                                    'city': city,
                                    'zip_code': zip_code,
                                    'country': country,
                                    'phone': phone
                                }
                                supabase_client.table('user_billing_info').upsert(billing_data).execute()

                                # Record purchase
                                purchase_data = {
                                    'user_id': user.id,
                                    'item_id': item['id'],
                                    'item_name': item['name'],
                                    'price': item['price'],
                                    'billing_info': billing_data,
                                    'purchased_at': datetime.now(timezone.utc).isoformat(),
                                    'status': 'pending'
                                }
                                supabase_client.table('purchases').insert(purchase_data).execute()

                                st.success("🎉 Purchase successful! Item will be shipped soon.")
                                time.sleep(2)
                                st.rerun()
                            except Exception as e:
                                st.error("Purchase failed")
                with col2:
                    if st.form_submit_button("❌ Cancel"):
                        del st.session_state.selected_item
                        st.rerun()
        else:
            st.error("Insufficient tokens!")
            if st.button("Back to Shop"):
                del st.session_state.selected_item
                st.rerun()


if __name__ == "__main__":
    main()


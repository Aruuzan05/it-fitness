import streamlit as st 
import pandas as pd 
import numpy as np 
import joblib 

@st.cache_resource 

def load_assets():
    preprocessor = joblib.load('../models/preprocessor.pkl')
    model = joblib.load('../models/linearreg.pkl')
    return preprocessor, model 

preprocessor, model = load_assets()

st.title("MetriFit AI Professional")

with st.sidebar:
    st.header("Demographics & Body")
    age = st.number_input("Age (RIDAGEYR)", 18, 80, 24)
    gender = st.selectbox("Gender (RIAGENDR)", options=[("Male", 1), ("Female", 2)], format_func=lambda x: x[0])[1]
    ethnicity = st.selectbox("Ethnicity (RIDRETH3)", options=[1, 2, 3, 4, 6, 7])
    weight = st.number_input("Weight (BMXWT) kg", 40.0, 200.0, 75.0)
    height = st.number_input("Height (BMXHT) cm", 120.0, 220.0, 175.0)
    
    st.header("Measurements")
    waist = st.number_input("Waist (BMXWAIST) cm", 50.0, 150.0, 85.0)
    hip = st.number_input("Hip (BMXHIP) cm", 50.0, 150.0, 95.0)
    arm = st.number_input("Arm Length (BMXARML) cm", 20.0, 50.0, 35.0)

# Main Screen for Activity and Nutrition
col1, col2 = st.columns(2)

with col1:
    st.subheader("Physical Activity (Weekly)")
    v_days = st.slider("Vigorous Days", 0, 7, 3)
    v_mins = st.number_input("Vigorous Mins/Day", 0, 240, 45)
    m_days = st.slider("Moderate Days", 0, 7, 5)
    m_mins = st.number_input("Moderate Mins/Day", 0, 240, 30)

with col2:
    st.subheader("Daily Nutrition")
    cals = st.number_input("Total Calories", 1000, 5000, 2200)
    prot = st.number_input("Protein (g)", 0, 300, 150)
    fats = st.number_input("Fats (g)", 0, 200, 70)
    carbs = st.number_input("Carbs (g)", 0, 600, 250)

# --- 3. ON-THE-FLY FEATURE ENGINEERING ---
# This block recreates your training logic exactly
vig_met = v_days * v_mins * 8
mod_met = m_days * m_mins * 4
total_met = vig_met + mod_met

# BMR & TDEE Logic
if gender == 1:
    bmr_val = (10 * weight) + (6.25 * height) - (5 * age) + 5
else:
    bmr_val = (10 * weight) + (6.25 * height) - (5 * age) - 161

# Activity Multiplier mapping
if total_met < 600: act_mult = 1.2
elif total_met < 1500: act_mult = 1.375
elif total_met < 3000: act_mult = 1.55
else: act_mult = 1.725

tdee_val = bmr_val * act_mult
surplus = cals - tdee_val

# Create the final Feature Dictionary
input_data = {
    'RIDAGEYR': age, 'RIAGENDR': gender, 'RIDRETH3': ethnicity,
    'BMXWT': weight, 'BMXHT': height, 'BMXWAIST': waist,
    'BMXHIP': hip, 'BMXARML': arm,
    'PAQ610': v_days, 'PAD615': v_mins, 'PAQ625': m_days, 'PAD630': m_mins,
    'PAQ655': v_days, 'PAD660': v_mins, 'PAQ670': m_days, 'PAD675': m_mins,
    'vig_met': vig_met, 'mod_met': mod_met, 'total_met_min': total_met,
    'act_mult': act_mult, 'bmr': bmr_val, 'tdee': tdee_val,
    'calories': cals, 'protein_g': prot, 'fat_g': fats, 'carb_g': carbs,
    'sugar_g': 40, 'fiber_g': 25, 'sur_def': surplus # Using defaults for sugar/fiber if not input
}

# --- 4. PREDICTION ---
X_input = pd.DataFrame([input_data])

if st.button("Generate AI Weight Analysis"):
    # Ensure columns are in the EXACT order the preprocessor expects
    X_input = X_input[preprocessor.feature_names_in_]
    
    X_scaled = preprocessor.transform(X_input)
    prediction_diff = model.predict(X_scaled)[0]
    
    prediction = weight + prediction_diff
    st.divider()
    st.subheader(f"Predicted Weight Changes in 7 days: {prediction:.2f} kg")
    
    

    if abs(prediction_diff) < 0.5:
        st.info("Your current habits are maintaining your current weight.")
    elif prediction_diff > 0:
        st.warning(f"Warning: Current intake suggests a gain of {prediction_diff:.2f} kg.")
    else:
        st.success(f"Success: Current habits suggest a loss of {abs(prediction_diff):.2f} kg.")
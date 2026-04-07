Develop an end-to-end Data Science application that goes beyond static calorie counting. The system will predict a user's weight trajectory using supervised learning and provide real-time macronutrient optimization using constrained optimization algorithms.

Technical Requirements & Details

┌─────────────────────────────────────────────────────────┐
│ INFERENCE TIME │
│ (every time a user submits) │
│ │
│ USER INPUTS (from Streamlit sidebar): │
│ age → e.g. 24 │
│ sex → male / female │
│ height_cm → e.g. 175 │
│ weight_kg → e.g. 82 │
│ calories → e.g. 2200 (what they eat daily) │
│ sedentary_mins → e.g. 480 │
│ sleep_hrs → e.g. 7 │
│ protein_g → e.g. 120 │
│ fat_g → e.g. 70 │
│ carb_g → e.g. 200 │
│ │
│ FEATURE ENGINEERING (same functions as training): │
│ caloric_surplus = calories - tdee │
│ surplus_per_kg = caloric_surplus / weight_kg │
│ bmi = weight_kg / height_m² │
│ │
│ MODEL PREDICTION: │
│ predicted_change = model.predict(X_user) │
│ → e.g. −0.8 kg (will lose ~0.8 kg in 7 days) │
│ │
│ WEIGHT TRAJECTORY (for the Plotly chart): │
│ Repeat prediction across N weeks, updating │
│ weight_kg each iteration: │
│ week 0: 82.0 kg │
│ week 1: 82.0 + (−0.8) = 81.2 kg │
│ week 2: 81.2 + model.predict(81.2, ...) = 80.5 kg │
│ ... │
│ │
│ OPTIMIZER INPUT: │
│ goal_weight_kg (from slider) → e.g. 75 kg │
│ timeline_weeks (from slider) → e.g. 12 weeks │
│ → required deficit = (82−75)×7700 / (12×7) kcal/day │
│ → target_calories = tdee − required_deficit │
│ │
│ OPTIMIZER OUTPUT (SciPy): │
│ protein_g = 2.0 × 75 = 150 g (600 kcal) │
│ fat_g = 25% × 1800 / 9 = 50 g (450 kcal) │
│ carb_g = remaining / 4 = 187 g (750 kcal) │
│ total = 1800 kcal/day │
│ │
│ LLM INPUT: │
│ "Generate a meal plan for 150g protein, │
│ 50g fat, 187g carbs (1800 kcal)" │
│ │
│ LLM OUTPUT (displayed in Streamlit): │
│ Breakfast: ..., Lunch: ..., Dinner: ..., │
│ Grocery list: ... │

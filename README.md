Develop an end-to-end Data Science application that goes beyond static calorie counting. The system will predict a user's weight trajectory using supervised learning and provide real-time macronutrient optimization using constrained optimization algorithms.
Technical Requirements & Details

1. Data Engineering & Sources

- Historical Data: Use the NHANES (CDC) dataset or a synthetic dataset generated via Python (NumPy/Pandas) containing: Age, Sex, Height, Weight, Body Fat %, Daily Steps, Sleep Hours, and Caloric Intake.
- Target Variable: Weight_Change_n+7 (Predicting weight 7 days into the future).
- Feature Engineering:
  - Implement the Mifflin-St Jeor and Katch-McArdle equations as "Engineered Features" to provide the model with a biological baseline.
  - Calculate Rolling Averages (7-day and 14-day) of caloric intake to account for metabolic adaptation.

2. Machine Learning Pipeline

- Model Selection: Compare a Gradient Boosting Regressor (XGBoost/LightGBM) with a Simple Neural Network (Multi-Layer Perceptron) built in PyTorch or TensorFlow.
- Loss Function: Use Mean Absolute Error (MAE) to ensure the prediction is interpreted in "kg" or "lbs" for easy user understanding.
- Optimization Layer: Use SciPy.optimize to solve for daily macros.
  - Constraints: Protein fixed at $2.0g/kg$ of body weight; Fats at $25\%$ of total calories; remaining calories allocated to Carbohydrates.

3. Software Architecture (The "Full Stack" DS)

- Backend: Python/FastAPI to serve model predictions.
- Frontend: Streamlit dashboard showing:
  - An interactive slider for "Goal Weight" and "Timeline."
  - A Plotly graph showing the predicted weight curve vs. the theoretical "formula-based" curve.
  - A "Daily Meal Plan" generator using an LLM (GPT-4o or Gemini) that converts the optimized macros into a grocery list.

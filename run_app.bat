@echo off
echo Installing dependencies...
python -m pip install -r requirements.txt
echo.
echo Starting Diabetes Prediction System...
python -m streamlit run app.py
pause


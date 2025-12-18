@echo off
echo Installing dependencies...
python -m pip install -r requirements.txt
echo.
echo Running Diabetes Prediction Script...
python diabetes_prediction.py
pause


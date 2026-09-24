# Diabetes Prediction System

Streamlit web app for diabetes risk prediction using a tuned **K-Nearest Neighbors (KNN)** model on the Pima Indians Diabetes dataset.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

Or on Windows: `start_app.bat` or `run_app.bat` (installs dependencies then runs the app).

## Optional: train / evaluate from the CLI

```bash
python diabetes_prediction.py
```

This trains all models defined in `diabetes_prediction.py` and prints metrics (the live app uses tuned KNN only, loaded from `saved_models/diabetes_model.pkl` when present).

## Features

- Login / sign-up (`users.json`)
- Predictions with doctor recommendations (`doctors.json`, `predictions.json`)
- Admin panel for managing doctors
- Dataset file `diabetes.csv` is used if present; otherwise it is downloaded automatically

## Requirements

Python 3.8+ — see `requirements.txt`.
